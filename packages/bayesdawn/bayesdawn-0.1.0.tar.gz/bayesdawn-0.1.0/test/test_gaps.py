# Standard useful python module
import numpy as np
import time
from scipy import linalg
# LDC modules
import tdi
# MC Sampler modules
import dynesty
from bayesdawn.utils import physics
from bayesdawn.waveforms import lisaresp
from bayesdawn import likelihoodmodel


if __name__ == '__main__':

    # Standard modules
    from scipy import signal
    import datetime
    import pickle
    from bayesdawn import psdmodel, datamodel
    from bayesdawn.utils import loadings, preprocess
    # For parallel computing
    # from multiprocessing import Pool, Queue
    # LDC tools
    import lisabeta.lisa.ldctools as ldctools
    # Plotting modules
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    # FTT modules
    import fftwisdom
    import pyfftw
    pyfftw.interfaces.cache.enable()
    from pyfftw.interfaces.numpy_fft import fft, ifft
    import configparser
    from optparse import OptionParser
    from bayesdawn.gaps import gapgenerator

    # ==================================================================================================================
    # Load configuration file
    # ==================================================================================================================
    parser = OptionParser(usage="usage: %prog [options] YYY.txt", version="10.28.2018, Quentin Baghi")
    (options, args) = parser.parse_args()
    if not args:
        config_file = "../configs/config_ldc_ptemcee.ini"
    else:
        config_file = args[0]
    # ==================================================================================================================
    config = configparser.ConfigParser()
    config.read(config_file)
    fftwisdom.load_wisdom()

    # ==================================================================================================================
    # Unpacking the hdf5 file and getting data and source parameters
    # ==================================================================================================================
    p, td = loadings.load_ldc_data(config["InputData"]["FilePath"])
    noiseless_path = config["InputData"]["FilePath"][0:-5] + "_noiseless" + config["InputData"]["FilePath"][-5:]
    _, td_noiseless = loadings.load_ldc_data(noiseless_path)
    del_t = float(p.get("Cadence"))
    tobs = float(p.get("ObservationDuration"))

    # ==================================================================================================================
    # Get the parameters
    # ==================================================================================================================
    # Get parameters as an array from the hdf5 structure (table)
    p_sampl = physics.get_params(p, sampling=True)
    tc = p_sampl[2]

    # ==================================================================================================================
    # Pre-processing data: anti-aliasing and filtering
    # ==================================================================================================================
    if config['InputData'].getboolean('trim'):
        i1 = np.int(config["InputData"].getfloat("StartTime") / del_t)
        i2 = np.int(config["InputData"].getfloat("EndTime") / del_t)
        t_offset = 52.657 + config["InputData"].getfloat("StartTime")
        tobs = (i2 - i1) * del_t
    else:
        i1 = 0
        i2 = np.int(td.shape[0])
        t_offset = 52.657

    tm, Xd, Yd, Zd, q = preprocess.preprocess_all(config, td, i1, i2, scale=config["InputData"].getfloat("rescale"))
    _, Xd_noiseless, Yd_noiseless, Zd_noiseless, q = preprocess.preprocess_all(config, td_noiseless, i1, i2,
                                                                           scale=config["InputData"].getfloat("rescale"))
    # Convert Michelson TDI to a_mat, E, T
    Ad, Ed, Td = ldctools.convert_XYZ_to_AET(Xd, Yd, Zd)
    Ad_noiseless, Ed_noiseless, Td_noiseless = ldctools.convert_XYZ_to_AET(Xd_noiseless, Yd_noiseless, Zd_noiseless)

    # ==================================================================================================================
    # Introducing gaps if requested
    # ==================================================================================================================
    # Set seed
    np.random.seed(int(config["Sampler"]["RandomSeed"]))

    if config["TimeWindowing"]["GapType"] == 'single':
        nd = [np.int(config["TimeWindowing"].getfloat("GapStartTime") / del_t)]
        nf = [np.int(config["TimeWindowing"].getfloat("GapEndTime") / del_t)]

    else:
        nd, nf = gapgenerator.generategaps(tm.shape[0], 1/del_t, config["TimeWindowing"].getint("GapNumber"),
                                           config["TimeWindowing"].getfloat("GapDuration"),
                                           gap_type=config["TimeWindowing"]["GapType"],
                                           f_gaps=config["TimeWindowing"].getfloat("GapFrequency"),
                                           wind_type='rect', std_loc=0, std_dur=0)

    n_data = tm.shape[0]

    # Mask with gaps
    wd_gaps = gapgenerator.windowing(nd, nf, n_data, window=config["TimeWindowing"]["WindowType"],
                                     n_wind=config["TimeWindowing"].getint("decaynumbergaps"))
    # Binary mask
    mask = gapgenerator.windowing(nd, nf, tm.shape[0], window='rect')
    # Mask with first segment of data only
    wd1 = np.zeros(n_data)
    wd1[0:nd[0]] = wd_gaps[0:nd[0]]
    wd = signal.tukey(Xd.shape[0], alpha=(config["InputData"].getfloat("EndTime") - tc) / tobs, sym=True)
    # wd = signal.tukey(Xd.shape[0], alpha=config["TimeWindowing"].getint("WindowDecay") / n_data, sym=True)
    # Saving mask
    # mask_file = "../data/mask_" + config["TimeWindowing"]["GapType"]
    # np.save(mask_file, mask)

    # ==================================================================================================================
    # Now we get extract the data and transform it to frequency domain
    # ==================================================================================================================
    # Frequencies
    freq = np.fft.fftfreq(len(tm), del_t * q)
    freqD = freq[:int(len(freq) / 2)]
    df = freqD[1] - freqD[0]

    # Without gaps
    resc = 1 # Xd.shape[0]/np.sum(wd)
    a_df = fft(wd * Ad) * del_t * q * resc
    e_df = fft(wd * Ed) * del_t * q * resc
    t_df = fft(wd * Ed) * del_t * q * resc

    # With gaps
    resc_gaps = 1 # Xd.shape[0]/np.sum(wd_gaps)
    a_df_gaps = fft(wd_gaps * Ad) * del_t * q * resc_gaps
    e_df_gaps = fft(wd_gaps * Ed) * del_t * q * resc_gaps
    t_df_gaps = fft(wd_gaps * Td) * del_t * q * resc_gaps

    # Noiseless
    a_df_noiseless = fft(wd * Ad_noiseless) * del_t * q * resc
    e_df_noiseless = fft(wd * Ed_noiseless) * del_t * q * resc
    t_df_noiseless = fft(wd * Td_noiseless) * del_t * q * resc

    a_df_gaps_noiseless = fft(wd_gaps * Ad_noiseless) * del_t * q * resc
    e_df_gaps_noiseless = fft(wd_gaps * Ed_noiseless) * del_t * q * resc
    t_df_gaps_noiseless = fft(wd_gaps * Td_noiseless) * del_t * q * resc

    # ==================================================================================================================
    # PSD estimation
    # ==================================================================================================================
    psd_cls = psdmodel.PSDSpline(n_data, 1 / del_t, n_knots=30, d=2, fmin=1 / (del_t * n_data) * 1.05, fmax=1 / (del_t * 2))
    psd_cls.estimate(Ad)
    sa = psd_cls.calculate(n_data)

    # ==================================================================================================================
    # Waveform regeneration
    # ==================================================================================================================
    # Restrict the frequency band to high SNR region
    inds = np.where((float(config['Model']['MinimumFrequency']) <= freq) & (freq <= float(config['Model']['MaximumFrequency'])))[0]
    # Consider only a_mat and E TDI data
    dataAE = [a_df[inds], e_df[inds]]

    ll_cls = likelihoodmodel.LogLike([Ad, Ed, Td], sa[inds], freqD[inds], tobs, del_t * q,
                                     normalized=config['Model'].getboolean('normalized'),
                                     t_offset=t_offset, channels=[1, 2, 3],
                                     scale=config["InputData"].getfloat("rescale"))

    t1 = time.time()
    # params = physics.like_to_waveform(p_sampl)
    # aft, eft, tft = lisaresp.lisabeta_template(params, freq[inds], tobs, tref=0, t_offset=t_offset, channels=[1, 2, 3])
    aft, eft, tft = ll_cls.compute_signal(p_sampl)
    t2 = time.time()
    print("=================================================================")
    print("LISABeta template computation time: " + str(t2 - t1))
    # Compute the waveform in the time domain
    aft_time = ll_cls.frequency_to_time(aft)

    # ==================================================================================================================
    # Creation of data class instance
    # ==================================================================================================================

    if config['Imputation'].getboolean('imputation'):
        dat_cls = datamodel.GaussianStationaryProcess(mask * Ad, mask, method=config["Imputation"]['method'],
                                                  na=150, nb=150,
                                                  p=config["Imputation"].getint("precondOrder"),
                                                  tol=config["Imputation"].getfloat("tolerance"),
                                                  n_it_max=config["Imputation"].getint("maximumIterationNumber"))


        ad_rec = dat_cls.impute(aft_time, psd_cls)
        a_df_rec = fft(wd * ad_rec) * del_t * q * resc

    else:
        a_df_rec = None


    # ==================================================================================================================
    # Spectrum distortion due to data gaps
    # ==================================================================================================================
    aft_gaps_full = np.zeros(n_data, dtype=aft.dtype)
    aft_gaps_full[inds] = aft
    aft_gaps_full[n_data - inds] = np.conj(aft)
    wd_gaps_fft = fft(wd_gaps)
    aft_gaps = ifft(fft(aft_gaps_full) * fft(wd_gaps_fft))[inds] / n_data

    # # PSD distortion
    # p_gaps = np.abs(wd_gaps_fft)**2 / n_data
    # sa_fft = fft(sa)
    # sa_gaps = np.real(ifft(sa_fft * fft(p_gaps)))/ n_data
    #
    # n_tau = 50
    # fs = 1 / del_t
    # snr_full = np.zeros(n_tau)
    # snr_gap = np.zeros(n_tau)
    # n_decays = np.linspace(10, 10000, n_tau).astype(np.int)
    # # PSD distortion as a function of the window decay time
    # print("Start computing SNR...")
    # for i in range(n_tau):
    #     wd_g = gapgenerator.windowing(nd, nf, tm.shape[0], window="modified_hann", n_wind=n_decays[i])
    #     # k2 = np.sum(wd_g ** 2)
    #     # k2_g = np.sum(wd_g ** 2)
    #     p_g = np.abs(fft(wd_g)) ** 2 / n_data
    #     sa_g = np.real(ifft(sa_fft * fft(p_g))) / n_data
    #     aft_gaps_time = fft(aft_time * wd_g)
    #     # snr[i] = 4.0 * df * np.abs(aft)**2 / (sa_g * 2 / fs)
    #     snr_gap[i] = 4.0 * df * np.sum(np.abs(aft_gaps_time[inds]) ** 2 / (2 * sa_g[inds]))
    #
    #     wd_full = gapgenerator.modified_hann(tm.shape[0], n_wind=n_decays[i])
    #     p_full = np.abs(fft(wd_full)) ** 2 / n_data
    #     sa_wind = np.real(ifft(sa_fft * fft(p_full))) / n_data
    #     aft_full_time = fft(aft_time * wd_full)
    #     snr_full[i] = 4.0 * df * np.sum(np.abs(aft_full_time[inds]) ** 2 / (2 * sa_wind[inds]))
    #
    # print("SNR computed.")
    # ==================================================================================================================
    # Plotting
    # ==================================================================================================================
    from plottools import presets
    presets.plotconfig(ctype='frequency', lbsize=16, lgsize=14)

    # Restrict the frequency band to high SNR region
    inds = np.where((float(config['Model']['MinimumFrequency']) <= freqD)
                    & (freqD <= float(config['Model']['MaximumFrequency'])))[0]

    # # Frequency plot
    # fig1, ax1 = plt.subplots(nrows=2)
    # ax1[0].loglog(freq[inds], np.abs(ADf[inds]), 'k', label='Complete data')
    # ax1[0].loglog(freq[inds], np.abs(ADf_gaps[inds]), 'gray', label='Gapped data')
    # # ax1[0].loglog(freq[inds], np.abs(aft_gaps), 'b', label='Template model')
    # plt.legend()
    # ax1[1].semilogx(freq[inds], np.angle(ADf[inds]), 'k')
    # ax1[1].semilogx(freq[inds], np.angle(ADf_gaps[inds]), 'gray')
    # ax1[1].loglog(freq[inds], np.angle(aft_gaps), 'b', label='Template model')
    # plt.show()

    # fig2, ax2 = plt.subplots(nrows=1)
    # ax2.loglog(freq[inds], np.abs(ADf1[inds]), 'gray', label='First data segment only')
    # ax2.loglog(freq[inds], np.abs(aft1), 'blue', label='Template model')
    # plt.legend()
    # plt.show()
    scale = config["InputData"].getfloat("rescale")
    f1, f2 = physics.find_distorted_interval(mask, p_sampl, t_offset, del_t, margin=0.5)

    fig1, ax1 = plt.subplots(nrows=1)
    ax1.loglog(freq[inds], scale * np.abs(a_df_noiseless[inds]) / np.sum(wd), 'k',
               label='Complete data')
    ax1.loglog(freq[inds], scale * np.abs(a_df_gaps_noiseless[inds]) / np.sum(wd_gaps),
               'gray', label='Gapped data')
    ax1.axvline(x=f1, ymin=0, ymax=scale * np.max(np.abs(a_df_noiseless[inds])) / np.sum(wd), color='r', linestyle='--')
    ax1.axvline(x=f2, ymin=0, ymax=scale * np.max(np.abs(a_df_noiseless[inds])) / np.sum(wd), color='r', linestyle='--')
    ax1.set_xlabel("Frequency [Hz]")
    ax1.set_ylabel("Fractional frequency")
    ax1.legend()

    fig3, ax3 = plt.subplots(nrows=1)
    ax3.loglog(freq[inds], scale * np.abs(a_df[inds]) / np.sqrt(del_t * np.sum(wd ** 2)), 'k', label='Complete data')
    ax3.loglog(freq[inds], scale * np.abs(a_df_gaps[inds]) / np.sqrt(del_t * np.sum(wd_gaps ** 2)), 'gray', label='Gapped data')
    if config['Imputation'].getboolean('imputation'):
        ax3.loglog(freq[inds], scale * np.abs(a_df_rec[inds]) / np.sqrt(del_t * np.sum(wd ** 2)), 'blue', label='Imputed data')
        ax3.loglog(freq[inds], scale * np.sqrt(sa[inds]*del_t), 'r', label='PSD estimate')
    ax3.set_xlabel("Frequency [Hz]")
    ax3.set_ylabel("Fractional frequency")
    ax3.legend()
    # ax3.loglog(freq[inds], np.sqrt(sa_gaps[inds] * del_t), 'r--', label='Distorted PSD')

    # # SNR plot
    # fig4, ax4 = plt.subplots(nrows=1, sharex=True, sharey=True)
    # ax4.plot(n_decays, snr, 'k')
    # plt.show()

    presets.plotconfig(ctype='time', lbsize=16, lgsize=14)
    # Time plot
    fig0, ax0 = plt.subplots(nrows=1, sharex=True, sharey=True)
    ax0.plot(tm, scale * Xd_noiseless, 'k', label='Signal')
    # ax0.semilogx(tm, scale * wd * np.max(np.abs(Xd_noiseless)), 'r', label='Data')
    ax0.semilogx(tm, scale * wd_gaps * np.max(np.abs(Xd_noiseless)), 'r', label='Mask')
    ax0.set_xlabel("Time [s]")
    ax0.set_ylabel("Fractional frequency")
    ax0.legend()
    plt.show()
