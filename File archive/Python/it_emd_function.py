"""
Extraction of IMFs using iterated masking EMD (itEMD).

Routines:
    it_emd
"""

import numpy as np
import emd
import warnings

############### FUNCTION IMPLEMENTATION ###########################################

def it_emd(x, sample_rate, mask_0='zc', N_imf=6, 
           N_iter_max=15, iter_th=0.1, N_avg=1, exclude_edges=False, 
           verbose=False, w_method='power', 
           ignore_last=False):

    samples = len(x)
    
    # Initialise mask
    if mask_0 == 'nyquist':
        mask = np.array([sample_rate/2**(n+1) for n in range(1, N_imf+1)])/sample_rate
    elif mask_0 =='zc':
        _, mask = emd.sift.mask_sift(x, max_imfs=N_imf, mask_freqs='zc',
                                       ret_mask_freq=True)
    elif mask_0 == 'random':
        mask = np.random.randint(0, sample_rate/4, size=N_imf) / sample_rate
    else:
        mask = mask_0
    
    # Initialise output variables and counters
    mask_all = np.zeros((N_iter_max+N_avg, N_imf))
    imf_all = np.zeros((N_iter_max+N_avg, N_imf, samples))
    niters = 0; niters_c = 0
    navg = 0
    maxiter_flag = 0
    continue_iter = True
    converged = False
    
    while continue_iter:
        if not converged:
            print(niters, end=' ')
        else:
            print('Converged, averaging... ' + str(niters_c) + ' / ' + str(N_avg))
        
        mask_all[niters+niters_c, :len(mask)] = mask
        
        # Compute mask sift
        imf = emd.sift.mask_sift(x, max_imfs=N_imf, mask_freqs=mask,
                                 mask_amp_mode='ratio_imf')
        
        # Compute IF and weighted IF mean for next iteration
        IP,IF,IA = emd.spectra.frequency_transform(imf, sample_rate, 'nht')
        mask_prev = mask
    
        if exclude_edges:
            ex = int(0.025*samples)
            samples_included = list(range(ex, samples-ex)) #Edge effects ignored
        else:
            samples_included = list(range(samples)) #All
        
        if w_method == 'IA':
            IF_weighted = np.average(IF[samples_included, :], 0, weights=IA[samples_included, :])
        if w_method == 'power':
            IF_weighted = np.average(IF[samples_included, :], 0, weights=IA[samples_included, :]**2)
        if w_method == 'avg':
            IF_weighted = np.mean(IF[samples_included, :], axis=0)
            
        mask = IF_weighted/sample_rate
        imf_all[niters+niters_c, :imf.shape[1], :] = imf.T

        # Check convergence 
        l = min(len(mask), len(mask_prev))  # l to exclude potential nans
        if ignore_last:
            l -= 1
        mask_variance = np.abs((mask[:l] - mask_prev[:l]) / mask_prev[:l]) 
        
        if np.all(mask_variance[~np.isnan(mask_variance)] < iter_th) or converged: 
            converged = True
            if navg < N_avg:
                navg += 1
            else:
                continue_iter = False
        
        if not converged:
            niters += 1
        else:
            niters_c += 1
        
        # Check maximum number of iterations
        if niters >= N_iter_max:
            warnings.warn('Maximum number of iterations reached')
            maxiter_flag = 1
            continue_iter = False
        
    print('N_iter = ', niters)
        
    # Compute final IMFs
    if maxiter_flag == 1:
        imf_final = imf_all[niters-1, :, :].T
        IF_final = mask_all[niters-1, :]*sample_rate
    else:
        imf_final = np.nanmean(imf_all[niters:niters+N_avg, :, :], axis=0).T
        IF_final = np.nanmean(mask_all[niters:niters+N_avg, :], axis=0)*sample_rate
    IF_std_final = np.nanstd(mask_all[niters:niters+N_avg, :], axis=0)*sample_rate
    
    # If no averaging, make mask variance as deviation from last iteration
    if N_avg < 2:
        IF_std_final = mask_variance
    
    # Only output non-nan IMFs
    N_imf_final = int(np.sum(~np.isnan(mask_all[niters-1, :])))
    imf_final = imf_final[:, :N_imf_final]
    IF_final = IF_final[:N_imf_final]
    IF_std_final = IF_std_final[:N_imf_final]
    
    if verbose:
        return [niters, mask_all, imf_final, IF_final, IF_std_final, imf_all]
    return [imf_final, IF_final, IF_std_final, niters, maxiter_flag]