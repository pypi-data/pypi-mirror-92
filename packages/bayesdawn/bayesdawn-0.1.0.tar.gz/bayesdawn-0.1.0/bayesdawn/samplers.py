# -*- coding: utf-8 -*-
# Author: Quentin Baghi 2017
# This code implements simple Metropolis-Hastings MCMC

import numpy as np
from scipy import linalg as linalg
import copy
from functools import reduce
import ptemcee
import h5py
import pickle
# import tables
try:
    import dynesty
    from dynesty import NestedSampler, DynamicNestedSampler
    from dynesty.dynamicsampler import stopping_function, weight_function
    import pandas as pd
    dynesty_on = True
except:
    print("dynesty does not seem to be installed. Proceed without it.")
    dynesty_on = False


def prior_transform(theta_u, lower_bound, upper_bound):

    # order in theta
     # 0   1   2   3     4      5     6  7    8    9    10
    # [Mc, q, tc, chi1, chi2, logDL, ci, sb, lam, psi, phi0]
    theta = lower_bound + (upper_bound - lower_bound) * theta_u

    return theta


def clipcov(X, nit = 3, n_sig = 5):
    """

    Parameters
    ----------
    sampdat : numpy array
        matrix of sampled data, size N_samples x ndim

    """


    X_clip = X[:]
    cov = np.cov(X_clip.T)

    for i in range(nit):

        dX = X_clip - np.mean(X_clip,axis=0)

        inds_tuple = [np.where( np.abs(dX[:,k]) <= n_sig * np.sqrt(cov[k,k]) )[0] 
                      for k in range(X.shape[1])]

        inds = reduce(np.intersect1d, inds_tuple)

        X_clip = X_clip[inds,:]

        cov = np.cov(X_clip.T)

    return cov,X_clip


def logprob(x,distrib_name,pars,constant = False):
    """

    Any distribution


    Parameters
    ----------
    x : scalar or array_like
        random variable value
    distrib_name : string
        name of the distribution
    args : tuple
        parameters giving central localization and scale



    """

    if distrib_name=='symbeta':

        # here we restrict ourselves to the symmetric beta distribution
        # with mode at 1/2
        a = pars[0]
        b = pars[1]

        alpha = 2
        beta = 2

        if np.shape(x)==():

            if (x>=a) & (x<=b):
                out = np.log((x-a)**(alpha-1)*(b-x)**(beta-1)/(b-a)**(alpha+beta-1))
            else:
                out = - np.inf

        else:
            out = np.zeros(len(x))
            inds = np.where((x>=a) & (x<=b))[0]
            out[inds] = np.log((x[inds]-a)**(alpha-1)*(b-x[inds])**(beta-1)/(b-a)**(alpha+beta-1))
            out[(x<a) | (x>b)] = - np.inf

    elif distrib_name=='uniform':

        a = pars[0]
        b = pars[1]

        if np.shape(x)==():
            if (x>=a) & (x<b):
                out = 0.0
            else:
                out = -np.inf
        else:
            out = np.zeros(len(x))
            inds = np.where((x>=a) & (x<=b))[0]
            out[inds] = 0.0
            out[(x<a) | (x>b)] = - np.inf



    elif distrib_name=='normal':

        # pars provides the mean and standard deviation of the normal distribution
        mu = pars[0]
        sigma = pars[1]

        out = lognorm(x,mu,sigma)

    else:

        raise ValueError("Distribution name not known or not implemented")

    return out


def metropolisHastings(target,proposal,xinit, Nsamples,proposalProb = []):
    """
    Metropolis-Hastings algorithm

    Inputs
    ------
    target returns the unnormalized log posterior, called as 
    'p = exp(target(x))'
    proposal is a fn, called as 'xprime = proposal(x)' where x is a 1xd vector
    xinit is a 1xd vector specifying the initial state
    Nsamples - total number of samples to draw
    proposalProb  - optional fn, called as 'p = proposalProb(x,xprime)',
    computes q(xprime|x). Not needed for symmetric proposals (Metropolis 
    algorithm)

    Outputs
    -------
    samples(s,:) is the s'th sample (of size d)
    naccept = number of accepted moves

    This code is adapted from pmtk3.googlecode.com

    """

    d = length(xinit)
    samples = np.zeros(Nsamples, d)
    x = xinit[:]
    naccept = 0
    logpOld = target(x)

    for t in range(Nsamples):
        xprime = proposal(x);
        logpNew = target(xprime);
        alpha = np.exp(logpNew - logpOld)

        if proposalProb is not None: # Hastings correction for asymmetric proposals
            qnumer = proposalProb(x, xprime) # q(x|x')
            qdenom = proposalProb(xprime, x) # q(x'|x)
            alpha = alpha * (qnumer/qdenom)

        r = np.min([1, alpha])
        u = np.random.uniform(low=0.0, high=1.0)
        if u < r:
            x = xprime
            naccept = naccept + 1
            logpOld = logpNew

        samples[t,:] = x

    return samples, naccept


class MHSampler(object):

    def __init__(self, ndim, logp_tilde):
        """

        Parameters
        ----------
        ndim : integer
            dimension of parameter space
        logp_tilde : callable
            log-probability distribution function to target
        """


        self.logp = logp_tilde
        self.N_params = ndim

        # Current state
        self.x = np.zeros(self.N_params, dtype=np.float64)
        self.accepted = 0

        # To save the samples
        self.x_samples = []
        self.logp_samples = []

    def set_cov(self, cov):
         # If the covariance is provided in the form of a matrix
        self.cov = cov
        if len(cov.shape) == 2 :
            self.L = linalg.cholesky(self.cov)
            self.L_func = lambda x : self.L.conj().T.dot(x)

        else:
            self.L_func = lambda x : x * np.sqrt(self.cov)

    def sample(self, x, logp_x):
        """

        Implement a single step of the Metropolis Hasting algorithm

        Reference
        ---------
        Kevin Murphy, Machine Learning: a_mat Probabilistic Perspective, 2012

        """

        # Sample from proposal distribution
        x_prime = x + self.L_func(np.random.normal(loc=0.0, scale=1.0, size=self.N_params))

        logp_xprime = self.logp(x_prime)

        dl = logp_xprime - logp_x

        if (dl > 0):
            x_out = copy.deepcopy(x_prime)
            logp_out = copy.deepcopy(logp_xprime)
            self.accepted = self.accepted + 1
        else:
            u = np.random.uniform(low=0.0, high=1.0)

            if (u < np.exp( dl )):
                x_out = copy.deepcopy(x_prime)
                logp_out = copy.deepcopy(logp_xprime)
                self.accepted = self.accepted + 1
            else:
                x_out = copy.deepcopy(x)
                logp_out = copy.deepcopy(logp_x)

        return x_out, logp_out

    def run_mcmc(self, x0, cov0, Ns, verbose=False, cov_update=100):
        """

        Run MCMC with serveral samples

        """
        self.set_cov(cov0)
        self.accepted = 0
        x_samples = np.zeros((Ns, self.N_params), dtype=np.float64)
        logp_samples = np.zeros((Ns), dtype=np.float64)
        x_samples[0, :] = x0
        logp_samples[0] = self.logp(x0)

        if not verbose:
            for s in range(1, Ns):
                x_samples[s,:],logp_samples[s] = self.sample(x_samples[s-1,:],
                                                             logp_samples[s-1])
        else:
            for s in range(1, Ns):
                x_samples[s,:],logp_samples[s] = self.sample(x_samples[s-1,:],
                                                             logp_samples[s-1])
                if (s%100 == 0):
                    print("Iteration " + str(s) + " completed.")
                    print("Accepted: " + str(self.accepted))
                if (s%cov_update == 0):
                    # Compute empirical covariance according to Haario optimal 
                    # formula:
                    self.set_cov( np.cov(self.x_samples[0:s+1,:].T)*2.38**2/self.N_params)

        return x_samples, logp_samples


class ExtendedPTMCMC(ptemcee.Sampler):

    def __init__(self, *args, **kwargs):

        super(ExtendedPTMCMC, self).__init__(*args, **kwargs)
        # ptemcee.Sampler.__init__(self, args)

        self.position = []

    def get_log_likelihood(self):

        return self._likeprior.logl

    def get_log_likelihood_args(self):

        return self._likeprior.loglargs

    def get_chain(self):

        return self.chain

    def update_log_likelihood(self, log_likelihood, loglike_args):

        self._likeprior.logl = log_likelihood
        self._likeprior.loglargs = loglike_args

    def update_log_prior(self, log_prior, logp_args):

        self._likeprior.logp = log_prior
        self._likeprior.logpargs = logp_args

    def single_sample(self, it, n_it, n_update, n_thin, callback):

        self.position, lnlike0, lnprob0 = self.sample(self.position, n_it,
                                                      thin=n_thin,
                                                      storechain=True)

        if it % n_update == 0:
            print("Update of auxiliary parameters at iteration " + str(it))
            # Instead of always using the same chain, we randomly draw the
            # index.
            i_chain = np.random.randint(low=0, high=self.position.shape[1])
            callback(self.position[0, i_chain, :])

    def run(self, n_it, n_save, n_thin, callback=None, n_callback=1000,
            n_start_callback=0, pos0=None, save_path='./'):
        """

        Parameters
        ----------
        n_it : int
            maximum number of iterations
        n_save : int
            request to save chains to file every n_save iteration
        n_thin : int
            thinning number
        callback : callable
            external function of the parameters, to call at each iteration
        n_callback : int
            call the callback function every n_callback iterations
        pos0 : array_like
            initial values for parameters
        save_path : str
            path to save the data

        Returns
        -------

        """

        # Initialization of parameter values
        if pos0 is None:
            lo, hi = self._likeprior.logpargs
            pos = np.random.uniform(lo, hi, size=(self.ntemps,
                                                  self.nwalkers,
                                                  len(hi)))
        else:
            pos = pos0[:]

        # If no callback function specified, set it to do nothing
        if callback is None:
            def callback(p):
                pass

        self.position = pos[:]
        it = 0

        for pos, lnlike0, lnprob0 in self.sample(pos, n_it,
                                                 thin=n_thin,
                                                 storechain=True):

            if ((it % n_save == 0) & (it != 0)) | (it == n_it - 1):
                print("Save data at iteration " + str(it) + "...")
                file_object = open(save_path + 'chain.p', "wb")
                pickle.dump(self.chain[:, :, 0:it//n_thin, :], file_object,
                            protocol=4)
                file_object.close()
                file_object = open(save_path + 'lnprob.p', "wb")
                pickle.dump(self.logprobability[:, :, 0:it//n_thin], 
                            file_object, protocol=4)
                file_object.close()
                print("Data saved.")

            if (it % n_callback == 0) & (it != 0) & (it >= n_start_callback):
                callback(self.chain[0, 0, it//n_thin, :])
                print("Callback function called at iteration " + str(it))

            it += 1

        return pos, lnlike0, lnprob0

if dynesty_on:
    class ExtendedNestedSampler(dynesty.nestedsamplers.MultiEllipsoidSampler):

        def __init__(self, *args, **kwargs):

            super(ExtendedNestedSampler, self).__init__(*args, **kwargs)

        def get_chain(self):

            return self.results.samples

        def update_log_likelihood(self, log_likelihood, loglike_args):

            self.loglikelihood.func = log_likelihood
            self.loglikelihood.args = loglike_args

        def update_log_prior(self, log_prior, log_prior_args):
            pass

        def run(self, n_it, n_update, n_thin, n_save, callback=None, pos0=None,
                save_path='./', param_names=None):

            print("The main nested sampling loop begins...")
            for it, res in enumerate(self.sample(maxiter=n_it)):
                if (it % n_update == 0) & (callback is not None):
                    print("Update of auxiliary parameters at iteration " + str(it))
                    # callback(self.saved_v[0, :])
                    callback(self.results.samples[0, :])
                if (it % n_save == 0) & (it != 0):
                    print("Save data at iteration " + str(it))
                    df = pd.DataFrame(self.results.samples[-n_save:, :],
                                    columns=param_names)
                    df.to_hdf(save_path, 'chain',
                            append=True, mode='a', format='table')

            print("Adding the final set of live points")
            for it_final, res in enumerate(self.add_live_points()):
                if (it_final % n_save == 0) & (it_final != 0):
                    print("Final iteration " + str(it_final) + " reached.")


    _SAMPLERS = dynesty.dynesty._SAMPLERS
    _SAMPLERS['extended'] = ExtendedNestedSampler


    def extended_nested_sampler(*args, **kwargs):

        return NestedSampler(*args, **kwargs)


    def extended_dynamic_nested_sampler(*args, **kwargs):

        return DynamicNestedSampler(*args, **kwargs)


    def save_object(obj, file_path):

        file_object = open(file_path, "wb")
        pickle.dump(obj, file_object)
        file_object.close()


    def run_and_save(sampler, nlive=50, n_save=1000, n_iter=100000,
                    file_path="initial_save.p", dynamic=False):
        """
        External function allowing us to run a Dynamic Nested Sampler from Dynesty
        while regularly saving the results

        Parameters
        ----------
        sampler : DynamicNestedSampler instance
            dynamic nested sampler
        nlive : int
            number of live points for the initial run
        n_save : int
            canence of result saving, expressed in number of iterations
        file_path : str
            directory path (+ suffix) where so save the results

        Returns
        -------

        """

        if dynamic:
            # Baseline run.
            it = 0
            for results in sampler.sample_initial(nlive=nlive, maxiter=n_iter):
                it += 1
                # If it is a multiple of n_save, save data
                if it % n_save == 0:
                    print("Saving results at iteration " + str(it))
                    save_object(sampler.results, file_path + "initial_save.p")
                else:
                    # print("Iteration " + str(it) + " completed.")
                    pass

            # Save initial results
            save_object(sampler.results, file_path + "initial_save.p")

            # Add batches until we hit the stopping criterion.
            it = 0
            while True:
                # evaluate stop
                stop = stopping_function(sampler.results,
                                        stop_kwargs={'pfrac': 1.0})
                if not stop:
                    # derive bounds
                    logl_bounds = weight_function(sampler.results,
                                                wt_kwargs={'pfrac': 1.0})
                    for results in sampler.sample_batch(logl_bounds=logl_bounds,
                                                        maxiter=n_iter):
                        it += 1
                        # If it is a multiple of n_save, save data
                        if it % n_save == 0:
                            print("Saving results at iteration " + str(it))
                            save_object(sampler.results,
                                        file_path + "batch_save.p")
                        else:
                            pass
                    sampler.combine_runs()  # add new samples to previous results
                else:
                    break

            # Save new results
            save_object(sampler.results, file_path + "batch_save.p")

        else:

            # The main nested sampling loop.
            print("Main nested sampling loop starts...")
            for it, res in enumerate(sampler.sample(maxiter=n_iter,
                                                    save_samples=True)):
                # If it is a multiple of n_save, run the callback function
                if (it % n_save == 0) & (it != 0):
                    print("Saving results at iteration " + str(it))
                    save_object(sampler.results, file_path + "initial_save.p")
                else:
                    pass

            # Save initial results
            save_object(sampler.results, file_path + "initial_save.p")

            # Adding the final set of live points.
            print("Adding the final set of live points...")
            for it_final, res in enumerate(sampler.add_live_points()):
                if (it_final % n_save == 0) & (it_final != 0):
                    save_object(sampler.results, file_path + "final_save.p")
                else:
                    pass

            # Save final results
            save_object(sampler.results, file_path + "final_save.p")
