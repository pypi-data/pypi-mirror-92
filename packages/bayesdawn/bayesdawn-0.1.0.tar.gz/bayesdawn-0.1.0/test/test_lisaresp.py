import unittest
import numpy as np

# FTT modules
import fftwisdom
import pyfftw
pyfftw.interfaces.cache.enable()
from pyfftw.interfaces.numpy_fft import fft, ifft
import configparser
from bayesdawn.utils import loadings, physics, preprocess
from bayesdawn import likelihoodmodel
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


def prepare_data(config):

    fftwisdom.load_wisdom()

    # Unpacking the hdf5 file and getting data and source parameters
    p, td = loadings.load_ldc_data(config["InputData"]["FilePath"])

    # Pre-processing data: anti-aliasing and filtering
    tm, xd, yd, zd, q, t_offset, tobs, del_t, p_sampl = preprocess.preprocess_ldc_data(p, td, config)

    # Frequencies
    freq_d = np.fft.fftfreq(len(tm), del_t * q)
    # Restrict the frequency band to high SNR region
    inds = np.where((float(config['Model']['MinimumFrequency']) <= freq_d)
                    & (freq_d <= float(config['Model']['MaximumFrequency'])))[0]
    # Theoretical PSD
    sa = tdi.noisepsd_AE(freq_d[inds], model='Proposal', includewd=None)
    sn = [sa, sa]

    # Convert Michelson TDI to a_mat, E, T (time domain)
    ad, ed, td = ldctools.convert_XYZ_to_AET(xd, yd, zd)

    # Transform to frequency domain
    wd = np.ones(ad.shape[0])
    wd_full = wd[:]
    mask = wd[:]
    # a_df, e_df, t_df = preprocess.time_to_frequency(ad, ed, td, wd, del_t, q, compensate_window=True)

    # Instantiate likelihood class
    ll_cls = likelihoodmodel.LogLike([mask * ad, mask * ed], sn, inds, tobs, del_t * q,
                                     normalized=config['Model'].getboolean('normalized'),
                                     t_offset=t_offset, channels=[1, 2],
                                     scale=config["InputData"].getfloat("rescale"),
                                     model_cls=None, psd_cls=None,
                                     wd=wd,
                                     wd_full=wd_full)

    return ll_cls, tm, ad, ed, td, wd, del_t, q, p_sampl, freq_d, inds


class TestWaveform(unittest.TestCase):

    def test_waveform_freq(self, config_file="../configs/config_test_lisaresp.ini", plot=True):

        config = configparser.ConfigParser()
        config.read(config_file)
        ll_cls, tm, ad, ed, td, wd, del_t, q, p_sampl, freq_d, inds = prepare_data(config)

        a_df, e_df, t_df = preprocess.time_to_frequency(ad, ed, td, wd, del_t, q, compensate_window=True)

        t1 = time.time()
        if config['Model'].getboolean('reduced'):
            i_sampl_intr = [0, 1, 2, 3, 4, 7, 8]
            aft, eft = ll_cls.compute_signal_reduced(p_sampl[i_sampl_intr])
        else:
            aft, eft = ll_cls.compute_signal(p_sampl)
        t2 = time.time()
        print('Waveform Calculated in ' + str(t2 - t1) + ' seconds.')

        rms = rms_error(aft, a_df[inds], relative=True)
        print("Cumulative relative error is " + str(rms))

        self.assertLess(rms, 1e-3, "Cumulative relative error sould be less than 0.02 (2 percents)")

        # Plotting
        if plot:
            from plottools import presets
            presets.plotconfig(ctype='time', lbsize=16, lgsize=14)

            # Frequency plot
            fig1, ax1 = plt.subplots(nrows=2, sharex=True, sharey=True)
            ax1[0].semilogx(freq_d[inds], np.real(a_df[inds]))
            ax1[0].semilogx(freq_d[inds], np.real(aft), '--')
            ax1[0].set_ylabel("Fractional frequency")
            # ax1[0].legend()
            ax1[1].semilogx(freq_d[inds], np.imag(a_df[inds]))
            ax1[1].semilogx(freq_d[inds], np.imag(aft), '--')
            ax1[1].set_xlabel("Frequency [Hz]")
            ax1[1].set_ylabel("Fractional frequency")
            # ax1[1].legend()
            plt.show()

    def test_waveform_time(self, config_file="../configs/config_test_lisaresp.ini", plot=True):

        config = configparser.ConfigParser()
        config.read(config_file)
        fftwisdom.load_wisdom()

        ll_cls, tm, ad, ed, td, wd, del_t, q, p_sampl, freq_d, inds = prepare_data(config)

        t1 = time.time()
        if config['Model'].getboolean('reduced'):
            i_sampl_intr = [0, 1, 2, 3, 4, 7, 8]
            aft, eft = ll_cls.compute_signal_reduced(p_sampl[i_sampl_intr])
        else:
            aft, eft = ll_cls.compute_signal(p_sampl)
        t2 = time.time()
        print('Waveform Calculated in ' + str(t2 - t1) + ' seconds.')

        # Convert to time-domain waveform
        aft_time = ll_cls.frequency_to_time(aft)
        eft_time = ll_cls.frequency_to_time(eft)

        rms = rms_error(aft_time, ad, relative=True)

        if plot:
            # # Time plot
            # fig0, ax0 = plt.subplots(nrows=1, sharex=True, sharey=True)
            # ax0.plot(tm, ad, 'k')
            # ax0.plot(tm, aft_time, 'r')
            # plt.show()

            # Frequency plot
            fig2, ax2 = plt.subplots(nrows=2, sharex=True, sharey=True)
            ax2[0].plot(tm, ad, label='TDI a_mat true signal')
            ax2[0].plot(tm, aft_time, '--', label='TDI a_mat regenerated signal')
            ax2[0].set_ylabel("Fractional frequency")
            # ax1[0].legend()
            ax2[1].plot(tm, ed, label='TDI E true signal')
            ax2[1].plot(tm, eft_time, '--', label='TDI E regenerated signal')
            ax2[1].set_xlabel("Time [s]")
            ax2[1].set_ylabel("Fractional frequency")
            # ax1[1].legend()
            plt.show()

        print("Cumulative relative error is " + str(rms))
        self.assertLess(rms, 1e-2, "Cumulative relative error sould be less than 0.02 (2 percents)")

    def test_reduced_model(self, config_file="../configs/config_test_lisaresp.ini", plot=True):

        config = configparser.ConfigParser()
        config.read(config_file)
        ll_cls, tm, ad, ed, td, wd, del_t, q, p_sampl, freq_d, inds = prepare_data(config)

        a_df, e_df, t_df = preprocess.time_to_frequency(ad, ed, td, wd, del_t,
                                                        q,
                                                        compensate_window=True)

        # # Instantiate likelihood class
        # ll_cls = likelihoodmodel.LogLike([mask * ad, mask * ed], sn, inds, tobs, del_t * q,
        #                                  normalized=config['Model'].getboolean('normalized'),
        #                                  t_offset=t_offset, channels=[1, 2],
        #                                  scale=config["InputData"].getfloat("rescale"),
        #                                  model_cls=None, psd_cls=None,
        #                                  wd=wd,
        #                                  wd_full=wd_full)


        i_sampl_intr = [0, 1, 2, 3, 4, 7, 8]

        # Generate a random parameter
        u = np.random.random(len(p_sampl))
        # par = prior_transform(theta_u, lower_bound, upper_bound)

        t1 = time.time()
        aft_red, eft_red = ll_cls.compute_signal_reduced(p_sampl[i_sampl_intr])
        t2 = time.time()
        print('Waveform Calculated in ' + str(t2 - t1) + ' seconds with reduced model.')
        t1 = time.time()
        aft, eft = ll_cls.compute_signal(p_sampl)
        t2 = time.time()
        print('Waveform Calculated in ' + str(t2 - t1) + ' seconds with full model.')

        rms = rms_error(aft, a_df[inds], relative=True)
        print("Cumulative relative error is " + str(rms))

        self.assertLess(rms, 1e-3, "Cumulative relative error sould be less than 0.02 (2 percents)")

        # Plotting
        if plot:
            from plottools import presets
            presets.plotconfig(ctype='time', lbsize=16, lgsize=14)

            # Frequency plot
            fig1, ax1 = plt.subplots(nrows=2, sharex=True, sharey=True)
            ax1[0].semilogx(freq_d[inds], np.real(aft), '--', label='Full model')
            ax1[0].semilogx(freq_d[inds], np.real(aft_red), 'b')
            ax1[0].set_ylabel("Fractional frequency")
            ax1[0].legend(loc="upper left")
            ax1[1].semilogx(freq_d[inds], np.imag(aft), '--', label='Full model')
            ax1[1].semilogx(freq_d[inds], np.imag(aft_red), 'b', label='Reduced model')
            ax1[1].set_xlabel("Frequency [Hz]")
            ax1[1].set_ylabel("Fractional frequency")
            ax1[1].legend(loc="upper left")
            plt.show()


if __name__ == '__main__':

    # unittest.main()
    tw = TestWaveform()
    tw.test_reduced_model()
