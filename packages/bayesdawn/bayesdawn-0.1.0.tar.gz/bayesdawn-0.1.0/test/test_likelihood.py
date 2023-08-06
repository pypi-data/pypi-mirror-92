import unittest
import numpy as np

# FTT modules
import fftwisdom
import pyfftw
pyfftw.interfaces.cache.enable()
from pyfftw.interfaces.numpy_fft import fft, ifft
import configparser
from bayesdawn.utils import loadings, physics, preprocess
from bayesdawn import likelihoodmodel, psdmodel
import tdi
import lisabeta.lisa.ldctools as ldctools
# Plotting modules
import matplotlib.pyplot as plt
import time


def rms_error(x, x_ref,  relative=True):

    rms = np.sqrt(np.sum(np.abs(x - x_ref) ** 2))

    if relative:
        rms = rms / np.sqrt(np.sum(np.abs(x_ref) ** 2))

    return rms


class TestLikelihood(unittest.TestCase):

    def test_likelihood_with_gaps(self, config_file="../configs/config_ldc_single_gap.ini", plot=True):

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
        psd_cls = None
        # One-sided PSD
        sa = tdi.noisepsd_AE(freq_d[inds], model='Proposal', includewd=None)

        data_cls = None

        # Instantiate likelihood class
        ll_cls = likelihoodmodel.LogLike([mask * ad, mask * ed], sa, inds, tobs, del_t * q,
                                         normalized=config['Model'].getboolean('normalized'),
                                         t_offset=t_offset, channels=[1, 2],
                                         scale=config["InputData"].getfloat("rescale"),
                                         model_cls=data_cls, psd_cls=psd_cls,
                                         wd=wd,
                                         wd_full=wd_full)
        # # Waveform generation in the Frequency domain
        # t1 = time.time()
        # if config['Model'].getboolean('reduced'):
        #     i_sampl_intr = [0, 1, 2, 3, 4, 7, 8]
        #     aft, eft = ll_cls.compute_signal_reduced(p_sampl[i_sampl_intr])
        # else:
        #     aft, eft = ll_cls.compute_signal(p_sampl)
        # t2 = time.time()
        # print('Waveform Calculated in ' + str(t2 - t1) + ' seconds.')

        # Get the windowed discrete Fourier transform used in the likelihood
        a_df_like, e_df_like = ll_cls.data_dft
        # Compare to the DFT of the complete data set
        a_df = fft(ad * wd_full) * del_t * q * wd_full.shape[0] / np.sum(wd_full)
        e_df = fft(ed * wd_full) * del_t * q * wd_full.shape[0] / np.sum(wd_full)

        # Plotting
        if plot:
            from plottools import presets
            presets.plotconfig(ctype='time', lbsize=16, lgsize=14)

            # Time plot
            fig0, ax0 = plt.subplots(nrows=1)
            ax0.semilogx(tm, ad, 'k', label='Full TDI a_mat data')
            ax0.semilogx(tm, wd * np.max(ad), 'r', label='Mask')
            ax0.semilogx(tm, mask * np.max(ad), 'gray', label='Masked data')

            # Frequency plot
            fig1, ax1 = plt.subplots(nrows=2, sharex=True, sharey=True)
            ax1[0].semilogx(freq_d[inds], np.real(a_df[inds]), label='Data DFT')
            ax1[0].semilogx(freq_d[inds], np.real(a_df_like), '--', label='Re-generated')
            ax1[0].set_ylabel("Fractional frequency", fontsize=16)
            ax1[0].legend(loc='upper left')
            ax1[1].semilogx(freq_d[inds], np.imag(a_df[inds]), label='Data DFT')
            ax1[1].semilogx(freq_d[inds], np.imag(a_df_like), '--', label='Re-generated')
            ax1[1].set_xlabel("Frequency [Hz]", fontsize=16)
            ax1[1].set_ylabel("Fractional frequency", fontsize=16)
            ax1[1].legend(loc='upper left')
            for i in range(len(ax1)):
                ax1[i].axvline(x=f1, ymin=0, ymax=np.max(np.real(a_df[inds])), color='r', linestyle='--')
                ax1[i].axvline(x=f2, ymin=0, ymax=np.max(np.real(a_df[inds])), color='r', linestyle='--')
            plt.show()

        rms = rms_error(a_df_like, a_df[inds], relative=True)

        print("Cumulative relative error is " + str(rms))
        self.assertLess(rms, 5e-2, "Cumulative relative error sould be less than 0.05 (5 percents)")


if __name__ == '__main__':

    unittest.main()
