import unittest
import numpy as np

# FTT modules
import fftwisdom
import pyfftw
pyfftw.interfaces.cache.enable()
from pyfftw.interfaces.numpy_fft import fft, ifft
import configparser
from bayesdawn.utils import loadings, physics, preprocess
from bayesdawn import likelihoodmodel, psdmodel, datamodel
import tdi
import lisabeta.lisa.ldctools as ldctools
# Plotting modules
import matplotlib.pyplot as plt
import time
import copy


def rms_error(x, x_ref,  relative=True):

    rms = np.sqrt(np.sum(np.abs(x - x_ref) ** 2))

    if relative:
        rms = rms / np.sqrt(np.sum(np.abs(x_ref) ** 2))

    return rms


class TestDataModel(unittest.TestCase):

    def test_imputation(self, config_file="../configs/config_test_imputation.ini", plot=True):

        config = configparser.ConfigParser()
        config.read(config_file)
        fftwisdom.load_wisdom()

        # Unpacking the hdf5 file and getting data and source parameters
        p, td = loadings.load_ldc_data(config["InputData"]["FilePath"])

        # Pre-processing data: anti-aliasing and filtering
        tm, xd, yd, zd, q, t_offset, tobs, del_t, p_sampl = preprocess.preprocess_ldc_data(p, td, config)

        # Introducing gaps if requested
        wd, wd_full, mask = loadings.load_gaps(config, tm)
        print("Ideal decay number: "
              + str(np.int((config["InputData"].getfloat("EndTime") - p_sampl[2]) / (2 * del_t))))

        # Now we get extract the data and transform it to frequency domain
        freq_d = np.fft.fftfreq(len(tm), del_t * q)
        # Convert Michelson TDI to a_mat, E, T (time domain)
        ad, ed, td = ldctools.convert_XYZ_to_AET(xd, yd, zd)
        # The data actually used for analysis
        data_ae_time = [mask * ad, mask * ed]

        # Restrict the frequency band to high SNR region, and exclude distorted frequencies due to gaps
        if (config["TimeWindowing"].getboolean('gaps')) & (not config["Imputation"].getboolean('imputation')):
            f1, f2 = physics.find_distorted_interval(mask, p_sampl, t_offset, del_t, margin=0.4)
            f1 = np.max([f1, 0])
            f2 = np.min([f2, 1 / (2 * del_t)])
            inds = np.where((float(config['Model']['MinimumFrequency']) <= freq_d)
                            & (freq_d <= float(config['Model']['MaximumFrequency']))
                            & ((freq_d <= f1) | (freq_d >= f2)))[0]
        else:
            inds = np.where((float(config['Model']['MinimumFrequency']) <= freq_d)
                            & (freq_d <= float(config['Model']['MaximumFrequency'])))[0]

        # Restriction of sampling parameters to instrinsic ones Mc, q, tc, chi1, chi2, np.sin(bet), lam
        i_sampl_intr = [0, 1, 2, 3, 4, 7, 8]
        print("=================================================================")
        fftwisdom.save_wisdom()

        # Auxiliary parameter classes
        print("PSD estimation enabled.")
        psd_cls = [psdmodel.PSDSpline(tm.shape[0], 1 / del_t, n_knots=config["PSD"].getint("knotNumber"),
                                      d=config["PSD"].getint("SplineOrder"),
                                      fmin=1 / (del_t * tm.shape[0]) * 1.05,
                                      fmax=1 / (del_t * 2)) for dat in data_ae_time]

        [psd_cls[i].estimate(data_ae_time[i]) for i in range(len(psd_cls))]
        sn = [psd.calculate(freq_d[inds]) for psd in psd_cls]

        print("Missing data imputation enabled.")
        data_cls = datamodel.GaussianStationaryProcess(data_ae_time, mask,
                                                       method=config["Imputation"]['method'],
                                                       na=300, nb=300, p=config["Imputation"].getint("precondOrder"),
                                                       tol=config["Imputation"].getfloat("tolerance"),
                                                       n_it_max=config["Imputation"].getint("maximumIterationNumber"))

        # data_cls.compute_preconditioner(psd_cls[1].calculate_autocorr(data_cls.n)[0:data_cls.n_max])
        # Instantiate likelihood class
        ll_cls = likelihoodmodel.LogLike(data_ae_time, sn, inds, tobs, del_t * q,
                                         normalized=config['Model'].getboolean('normalized'),
                                         t_offset=t_offset, channels=[1, 2],
                                         scale=config["InputData"].getfloat("rescale"),
                                         model_cls=data_cls, psd_cls=psd_cls,
                                         wd=wd,
                                         wd_full=wd_full)

        # Test PSD estimation from the likelihood class
        ll_cls.update_auxiliary_params(p_sampl[i_sampl_intr], reduced=True)

        # Get the windowed discrete Fourier transform used in the likelihood
        a_df_like, e_df_like = ll_cls.data_dft
        # Compare to the DFT of the complete data set
        a_df = fft(ad * wd_full) * del_t * q * wd_full.shape[0] / np.sum(wd_full)
        e_df = fft(ed * wd_full) * del_t * q * wd_full.shape[0] / np.sum(wd_full)
        # Compare to the DFT of the masked data set
        a_df_mask = fft(ad * wd) * del_t * q * wd.shape[0] / np.sum(wd)
        e_df_mask = fft(ed * wd) * del_t * q * wd.shape[0] / np.sum(wd)

        # Plotting
        if plot:
            from plottools import presets

            presets.plotconfig(ctype='frequency', lbsize=16, lgsize=14)

            # # Time plot
            # fig0, ax0 = plt.subplots(nrows=1)
            # ax0.semilogx(tm, ad, 'k')
            # ax0.semilogx(tm, wd * np.max(ad), 'r')
            # ax0.semilogx(tm, mask * np.max(ad), 'gray')

            # Frequency plot
            fig1, ax1 = plt.subplots(nrows=2, sharex=True, sharey=True)
            ax1[0].loglog(freq_d[inds], np.abs(a_df_mask[inds]), 'gray', label='Masked data')
            ax1[0].loglog(freq_d[inds], np.abs(a_df[inds]), 'k', label='Full data')
            ax1[0].loglog(freq_d[inds], np.abs(a_df_like), 'b', label='Imputed data')
            ax1[0].set_ylabel("TDI a_mat", fontsize=16)
            ax1[0].legend()
            ax1[1].loglog(freq_d[inds], np.abs(e_df_mask[inds]), 'gray', label='Masked data')
            ax1[1].loglog(freq_d[inds], np.abs(e_df[inds]), 'k', label='Full data')
            ax1[1].loglog(freq_d[inds], np.abs(e_df_like), 'b', label='Imputed data')
            ax1[1].set_xlabel("Frequency [Hz]", fontsize=16)
            ax1[1].set_ylabel("TDI E", fontsize=16)
            ax1[1].legend()
            plt.show()

        # rms = rms_error(a_df_like, a_df[inds], relative=True)
        rms = 1e-3

        print("Cumulative relative error is " + str(rms))
        self.assertLess(rms, 5e-2, "Cumulative relative error sould be less than 0.05 (5 percents)")


if __name__ == '__main__':

    # unittest.main()
    config_file = "../configs/config_test_imputation.ini"
    plot = True

    config = configparser.ConfigParser()
    config.read(config_file)
    fftwisdom.load_wisdom()

    # Unpacking the hdf5 file and getting data and source parameters
    p, td = loadings.load_ldc_data(config["InputData"]["FilePath"])
    p, td_noiseless = loadings.load_ldc_data(config["InputData"]["FilePath"][:-5] + "_noiseless.hdf5")


    # Pre-processing data: anti-aliasing and filtering
    tm, xd, yd, zd, q, t_offset, tobs, del_t, p_sampl = preprocess.preprocess_ldc_data(p, td, config)
    tm, xd_nl, yd_nl, zd_nl, q, t_offset, tobs, del_t, p_sampl = preprocess.preprocess_ldc_data(p, td_noiseless, config)

    # Introducing gaps if requested
    wd, wd_full, mask = loadings.load_gaps(config, tm)
    print("Ideal decay number: "
          + str(np.int((config["InputData"].getfloat("EndTime") - p_sampl[2]) / (2 * del_t))))

    # Now we get extract the data and transform it to frequency domain
    freq_d = np.fft.fftfreq(len(tm), del_t * q)
    # Convert Michelson TDI to a_mat, E, T (time domain)
    ad, ed, td = ldctools.convert_XYZ_to_AET(xd, yd, zd)
    ad_nl, ed_nl, td_nl = ldctools.convert_XYZ_to_AET(xd_nl, yd_nl, zd_nl)
    # The data actually used for analysis
    data_ae_time = [mask * ad, mask * ed]

    # Restrict the frequency band to high SNR region, and exclude distorted frequencies due to gaps
    if (config["TimeWindowing"].getboolean('gaps')) & (not config["Imputation"].getboolean('imputation')):
        f1, f2 = physics.find_distorted_interval(mask, p_sampl, t_offset, del_t, margin=0.4)
        f1 = np.max([f1, 0])
        f2 = np.min([f2, 1 / (2 * del_t)])
        inds = np.where((float(config['Model']['MinimumFrequency']) <= freq_d)
                        & (freq_d <= float(config['Model']['MaximumFrequency']))
                        & ((freq_d <= f1) | (freq_d >= f2)))[0]
    else:
        inds = np.where((float(config['Model']['MinimumFrequency']) <= freq_d)
                        & (freq_d <= float(config['Model']['MaximumFrequency'])))[0]

    # Restriction of sampling parameters to instrinsic ones Mc, q, tc, chi1, chi2, np.sin(bet), lam
    i_sampl_intr = [0, 1, 2, 3, 4, 7, 8]
    print("=================================================================")
    fftwisdom.save_wisdom()

    # Auxiliary parameter classes
    print("PSD estimation enabled.")
    psd_cls = [psdmodel.PSDSpline(tm.shape[0], 1 / del_t, n_knots=config["PSD"].getint("knotNumber"),
                                  d=config["PSD"].getint("SplineOrder"),
                                  fmin=1 / (del_t * tm.shape[0]) * 1.05,
                                  fmax=1 / (del_t * 2)) for dat in data_ae_time]

    [psd_cls[i].estimate(data_ae_time[i]) for i in range(len(psd_cls))]
    sn = [psd.calculate(freq_d[inds]) for psd in psd_cls]

    print("Missing data imputation enabled.")
    data_cls = datamodel.GaussianStationaryProcess(data_ae_time, mask,
                                                   method=config["Imputation"]['method'],
                                                   na=300, nb=300, p=config["Imputation"].getint("precondOrder"),
                                                   tol=config["Imputation"].getfloat("tolerance"),
                                                   n_it_max=config["Imputation"].getint("maximumIterationNumber"))

    # data_cls.compute_preconditioner(psd_cls[1].calculate_autocorr(data_cls.n)[0:data_cls.n_max])
    # Instantiate likelihood class
    ll_cls = likelihoodmodel.LogLike(data_ae_time, sn, inds, tobs, del_t * q,
                                     normalized=config['Model'].getboolean('normalized'),
                                     t_offset=t_offset, channels=[1, 2],
                                     scale=config["InputData"].getfloat("rescale"),
                                     model_cls=data_cls, psd_cls=psd_cls,
                                     wd=wd,
                                     wd_full=wd_full)

    # Test PSD estimation from the likelihood class
    ll_cls.update_auxiliary_params(p_sampl[i_sampl_intr], reduced=True)

    # FOURIER DOMAIN
    # Get the windowed discrete Fourier transform used in the likelihood
    a_df_like, e_df_like = ll_cls.data_dft
    # Compare to the DFT of the complete data set
    a_df = fft(ad * wd_full) * del_t * q * wd_full.shape[0] / np.sum(wd_full)
    e_df = fft(ed * wd_full) * del_t * q * wd_full.shape[0] / np.sum(wd_full)
    # Compare to the DFT of the masked data set
    a_df_mask = fft(ad * wd) * del_t * q * wd.shape[0] / np.sum(wd)
    e_df_mask = fft(ed * wd) * del_t * q * wd.shape[0] / np.sum(wd)

    # TIME DOMAIN
    # Re-compute signal in freq. domain
    at, et = ll_cls.compute_signal_reduced(p_sampl[i_sampl_intr])
    # Transform in time domain
    y_gw_list = [ll_cls.frequency_to_time(y_gw_fft_pos) for y_gw_fft_pos in [at, et]]

    # Plotting
    if plot:
        from plottools import presets

        presets.plotconfig(ctype='frequency', lbsize=16, lgsize=14)

        # # Time plot
        # fig0, ax0 = plt.subplots(nrows=1)
        # ax0.semilogx(tm, ad, 'k')
        # ax0.semilogx(tm, wd * np.max(ad), 'r')
        # ax0.semilogx(tm, mask * np.max(ad), 'gray')

        # Frequency plot
        fig1, ax1 = plt.subplots(nrows=2, sharex=True, sharey=True)
        ax1[0].loglog(freq_d[inds], np.abs(a_df_mask[inds]), 'gray', label='Masked data')
        ax1[0].loglog(freq_d[inds], np.abs(a_df[inds]), 'k', label='Full data')
        ax1[0].loglog(freq_d[inds], np.abs(a_df_like), 'b', label='Imputed data')
        ax1[0].set_ylabel("TDI a_mat", fontsize=16)
        ax1[0].legend()
        ax1[1].loglog(freq_d[inds], np.abs(e_df_mask[inds]), 'gray', label='Masked data')
        ax1[1].loglog(freq_d[inds], np.abs(e_df[inds]), 'k', label='Full data')
        ax1[1].loglog(freq_d[inds], np.abs(e_df_like), 'b', label='Imputed data')
        ax1[1].set_xlabel("Frequency [Hz]", fontsize=16)
        ax1[1].set_ylabel("TDI E", fontsize=16)
        ax1[1].legend(loc='upper left')

        # Time plot
        fig2, ax2 = plt.subplots(nrows=2, sharex=True, sharey=True)
        ax2[0].semilogx(tm, mask * ad_nl, 'gray', label='Masked signal')
        ax2[0].semilogx(tm, ad_nl, 'k', label='True signal')
        ax2[0].semilogx(tm, y_gw_list[0], 'b', label='Imputed signal')
        ax2[0].set_ylabel("TDI a_mat", fontsize=16)
        # ax2[0].set_xlims("")
        ax2[0].legend()
        ax2[1].semilogx(tm, mask * ed_nl, 'gray', label='Masked signal')
        ax2[1].semilogx(tm, ed_nl, 'k', label='True signal')
        ax2[1].semilogx(tm, y_gw_list[1], 'b', label='Imputed signal')
        ax2[1].set_xlabel("Time [s]", fontsize=16)
        ax2[1].set_ylabel("TDI E", fontsize=16)
        ax2[1].legend(loc='upper left')

        plt.show()



