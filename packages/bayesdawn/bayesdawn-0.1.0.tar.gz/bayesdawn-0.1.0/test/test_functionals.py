

if __name__ == '__main__':

    # import alisa
    from alisa import lisaresponse, gwsources, instrument, lisaorbit, lisatdi
    import numpy as np
    from matplotlib import pyplot as plt
    import loadsourceconfig
    from bayesdawn.waveforms import lisaresp, wavefuncs, coeffs
    import pyFLR
    import alwaves

    # Retrieve source configuration
    # ==========================================================================
    conf_file_path = '/Users/qbaghi/Codes/python/gwaves/configs/'
    conf_file_name = 'GBsourceconfig_1year_A=2e-20_monof0=2e-4.txt'
    # Change the parameters according to the config file
    conf = loadsourceconfig.loadconfig(conf_file_path + conf_file_name)
    # Get source parameters
    param_dic = gwsources.ldc2dic(conf.p)

    # Time-domain simulation using aLISA
    # ==========================================================================
    # Source class
    gwsrc = gwsources.UCBSource(param_dic['f_0'],
                                param_dic['f_dot'],
                                param_dic['a_mat'],
                                param_dic['phi_0'],
                                param_dic['theta'],
                                param_dic['phi'],
                                param_dic['psi'],
                                param_dic['incl'],
                                name='UCB')
    ts = conf.p.get("Cadence")
    tobs = conf.p.get("ObservationDuration")
    instr = instrument.LISAInstrument(tobs=tobs, fs=1/ts)
    # Definition of LISA orbit
    orb = lisaorbit.LISAorbit(phi_rot=conf.Phi_rot)
    # Definition of TDI algorithm
    tdint = lisatdi.LIDATdi(generation='1st')
    # Instanciation of LISA response
    lr = lisaresponse.LISAResponse(instr, orb, tdint)
    # Construct orbit quantities
    lr.orbit.build_orbital_phase(lr.t)
    lr.orbit.build_orbital_phase_deriv(lr.t)
    lr.orbit.build_barycenter_pos(lr.t)
    # Compute list of unit vectors along each arm direction n_i(t)
    # (and their time derivatives)
    n_vect = [lr.build_arm_vect(i, deriv=0) for i in range(1, 4)]
    i = 1
    # Modulation functions
    chi_plus_func, chi_cros_func = lr.build_projection_functions(gwsrc,
                                                                 n_vect[i-1],
                                                                 deriv=0)
    print("Forming time vector...")
    t_val = instr.compute_time_vector()
    chi_plus_call = lisaresponse.sympy2func(chi_plus_func, usedlib="numpy")
    chi_cros_call = lisaresponse.sympy2func(chi_cros_func, usedlib="numpy")
    chi_plus, chi_cros = chi_plus_call(t_val), chi_cros_call(t_val)

    # Time-domain simulation of modulation functions by bayesdawn
    # ==========================================================================
    coeff_p, coeff_c = coeffs.xi_coeffs(param_dic['theta'], param_dic['phi'],
                                        conf.Phi_rot, i)
    # Orbital phase
    phi_t = lisaresponse.sympy2func(lr.orbit.phi_T, usedlib="numpy")

    # Matrix of harmonics
    mat_a = np.vstack([np.cos(k * phi_t(t_val)) for k in range(5)]).T
    mat_b = np.vstack([np.sin(k * phi_t(t_val)) for k in range(5)]).T
    mat = np.hstack([mat_a, mat_b])

    chi_plus_fast = np.dot(mat, coeff_p)
    chi_cros_fast = np.dot(mat, coeff_c)

    # ==========================================================================
    # Generate the same modulation functions with fast time-domain code
    # ==========================================================================
    # fastresp = pyFLR.fastResponse(alwaves.Phi_GB_func, pyFLR.beta_GB,
    #                               phi_rot=conf.phi_rot, low_freq=True)
    phi_i = np.pi / 3 * (2 * i + 1) - conf.Phi_rot
    chi_plus_flr, chi_cros_flr = pyFLR.projection_functional(param_dic['theta'],
                                                             param_dic['phi'],
                                                             phi_t(t_val),
                                                             phi_i)

    err_plus = np.mean(np.abs(chi_plus - chi_plus_fast))
    err_cros = np.mean(np.abs(chi_cros - chi_cros_fast))

    print("Error on xi+: " + str(err_plus) + " should be less than 1e-14.")
    print("Error on xix: " + str(err_cros) + " should be less than 1e-14.")

    # Plot and compare
    # ==========================================================================
    fig, ax = plt.subplots(nrows=2)
    ax[0].plot(t_val, chi_plus, 'k', label="aLISA")
    ax[0].plot(t_val, chi_plus_flr, 'b--', label="pyFLR")
    ax[0].plot(t_val, chi_plus_fast, 'r:', label="Bayesdawn")
    ax[0].legend(loc='upper left')
    ax[1].plot(t_val, chi_cros, 'k', label="aLISA")
    ax[1].plot(t_val, chi_cros_flr, 'b--', label="pyFLR")
    ax[1].plot(t_val, chi_cros_fast, 'r:', label="Fast")
    ax[1].legend(loc='upper left')
    plt.show()
