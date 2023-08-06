#!/usr/bin/python
import numpy as np
from sidekit import StatServer, Ndx , FactorAnalyser
from sidekit.iv_scoring import fast_PLDA_scoring
import numpy
import copy

def adapt_model(model_iv, g_iv, norm_iv, adaptation_ratio):
    """

    :param model_iv: all vectors (previous + current show)
    :param g_iv: output vectors from the cross_show function
    :param norm_iv: original training vectors (from the training set only)
    :param adaptation_ratio: weight of the out-of domain vectors (between 0 and 1)
    :return:
    """

    vec_dim = g_iv.stat1[0].shape[0]
    adapt_iv, _, __ = keep_recurring_speakers(g_iv, vec_dim, occ_number=2)

    adapt_iv.spectral_norm_stat1(model_iv.sn_mean[:1], model_iv.sn_cov[:1])

    adapted_model_iv = copy.deepcopy(model_iv)
    adapted_model_iv.model_filename = 'model/adapted_model_256_200_100.h5'

    new_plda = FactorAnalyser()
    new_plda.weighted_likelihood_plda(out_stat_server=norm_iv,  # out of domain
                                      in_stat_server=adapt_iv, #
                                      alpha=adaptation_ratio,
                                      rank_f=vec_dim,
                                      nb_iter=10,
                                      scaling_factor=1.,
                                      output_file_name=None,
                                      save_partial=False)

    adapted_model_iv.plda_f = new_plda.F
    adapted_model_iv.plda_sigma = new_plda.Sigma
    adapted_model_iv.plda_mean = new_plda.mean

    return adapted_model_iv



def my_merge(ss_1, ss_2):
    out_sessions = np.unique(ss_1.modelset).shape[0]

    in_sessions = np.unique(ss_2.modelset).shape[0]

    tot_sessions = ss_1.modelset.shape[0] + ss_2.modelset.shape[0]

    flt_iv = StatServer()
    flt_iv.stat0 = np.ones((tot_sessions, 1))
    flt_iv.stat1 = np.ones((tot_sessions, ss_1.stat1.shape[1]))
    flt_iv.modelset = np.empty(tot_sessions, dtype="|O")
    flt_iv.segset = np.empty(tot_sessions, dtype="|O")
    flt_iv.start = np.empty(tot_sessions, dtype="|O")
    flt_iv.stop = np.empty(tot_sessions, dtype="|O")

    for idx in range(ss_1.modelset.shape[0]):
        flt_iv.stat1[idx, :] = ss_1.stat1[idx, :]
        flt_iv.modelset[idx] = str(ss_1.modelset[idx])
        flt_iv.segset[idx] = ss_1.segset[idx]
        flt_iv.start[idx] = ss_1.start[idx]
        flt_iv.stop[idx] = ss_1.stop[idx]

    for idx2 in range(ss_2.modelset.shape[0]):
        idx = idx2 + ss_1.modelset.shape[0]
        flt_iv.stat1[idx, :] = ss_2.stat1[idx2, :]
        flt_iv.modelset[idx] = str(ss_2.modelset[idx2])
        flt_iv.segset[idx] = ss_2.segset[idx2]
        flt_iv.start[idx] = ss_2.start[idx2]
        flt_iv.stop[idx] = ss_2.stop[idx2]

    return flt_iv


def keep_recurring_speakers(iv_ss, rank_F, occ_number=3, filter_by_name=False):
    unique, counts = numpy.unique(iv_ss.modelset, return_counts=True)
    tot_sessions = 0
    kept_idx = []
    for model in range(unique.shape[0]):
        if counts[model] >= occ_number \
                and ((not (unique[model]).startswith("speaker")
                     and not (unique[model]).startswith("presentat")
                     and not (unique[model]).startswith("sup+")
                     and not (unique[model]).startswith("voix")
                     and not (unique[model]).startswith("publicitaire")
                     and not (unique[model]).startswith("locuteur")
                     and not (unique[model]).startswith("inconnu")
                     and not (unique[model]).startswith("traduct")
                     and not ("#" in (unique[model]))
                     and "_" in (unique[model])
                     and filter_by_name)
                     or (not filter_by_name)):
            kept_idx = numpy.append(kept_idx, numpy.where(iv_ss.modelset == unique[model]))
            tot_sessions += counts[model]
    flt_iv = StatServer()
    flt_iv.stat0 = numpy.ones((tot_sessions, 1))
    flt_iv.stat1 = numpy.ones((tot_sessions, rank_F))
    flt_iv.modelset = numpy.empty(tot_sessions, dtype="|O")
    flt_iv.segset = numpy.empty(tot_sessions, dtype="|O")
    flt_iv.start = numpy.empty(tot_sessions, dtype="|O")
    flt_iv.stop = numpy.empty(tot_sessions, dtype="|O")

    i = 0
    for model in range(unique.shape[0]):
        if counts[model] >= occ_number \
                and ((not (unique[model]).startswith("speaker")
                     and not (unique[model]).startswith("presentat")
                     and not (unique[model]).startswith("sup+")
                     and not (unique[model]).startswith("voix")
                     and not (unique[model]).startswith("publicitaire")
                     and not (unique[model]).startswith("locuteur")
                     and not (unique[model]).startswith("inconnu")
                     and not (unique[model]).startswith("traduct")
                     and not ("#" in (unique[model]))
                     and "_" in (unique[model])
                     and filter_by_name)
                     or (not filter_by_name)):
            for ivector in numpy.where(iv_ss.modelset == unique[model])[0]:
                flt_iv.stat1[i, :] = iv_ss.stat1[ivector, :]
                flt_iv.modelset[i] = iv_ss.modelset[ivector]
                flt_iv.segset[i] = iv_ss.segset[ivector]
                flt_iv.start[i] = iv_ss.start[ivector]
                flt_iv.stop[i] = iv_ss.stop[ivector]
                i += 1
    unique = numpy.unique(flt_iv.modelset)
    return flt_iv, unique.shape[0], kept_idx

