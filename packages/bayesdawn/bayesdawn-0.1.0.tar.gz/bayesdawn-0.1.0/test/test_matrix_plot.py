#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Friday March 06

Test the utils modules for matrix representation

@author: qbaghi

"""
import numpy as np
import pyfftw
from scipy import linalg
from bayesdawn.gaps import gapgenerator, operators
from bayesdawn import psdmodel
from pyfftw.interfaces.numpy_fft import fft, ifft
pyfftw.interfaces.cache.enable()
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LogNorm
from plottools import presets


if __name__ == "__main__":

    # Sampling frequency
    fs = 0.1
    # Set the data size
    n_data = 2**9
    # Set number of gaps
    n_gaps = 20
    # Set gap duration
    t_gaps = 3 / fs
    # Generate the mask
    np.random.seed(1356123)
    nd, nf = gapgenerator.generategaps(n_data, fs, n_gaps, t_gaps,
                                       gap_type='random')
    mask_vect = gapgenerator.windowing(nd, nf, n_data, window='rect')
    inds_obs = np.where(mask_vect == 1)[0]
    inds_mis = np.where(mask_vect == 0)[0]
    # Instantiate observed data mapping  matrix
    w_o_cls = operators.MappingOperator(inds_obs, n_data)
    # Instantiate PSD matrix
    psd_cls = psdmodel.PSDTheoretical(n_data, fs)
    # Build matrix n_o x n
    w_o = w_o_cls.build_matrix(sp=False)
    # Compute PSD values
    s_n = psd_cls.calculate(n_data)[0]
    s_2n = psd_cls.calculate(2 * n_data)[0]
    s_n /= s_n.max()
    s_2n /= s_2n.max()
    # Form corresponding diagonal matrix
    # gamma = np.diag(s_n)
    lamb = np.diag(s_n)
    gamma = linalg.toeplitz(np.real(ifft(s_2n))[0:n_data])
    i_n = np.diag(np.ones(n_data))
    # # Compute Fourier-domain W_o_tilde^{*} of size n_data x N_o
    # w_o_tilde_t = fft(w_o.T, axis=0)
    # # Compute matrix operator
    # c_oo = np.dot(w_o_tilde_t.conj().T, lamb).dot(w_o_tilde_t)
    # c_oo_inv = linalg.pinv(c_oo)
    # p_mat = lamb.dot(w_o_tilde_t).dot(c_oo_inv).dot(w_o_tilde_t.T.conj())
    # mat_plot = np.abs(p_mat)

    # Compute matrix operator
    c_oo = np.dot(w_o, gamma).dot(w_o.T)
    c_oo_inv = linalg.pinv(c_oo)
    p_mat = gamma.dot(w_o.T).dot(c_oo_inv).dot(w_o)
    mat_plot = np.abs(c_oo_inv)

    # # Computation of I + Z^T Sigma Y
    # w_m_cls = operators.MappingOperator(inds_mis, n_data)
    # w_m = w_m_cls.build_matrix(sp=False)
    # sigma_mm = w_m.dot(gamma.dot(w_m.T))
    # mat_plot = np.abs(sigma_mm)
    # y_mat = np.hstack([(i_n - gamma).dot(w_m.T), w_m.T])
    # z_mat = np.hstack([w_m.T, (np.diag(mask_vect) - i_n).dot(np.dot(gamma, w_m.T))])
    #
    # k_mat = np.diag(np.ones(2*len(inds_mis))) + z_mat.T.dot(gamma.dot(y_mat))
    # k_mat_inv = linalg.pinv(k_mat)
    # # mat_plot = np.abs(k_mat_inv)
    # sigma_inv = linalg.pinv(gamma)
    # sigma_bar_inv = sigma_inv[:]
    # sigma_bar_inv -= np.dot(sigma_inv,
    #                         np.dot(y_mat, k_mat_inv)).dot(z_mat.T.dot(sigma_inv))
    # sigma_bar_inv_oo = w_o.dot(np.dot(sigma_bar_inv, w_o.T))

    # Vizualize the result
    mat_plot_masked = operators.mask_matrix(mat_plot, threshold=1e-3)

    presets.plotconfig(ctype='time', lbsize=16, lgsize=14)
    fig, ax = plt.subplots()
    ax.set_title(r"Time-domain operator $\mathbf{\Sigma}_{oo}^{-1}$")
    cs = ax.imshow(mat_plot_masked, norm=LogNorm())
    # cs = ax.imshow(mat_plot)
    cbar = fig.colorbar(cs)
    # cbar.ax.minorticks_off()
    plt.show()


    # fig = plt.figure()
    # ax1 = fig.add_subplot(111)
    # # Bilinear interpolation - this will look blurry
    # # ax1.imshow(np.abs(p_mat), interpolation='bilinear', cmap=cm.Greys_r)
    # # ax2 = fig.add_subplot(122)
    # # 'nearest' interpolation - faithful but blocky
    # ax1.imshow(p_mat_abs, interpolation='nearest', cmap=cm.Greys_r,
    #            norm=LogNorm(vmin=p_mat_abs.min(), vmax=p_mat_abs.max()))
    # plt.show()
