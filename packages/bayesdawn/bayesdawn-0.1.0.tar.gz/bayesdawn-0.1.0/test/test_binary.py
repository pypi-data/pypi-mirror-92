import unittest
from matplotlib import pyplot as plt
import time
from plottools import presets
import numpy as np
import loadsourceconfig
from bayesdawn.waveforms import lisaresp, wavefuncs, coeffs
from alisa import gwsources
import pyFLR
# FTT modules
import fftwisdom
import pyfftw
from pyfftw.interfaces.numpy_fft import fft
import h5py
import configparser


def compare_plots(x_list, y_list_1, y_list_2,
                  xlabel='Frequency', ylabel='FFT',
                  label_1='Measurement',
                  label_2='FD model',
                  titles=['Channel 1', 'Channel 2', 'Channel 3']):

    presets.plotconfig(ctype='frequency', lbsize=16, lgsize=14)
    fig0, ax = plt.subplots(nrows=3, ncols=2)
    for i in range(len(x_list)):
        ax[i, 0].plot(x_list[i], np.abs(y_list_1[i]), color='k',
                      linestyle='solid', label=label_1)
        ax[i, 0].plot(x_list[i], np.abs(y_list_2[i]), color='r',
                      linestyle='dotted',
                      label=label_2)
        ax[i, 0].set_ylabel(ylabel + "Amplitude")
        ax[i, 0].set_xscale("log")
        ax[i, 1].plot(x_list[i], np.angle(y_list_1[i]), color='k',
                      linestyle='solid', label=label_1)
        ax[i, 1].plot(x_list[i], np.angle(y_list_2[i]), color='r',
                      linestyle='dotted',
                      label=label_2)
        ax[i, 1].set_ylabel(ylabel + "Phase")
        ax[i, 1].set_xscale("log")
        ax[i, 1].set_xlabel(xlabel)
        ax[i, 1].legend(loc=1)

    plt.show()


class TestUCBWaveform(unittest.TestCase):

    def test_compute_signal_freq(self, display=True):

        # Retrieve source configuration
        # ======================================================================
        conf_file_path = '/Users/qbaghi/Codes/data/simulations/phasemeters/'
        # simu_file_name = '2020-03-10_13h59-56_signal_1month_HMCnc_fs=200mHz_constant_arms_rotating_simu.hdf5'
        input_prefix = '2020-03-30_15h13-59_signal_1month_HMCnc_fs=1Hz_equal_arms'
        # Get other information about the simulation
        config_simu = configparser.ConfigParser()
        config_simu.read(conf_file_path + input_prefix + '_config.ini')
        # Source configuration
        source_config_path = config_simu["Input"].get("SourceConfigPath")
        conf = loadsourceconfig.loadconfig(source_config_path)
        # Get source parameters
        param_dic = gwsources.ldc2dic(conf.p)

        # Get the simulated signal in single-links
        # ======================================================================
        print("Loading data...")
        fh5 = h5py.File(conf_file_path + input_prefix + "_simu.hdf5", 'r')
        pm_sig = fh5["signal/pm"][()]
        pm_prime_sig = fh5["signal/pm_prime"][()]
        t_val = fh5["signal/time"][()]
        fh5.close()
        # pm_sig = np.load(simu_file_path + 'pm.npy')
        # pm_prime_sig = np.load(simu_file_path + 'pm_prime.npy')
        print("Data loaded.")

        # ==========================================================================
        nc = lisaresp.optimal_order(param_dic["theta"], param_dic["f_0"])
        n = pm_sig.shape[0]
        fs = 1 / (t_val[1] - t_val[0])
        f = np.fft.fftfreq(n) * fs
        tobs = n / fs
        conf.p.addPar("ObservationDuration", tobs, "Second")
        conf.p.addPar("Cadence", 1 / fs, "Second")

        f1 = param_dic["f_0"] - 3e-5
        f2 = param_dic["f_0"] + 3e-5
        inds = np.where((f >= f1) & (f <= f2))[0]

        waveform = lisaresp.UCBWaveform(wavefuncs.v_func_gb,
                                        phi_rot=0,
                                        armlength=2.5e9,
                                        nc=nc)
        params = np.array([param_dic["A"], param_dic["incl"], param_dic["phi_0"],
                           param_dic["psi"], param_dic["theta"], param_dic["phi"],
                           param_dic["f_0"], param_dic["f_dot"]])

        # Compute the signal for each arm
        channel = 'phasemeters'

        t1 = time.time()
        s1, s2, s3 = waveform.compute_signal_freq(f[inds],
                                                  params,
                                                  1/param_dic["fs"],
                                                  tobs,
                                                  channel=channel)
        t2 = time.time()
        print("Waveform computed in " + str(t2 - t1) + " second.")

        # t1 = time.time()
        # fr, xf, yf, zf = clht.waveforms_mldc.GenerateFastGB(conf.p, FD=True,
        #                                                     oversample=4,
        #                                                     algorithm='ldc')
        # t2 = time.time()
        # print("LDC waveform computed in " + str(t2 - t1) + " second.")

        # # Simulate signal in single-links using medium-fast time-domain code
        # # ==========================================================================
        # fastresp = pyFLR.fastResponse(alwaves.Phi_GB_func, pyFLR.beta_GB,
        #                               phi_rot=conf.phi_rot, low_freq=True)
        # tm_fast, pm_fast, pm_prime_fast = fastresp.evaluate_pm(conf.p)

        # Plot one phasemeter signal
        # ==========================================================================
        print("Computing FFT...")
        pm_sig_1 = fft(pm_sig[:, 0])
        pm_sig_2 = fft(pm_sig[:, 1])
        pm_sig_3 = fft(pm_sig[:, 2])
        pm_p_sig_1 = fft(pm_prime_sig[:, 0])
        pm_p_sig_2 = fft(pm_prime_sig[:, 1])
        pm_p_sig_3 = fft(pm_prime_sig[:, 2])
        # pm_ref_1 = fft(pm_fast[:, 0])
        # pm_ref_2 = fft(pm_fast[:, 1])
        # pm_ref_3 = fft(pm_fast[:, 2])
        fftwisdom.save_wisdom()
        # pm_sig_fft = fft(pm_sig, axis=0)
        print("FFT computed.")
        mod_err_1 = np.mean(np.abs(pm_sig_1[inds] - s1)/np.abs(pm_sig_1[inds]))
        # ang_err_1 = np.mean(np.angle(pm_sig_1[inds] - s1)/np.angle(pm_sig_1[inds]))
        print("Relative error on s1: " + str(mod_err_1)
              + " should be less than 5%.")
        x_list = [f[inds], f[inds], f[inds]]
        # Each phasemeter pm_{i} measure h_{i+2} 3, 1, 2
        y_list_1 = [pm_sig_1[inds], pm_sig_2[inds], pm_sig_3[inds]]
        y_list_2 = [s1, s2, s3]
        compare_plots(x_list, y_list_1, y_list_2)
        # Each phasemeter pm_prime_{i} measure h_{i+1} 2, 3, 1
        y_list_1p = [pm_p_sig_1[inds], pm_p_sig_2[inds], pm_p_sig_3[inds]]
        y_list_2p = [s3, s1, s2]
        compare_plots(x_list, y_list_1p, y_list_2p)
        # # Compare with another way of calculating
        # y_list_1 = [pm_sig_1[inds], pm_sig_2[inds], pm_sig_3[inds]]
        # y_list_2 = [pm_ref_1[inds], pm_ref_2[inds], pm_ref_3[inds]]
        # compare_plots(x_list, y_list_1, y_list_2)

        self.assertTrue(mod_err_1 < 0.05)


if __name__ == '__main__':

    pyfftw.interfaces.cache.enable()
    fftwisdom.load_wisdom()
    # unittest.main()

    # Retrieve source configuration
    conf_file_path = '/Users/qbaghi/Codes/data/simulations/phasemeters/'
    input_prefix = '2020-04-04_12h07-34_signal_1month_HMCnc_fs=200mHz_equal_arms'
    # Get other information about the simulation
    config_simu = configparser.ConfigParser()
    config_simu.read(conf_file_path + input_prefix + '_config.ini')
    # Source configuration
    source_config_path = config_simu["Input"].get("SourceConfigPath")
    conf = loadsourceconfig.loadconfig(source_config_path)
    # Get source parameters
    param_dic = gwsources.ldc2dic(conf.p)
    # Signal data path
    fh5 = h5py.File(conf_file_path + input_prefix + "_simu.hdf5", 'r')
    # Load signal data
    pm_sig = fh5["signal/pm"][()]
    pm_prime_sig = fh5["signal/pm_prime"][()]
    fh5.close()

    n_data = pm_sig.shape[0]
    fs = config_simu["Parameters"].getfloat("OutputSamplingFrequency")
    tobs = n_data / fs
    f = np.fft.fftfreq(n_data) * fs
    nc = lisaresp.optimal_order(param_dic["theta"], param_dic["f_0"])
    ts = 1 / fs
    # Update Observation duration and sampling cadence
    conf.p.addPar("ObservationDuration", tobs, "Second")
    conf.p.addPar("Cadence", ts, "Second")
    # Restrict bandwidth for waveform compuation
    f1 = param_dic["f_0"] - 5e-5
    f2 = param_dic["f_0"] + 5e-5
    inds = np.where((f >= f1) & (f <= f2))[0]

    waveform_full = lisaresp.UCBWaveformFull(wavefuncs.v_func_gb, 1/fs, tobs,
                                             phi_rot=0, armlength=2.5e9,
                                             nc=2**9, arm_list=None, e=0)

    params = np.array([param_dic["A"], param_dic["incl"], param_dic["phi_0"],
                       param_dic["psi"], param_dic["theta"], param_dic["phi"],
                       param_dic["f_0"], param_dic["f_dot"]])
    channel="phasemeters"

    # --------------------------------------------------------------------------
    # Extract physical parameters
    a0, incl, phi_0, psi, theta, phi, f_0, f_dot = params
    # Compute design matrices
    param_intr = np.array([theta, phi, f_0, f_dot])

    # # Compute optimal number of coefficients if not provided
    # # self.nc = self.optimal_sample_number(theta, f_0, f_dot)
    # # Compute slow part of nc x 2 design matrices in time domain
    # index_list = [3, 1, 2]
    # a_slow_3 = [waveform_full.compute_slow_part(theta, phi, f_0, 3,
    #                                             channel="phasemeters")]
    # # Compute its FFC to get Fourier series coefficients
    # # (lisf ot nc x 2 matrices)
    # cn = fft(a_slow_3, axis=0)
    # # Compute corresponding frequency vector
    # f_vect = np.fft.fftfreq(waveform_full.nc) / waveform_full.tobs
    # ef = np.exp(2j * np.pi * f_vect * waveform_full.t_sample)
    #
    # a_slow_3_approx = np.array([cn[:, 0] * ef])
