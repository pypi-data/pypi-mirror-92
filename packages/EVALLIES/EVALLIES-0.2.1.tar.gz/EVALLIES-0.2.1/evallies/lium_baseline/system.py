# -* coding: utf-8 -*-

#################################################################################
# This file is part of EVALLIES.                                                #
#                                                                               #
# EVALLIES is a python package for lifelong learning speaker diarization.       #
# Home page: https://git-lium.univ-lemans.fr/Larcher/evallies                   #
#                                                                               #
# EVALLIES is free software: you can redistribute it and/or modify              #
# it under the terms of the GNU LLesser General Public License as               #
# published by the Free Software Foundation, either version 3 of the License,   #
# or (at your option) any later version.                                        #
#                                                                               #
# EVALLIES is distributed in the hope that it will be useful,                   #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 #
# GNU Lesser General Public License for more details.                           #
#                                                                               #
# You should have received a copy of the GNU Lesser General Public License      #
# along with SIDEKIT.  If not, see <http://www.gnu.org/licenses/>.              #
#                                                                               #
#################################################################################
"""
Copyright 2020-2021 Anthony Larcher, Meysam Shamsi & Yevhenii Propkopalo

    :mod:`lium_baseline.system`

"""


import copy
import decimal
import fastcluster
import h5py
import logging
import numpy
import os
import pandas
import pickle
import sidekit
import soundfile
import s4d
import sys
import torch
import torch
import yaml

from scipy.cluster import hierarchy as hac

from scipy.spatial.distance import squareform

from .utils import add_show_in_id
from .utils import remove_show_from_id
from .utils import s4d_to_allies

from .utils import keep_recurring_speakers
#from .incremental import perform_iv_seg
#from .incremental import cross_show

from ..user_simulation import MessageToUser
from ..user_simulation import Request

from .interactive import apply_correction
# from .interactive import active_learning_tree
from .interactive import active_learning_tree_two_options

from .plda_adapt import adapt_model

#from s4d import viterbi, segmentation
#from s4d.clustering import hac_bic
#from s4d.model_iv import ModelIV



def concat_statservers(ss_1, ss_2):
    out_sessions = numpy.unique(ss_1.modelset).shape[0]

    in_sessions = numpy.unique(ss_2.modelset).shape[0]

    tot_sessions = ss_1.modelset.shape[0] + ss_2.modelset.shape[0]

    flt_iv = sidekit.StatServer()
    flt_iv.stat0 = numpy.ones((tot_sessions, 1))
    flt_iv.stat1 = numpy.ones((tot_sessions, ss_1.stat1.shape[1]))
    flt_iv.modelset = numpy.empty(tot_sessions, dtype="|O")
    flt_iv.segset = numpy.empty(tot_sessions, dtype="|O")
    flt_iv.start = numpy.empty(tot_sessions, dtype="|O")
    flt_iv.stop = numpy.empty(tot_sessions, dtype="|O")

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


def rename_models(within_iv, within_diar, existing_models):
    """
    """
    within_models = dict()
    idx = 0

    for mod in set(within_iv.modelset):
        while f"Spk{idx}" in existing_models:
            idx += 1
        within_models[mod] = f"Spk{idx}"
        idx += 1

    within_iv.modelset = within_iv.modelset.astype('U50')
    for idx, mod in enumerate(within_iv.modelset):
        within_iv.modelset[idx] = within_models[mod]


    for idx, seg in enumerate(within_diar.segments):
        within_diar.segments[idx]['cluster'] = within_models[seg['cluster']]

    return within_iv, within_diar


def perform_iv_seg(sn_mean,
                   sn_cov,
                   plda_mean,
                   plda_f,
                   plda_sigma,
                   th_W,
                   initial_diar,
                   within_iv,
                   hac_method,
                   precomputed_scores=None):
    """

    """

    # Compute scores for each pair of segment to be used in human assisted correction
    # It provides information


    within_iv_mean = within_iv.mean_stat_per_model()

    # Normalize i-vectors
    within_iv_mean.spectral_norm_stat1(sn_mean[:1], sn_cov[:1])
    if within_iv_mean.modelset.shape[0] > 1:
        if precomputed_scores is None:
            # Compute scores
            ndx = sidekit.Ndx(models=within_iv_mean.modelset, testsegs=within_iv_mean.modelset)
            scores = sidekit.iv_scoring.fast_PLDA_scoring(within_iv_mean, within_iv_mean, ndx,
                                                          plda_mean,
                                                          plda_f,
                                                          plda_sigma,
                                                          p_known=0.0,
                                                          scaling_factor=1.0,
                                                          check_missing=False)
            scores.scoremat = 0.5 * (scores.scoremat + scores.scoremat.transpose())
        else:
            scores = precomputed_scores
            scores.scoremat = 0.5 * (scores.scoremat + scores.scoremat.transpose())

        # Run HAC clustering
        new_diar, cluster_dict, merge = s4d.clustering.hac_iv.hac_iv(initial_diar, scores, threshold=th_W, method=hac_method)
        

        # Update the model names of i-vector
        # reverse the cluster dict:
        update_dict = dict()
        for k, v in cluster_dict.items():
            for _v in v:
                update_dict[_v] = k
        
        for idx, mod in enumerate(within_iv.modelset):
            if mod in update_dict:
                within_iv.modelset[idx] = update_dict[mod]

    else:
        new_diar = initial_diar
        scores = None 

    return new_diar, within_iv, scores


def cross_show(model, model_cfg, previous_iv, previous_diar, within_iv, within_diar, th_x, incremental=True):
    """
    """
    # Make sure model names are not overlapping (change within show models if needed)
    within_iv, within_diar = rename_models(within_iv, within_diar, existing_models=previous_iv.modelset)
    # backup previous_iv and within_iv
    within_iv_backup = copy.deepcopy(within_iv)
    previous_iv_backup = copy.deepcopy(previous_iv)

    # get the mean_per_model for previous and within
    within_iv_mean = within_iv.mean_stat_per_model()
    previous_iv_mean = previous_iv.mean_stat_per_model()

    # merge the mean_per_model for previous and within
    ll_iv_mean = concat_statservers(previous_iv_mean, within_iv_mean)

    # compute scores, constrain and run HAC clustering
    # Normalize all
    ll_iv_mean.spectral_norm_stat1(model["model_iv"].sn_mean[:1], model["model_iv"].sn_cov[:1])

    # Compute the score matrix
    ndx = sidekit.Ndx(models=ll_iv_mean.modelset, testsegs=ll_iv_mean.modelset)
    scores = sidekit.iv_scoring.fast_PLDA_scoring(ll_iv_mean, ll_iv_mean, ndx,
                                                  model["model_iv"].plda_mean,
                                                  model["model_iv"].plda_f,
                                                  model["model_iv"].plda_sigma,
                                                  p_known=0.0,
                                                  scaling_factor=1.0,
                                                  check_missing=False)
    scores.scoremat = -0.5 * (scores.scoremat + scores.scoremat.transpose())

    # Constrain the scores to forbid any new clustering between previous shows
    lowest_distance = numpy.min(scores.scoremat)
    for iv_idx in range(previous_iv_mean.modelset.shape[0]):
        for iv_jdx in range(previous_iv_mean.modelset.shape[0]):
            if previous_iv_mean.modelset[iv_idx] == previous_iv_mean.modelset[iv_jdx]:
                scores.scoremat[iv_idx, iv_jdx] = lowest_distance - 1
            else:
                scores.scoremat[iv_idx, iv_jdx] = numpy.inf


    # Add to keep the within show clustering
    for iv_idx in range(previous_iv_mean.modelset.shape[0], ll_iv_mean.modelset.shape[0]):
        for iv_jdx in range(previous_iv_mean.modelset.shape[0], ll_iv_mean.modelset.shape[0]):
            if ll_iv_mean.modelset[iv_idx] == ll_iv_mean.modelset[iv_jdx]:
                scores.scoremat[iv_idx, iv_jdx] = lowest_distance - 1
            else:
                scores.scoremat[iv_idx, iv_jdx] = numpy.inf
    # fin modif

    # Modify the scores between old shows and the current one accordingly
    numpy.fill_diagonal(scores.scoremat, numpy.inf)
    for idx in range(previous_iv_mean.modelset.shape[0], ll_iv_mean.modelset.shape[0]):
        for jdx in range(previous_iv_mean.modelset.shape[0]):
            scores.scoremat[idx, jdx] = numpy.max(scores.scoremat[idx, numpy.where(previous_iv_mean.modelset == previous_iv_mean.modelset[jdx])])
            scores.scoremat[jdx, idx] = scores.scoremat[idx, jdx]
    numpy.fill_diagonal(scores.scoremat, 0)

    numpy.fill_diagonal(scores.scoremat, numpy.inf)

    #with open("matrix_ cross_show.txt", 'w') as fh:
    #    for ii in range(scores.scoremat.shape[0]):
    #        for jj in range(scores.scoremat.shape[1]):
    #            fh.write(f"{scores.scoremat[ii, jj]:3.1f},\t")
    #        fh.write("\n")

    mini0 = numpy.min(scores.scoremat) - 1
    scores.scoremat -= mini0

    modelset_seg_idx = dict()
    for seg in previous_diar.segments:
        modelset_seg_idx[seg['cluster']] = numpy.where(ll_iv_mean.modelset == seg['cluster'])[0]

    numpy.fill_diagonal(scores.scoremat, 0.0)
    squareform_plda = squareform(scores.scoremat)
    #Z = fastcluster.linkage(squareform_plda, method='complete', metric='euclidean', preserve_input=True)
    Z = fastcluster.linkage(squareform_plda, method='complete', preserve_input=True)

    """
    if we want to set the final number of cluster (approach DiHard)
    the next line should be replaced with

    final_cluster_nb = 12
    T = hac.fcluster(Z, t=final_cluster_nb, criterion="maxclust")

    Beware, final_cluster_nb should be higher than than the number of cluster existing in previous_iv_mean
    """
    T = hac.fcluster(Z, th_x - mini0, 'distance')

    # DSon't allow to modify the names of previously existing clusters
    # Create a dictionnary with old_model_name as key and new_luster as value
    cluster_dict = dict()
    clusters_by_index = dict()
    for ii in range(T.shape[0]):
        if T[ii] not in clusters_by_index:
            clusters_by_index[T[ii]] = ll_iv_mean.modelset[ii]
        cluster_dict[ll_iv_mean.modelset[ii]] = clusters_by_index[T[ii]]

    # concatenate previous_iv et within_iv
    new_previous_iv = concat_statservers(previous_iv_backup, within_iv_backup)
    new_previous_diar = copy.deepcopy(previous_diar)
    new_previous_diar.segments += within_diar.segments

    # Modify the model names for i-vectors
    for ii, mod in enumerate(new_previous_iv.modelset):
        new_previous_iv.modelset[ii] = cluster_dict[mod]

    # modify the model names for diar
    for ii, seg in enumerate(new_previous_diar.segments):
        new_previous_diar.segments[ii]['cluster'] = cluster_dict[seg['cluster']]

    for ii, seg in enumerate(within_diar.segments):
        within_diar.segments[ii]['cluster'] = cluster_dict[seg['cluster']]

    return new_previous_iv, new_previous_diar, within_diar

#def allies_load_seg(model_cfg, th, show):
#
#    current_diar = s4d.Diar.read_seg(f"{model_cfg['tmp_dir']}/seg/within_{th}/{show}.seg")
#    current_vec = sidekit.StatServer(f"{model_cfg['tmp_dir']}/seg/within_{th}/{show}_vec.h5")
#
#    return current_diar, current_vec


def allies_initial_training(system_config, train_data):
    """
    Train the initial Diarization system
    """
    # Load the config file
    with open(system_config, 'r') as fh:
        model_cfg = yaml.load(fh, Loader=yaml.FullLoader)

    if model_cfg["model"]["type"] == "lium_iv":
        model, model_cfg = lium_iv_initial_training(model_cfg, train_data)

    elif model_cfg["model"]["type"] == "lium_xv":
        model, model_cfg = lium_xv_initial_training(model_cfg, train_data)

    elif model_cfg["model"]["type"] == "lium_sliding_iv":
        model = None

    elif model_cfg["model"]["type"] == "lium_sliding_xv":
        model = None

    return model, model_cfg



def lium_sliding_xv(model_cfg, train_data):
    pass



def lium_iv_initial_training(model_cfg, train_data):
    """
    Extract features and store them in tmp folder
    Train UBM
    Train TV
    Extract i-vectors
    Train PLDA

    :param model_cfg: a dictionnary describing the system parameters 
    :param train_data: a Data generator used to access the data
    """
    fe = sidekit.FeaturesExtractor(audio_filename_structure="",
                                   feature_filename_structure="feat/{}.h5",
                                   sampling_frequency=16000,
                                   lower_frequency=133.3333,
                                   higher_frequency=6855.4976,
                                   filter_bank="log",
                                   filter_bank_size=40,
                                   window_size=0.025,
                                   shift=0.01,
                                   ceps_number=13,
                                   pre_emphasis=0.97,
                                   keep_all_features=True,
                                   vad='percentil',
                                   save_param=["energy", "cep", "vad"],
                                   compressed='none')

    fs_seg = sidekit.FeaturesServer(feature_filename_structure=model_cfg['tmp_dir']+ "/feat/{}.h5",
                                    dataset_list = ['energy', 'cep'],
                                    keep_all_features=True,
                                    mask='[1-13]',
                                    delta=False,
                                    double_delta=False)


    fs_acoustic = sidekit.FeaturesServer(feature_filename_structure=model_cfg['tmp_dir'] + "/feat/{}.h5",
                                         dataset_list = ['energy', 'cep'],
                                         keep_all_features=False,
                                         delta=True,
                                         double_delta=True,
                                         feat_norm='cmvn_sliding')

    train_diar = s4d.diar.Diar()
    train_diar.add_attribut(new_attribut='gender', default='U')
    name_dict = {}
    # iterate on train_data
    if not os.path.isdir(f"{model_cfg['tmp_dir']}/feat"):
        os.makedirs(f"{model_cfg['tmp_dir']}/feat")

    for idx, (show, file_info, uem, ref, filename) in enumerate(train_data):

        if not os.path.isfile(f"{model_cfg['tmp_dir']}/feat/{show}.h5"):
            fe.save(show,
                    channel=0,
                    input_audio_filename=filename,
                    output_feature_filename=f"{model_cfg['tmp_dir']}/feat/{show}.h5")

        # Use the ref info to fill the Diar object
        for spk, start, end in zip(ref.speaker, ref.start_time, ref.end_time):
            train_diar.append(show=show,
                              cluster= spk,
                              start=int(round(float(start) * 100.)),
                              stop=int(round(float(end) * 100.))
                              #stop=int(round(float(end) * 100.)) + int(round(float(start) * 100.))
                              )

    print(f'Training data contains:')
    print("\t" + f'{len(train_diar.unique("show"))} files')
    print("\t" + f'{len(train_diar.unique("cluster"))} speakers')
    print("\t" + f'{len(train_diar)} segments')
    name_dict[show] = int(idx)


    ######################################
    # Train UBM
    ######################################
    ubm_diar = copy.deepcopy(train_diar)
    ubm_diar.segments = ubm_diar.segments[:1000]
    ubm_idmap = ubm_diar.id_map()

    if not os.path.isfile(f"{model_cfg['tmp_dir']}/model/ubm.h5"):
        ubm = sidekit.Mixture()
        logging.critical("Start UBM training with {} segments".format(len(ubm_idmap.leftids)))
        ubm.EM_split(fs_acoustic,
                     ubm_idmap,
                     model_cfg['model']['distrib_nb'],
                     num_thread=model_cfg['nb_thread'],
                     save_partial=False)
        ubm.write(f"{model_cfg['tmp_dir']}/model/ubm.h5")
    else:
        logging.critical("Load UBM from file")
        ubm = sidekit.Mixture(f"{model_cfg['tmp_dir']}/model/ubm.h5")
    logging.critical("\t Done")

    ######################################
    # Train TV
    ######################################
    long_seg_diar = copy.deepcopy(train_diar)
    short_seg_diar = long_seg_diar.filter("duration", "<", 100)
    long_seg_diar = long_seg_diar.filter("duration", ">=", 100)
    tv_idmap = long_seg_diar.id_map()

    if not os.path.isfile(f"{model_cfg['tmp_dir']}/model/TV.h5"):

        # Accumulate sufficient statistics for the training data
        logging.critical("Create StatServer with {} segments".format(len(tv_idmap.leftids)) )
        tv_stat = sidekit.StatServer(tv_idmap,
            distrib_nb=ubm.get_distrib_nb(),
            feature_size=model_cfg['model']['feature_size'] * 3
            )

        tv_stat.accumulate_stat(ubm=ubm,
            feature_server=fs_acoustic,
            seg_indices=range(tv_stat.segset.shape[0]),
            num_thread=model_cfg['nb_thread']
            )

        tv_stat = add_show_in_id(tv_stat)
        tv_stat.write(f"{model_cfg['tmp_dir']}/model/tv_stat.h5")
        logging.critical("\t Done")

        # Sufficient statistics are passed to the FactorAnalyser via an HDF5 file handler that stays in memory
        tv_stat_h5f = h5py.File(f'{model_cfg["tmp_dir"]}/tmp_tv_stat.h5', 'a', backing_store=False, driver='core')
        tv_stat.to_hdf5(tv_stat_h5f)
        #tv_stat.write(f'{model_cfg["tmp_dir"]}/tv_stat.h5', prefix='', mode='w')
        tv_fa = sidekit.FactorAnalyser()
        logging.critical("Start TV training with {} segments".format(len(tv_stat.modelset)))
        tv_fa.total_variability(tv_stat_h5f,
                                ubm,
                                tv_rank=model_cfg['model']['vectors']['size'],
                                nb_iter=10,
                                min_div=True,
                                tv_init=None,
                                batch_size=300,
                                save_init=False,
                                output_file_name=None,
                                num_thread=model_cfg['nb_thread'])
        tv_fa.write(f"{model_cfg['tmp_dir']}/model/TV.h5")
    else:
        logging.critical("Load TV from file")
        tv_fa = sidekit.FactorAnalyser(f"{model_cfg['tmp_dir']}/model/TV.h5")
    logging.critical("\t Done")

    ######################################
    # Extract I-vectors and train PLDA
    ######################################
    if not os.path.isfile(f"{model_cfg['tmp_dir']}/model/training_ivectors.h5"):

        if not os.path.isfile(f"{model_cfg['tmp_dir']}/model/short_seg_stat.h5"):
            # Accumulate sufficient statistics for the short segment from training data
            short_seg_idmap = short_seg_diar.id_map()
            short_seg_stat = sidekit.StatServer(short_seg_idmap,
                distrib_nb=ubm.get_distrib_nb(),
                feature_size=model_cfg['model']['feature_size'] * 3
                )
            logging.critical("Start computing short segment statistics: {}".format(len(short_seg_stat.modelset)))
            short_seg_stat.accumulate_stat(ubm=ubm,
                                           feature_server=fs_acoustic,
                                           seg_indices=range(short_seg_stat.segset.shape[0]),
                                           num_thread=model_cfg['nb_thread']
                                           )
            logging.critical("short iv stat ok")
            # Rename in order to get one i-vector per segment
            #tv_stat = add_show_in_id(tv_stat)
            short_seg_stat = add_show_in_id(short_seg_stat)

            short_seg_stat.write(f"{model_cfg['tmp_dir']}/model/short_seg_stat.h5")



        logging.critical("Start extracting i-vectors")
        long_iv = tv_fa.extract_ivectors(ubm, f"{model_cfg['tmp_dir']}/model/tv_stat.h5", num_thread=model_cfg['nb_thread'])
        short_iv = tv_fa.extract_ivectors(ubm, f"{model_cfg['tmp_dir']}/model/short_seg_stat.h5",  num_thread=model_cfg['nb_thread'])

        current_iv = long_iv.merge(long_iv, short_iv)

        #long_iv.write(f"{model_cfg['tmp_dir']}/long_ivectors.h5")
        #short_iv.write(f"{model_cfg['tmp_dir']}/short_ivectors.h5")
        current_iv.write(f"{model_cfg['tmp_dir']}/model/training_ivectors.h5")
    else:
        logging.critical("Load IV from file")
        current_iv = sidekit.StatServer(f"{model_cfg['tmp_dir']}/model/training_ivectors.h5")
    logging.critical("\tI-vectors OK")


    # After taking the mean per speaker per file, we rename the clusters in order
    # to get one mean i-vector per speaker per file but same cluster_ID across shows
    current_iv_mean = current_iv.mean_stat_per_model()
    current_iv_mean = remove_show_from_id(current_iv_mean)

    # Normalize i-vectors
    norm_iv = copy.deepcopy(current_iv_mean)
    norm_mean, norm_cov = norm_iv.estimate_spectral_norm_stat1(1, 'sphNorm')
    norm_iv, n_recc, _ = keep_recurring_speakers(norm_iv, rank_F=model_cfg['model']['vectors']['size'], occ_number=2, filter_by_name=True)

    norm_iv.spectral_norm_stat1(norm_mean, norm_cov)
    logging.critical("start PLDA training")
    #plda_fa = sidekit.FactorAnalyser() Train  PLDA
    plda_fa = sidekit.FactorAnalyser()
    plda_fa.plda(norm_iv,
            rank_f=model_cfg['model']['plda_rank'],
            nb_iter=10,
            scaling_factor=1.,
            output_file_name=f"{model_cfg['tmp_dir']}/model/plda",
            save_partial=False)
    logging.critical("PLDA ok")

    model_iv = s4d.ModelIV()
    model_iv.ubm = ubm
    model_iv.tv = tv_fa.F
    model_iv.tv_mean = tv_fa.mean
    model_iv.tv_sigma = tv_fa.Sigma
    model_iv.sn_mean = norm_mean
    model_iv.sn_cov = norm_cov
    model_iv.plda_mean = plda_fa.mean
    model_iv.plda_f = plda_fa.F
    model_iv.plda_g = None
    model_iv.plda_sigma = plda_fa.Sigma
    model_iv.ivectors = current_iv
    model_iv.scores = None
    model_iv.nb_thread = 1

    model = dict()
    model["model_iv"] = model_iv
    model["global_diar"] = train_diar
    pickle.dump(model, open(f"{model_cfg['tmp_dir']}/model/model_allies_baseline_{model_cfg['model']['vectors']['type']}v.p", "wb" ))

    return model, model_cfg


def lium_vad_training(model_cfg, train_data):
    """
    Select data for VAD training
    Train the model
    return the model

    :param model_cfg:
    :param train_data:
    :return:
    """
    # Prepare the training data
     #IL SUFFIT DE GENERER LA LISTE DE FICHIERS ET DE LA STOCKER DANS TMP
    training_file_list = []
    for idx, (show, file_info, uem, ref, filename) in enumerate(train_data):
        training_file_list.append(show)
    with open("list/vad_list.lst", "w") as fh:
        fh.write("\n".join(training_file_list))

    # Iterative training
    s4d.nnet.seqTrain(dataset_yaml=model_cfg['model']['vad']['db_yaml'],
                      model_yaml=model_cfg['model']['vad']['model_yaml'],
                      epochs=model_cfg['model']['vad']['epochs'],
                      lr=model_cfg['model']['vad']['lr'],
                      patience=2,
                      tmp_model_name=model_cfg['tmp_dir']+"/model/tmp_vad",
                      best_model_name=model_cfg['tmp_dir']+"/model/best_vad",
                      multi_gpu=True,
                      opt=model_cfg['model']['vad']['opt'],
                      log_interval=10,
                      num_thread=model_cfg['nb_thread']
                      )


def lium_xv_initial_training(model_cfg, train_data):
    """

    """

    if not os.path.isdir(f"{model_cfg['tmp_dir']}/model"):
        os.makedirs(f"{model_cfg['tmp_dir']}/model")

    # Train the VAD and save to disk
    if not os.path.isfile(model_cfg['tmp_dir'] + "/model/best_vad.pt"):
        lium_vad_training(model_cfg, train_data)

    train_diar = s4d.diar.Diar()
    df_data = dict()
    df_data['speaker_idx'] = []
    df_data['database'] = []
    df_data['speaker_id'] = []
    df_data['start'] = []
    df_data['duration'] = []
    df_data['file_id'] = []
    df_data['gender'] = []
    train_diar.add_attribut(new_attribut='gender', default='U')
    name_dict = {}

    # iterate on train_data
    spk_idx = 0
    speaker_idx = dict()
    for idx, (show, file_info, uem, ref, filename) in enumerate(train_data):

        # Use the ref info to fill the Diar object
        # fill a pandas.DataFrame at the sale tim to select data for X-vector extractor training
        for spk, start, end in zip(ref.speaker, ref.start_time, ref.end_time):
            if spk not in speaker_idx:
                speaker_idx[spk] = spk_idx
                spk_idx += 1

            train_diar.append(show=show,
                              cluster= spk,
                              start=int(round(float(start) * 100.)),
                              stop=int(round(float(end) * 100.)) ,
                              #stop=int(round(float(end) * 100.)) + int(round(float(start) * 100.))
                              )
            df_data["speaker_idx"].append(speaker_idx[spk])
            df_data["speaker_id"].append(spk)
            df_data["start"].append(start)
            df_data["duration"].append(end - start)
            df_data["file_id"].append(show)
            df_data["database"].append("allies_train")
            df_data["gender"].append('u')

    print(f'Training data contains:')
    print("\t" + f'{len(train_diar.unique("show"))} files')
    print("\t" + f'{len(train_diar.unique("cluster"))} speakers')
    print("\t" + f'{len(train_diar)} segments')

    df = pandas.DataFrame(df_data)
    df = df.loc[df['duration'] > model_cfg['model']['vectors']['xvectors']['duration']]
    vc = df.speaker_idx.value_counts()
    selected_df = df[df.speaker_idx.isin(vc.index[vc.values >= model_cfg['model']['vectors']['xvectors']['min_nb_sessions']])]
    speaker_new_idx = dict(zip(list(selected_df.speaker_idx.unique()), numpy.arange(len(list(selected_df.speaker_idx.unique())))))
    selected_df = selected_df.reset_index(drop=True)
    for idx in range(len(selected_df)):
        selected_df.at[idx, 'speaker_idx'] = speaker_new_idx[selected_df.at[idx, 'speaker_idx']]
    
    selected_df.to_csv("list/xvector.csv", index=False)

    training_speaker_nb = len(selected_df.speaker_idx.unique())

    model_cfg["model"]["speaker_nb"] = training_speaker_nb
    #model_cfg["model"]["speaker_nb"] = 111
    if not os.path.isfile(model_cfg['tmp_dir']+"/model/best_xtractor.pt"):
        sidekit.nnet.xtrain(speaker_number=training_speaker_nb,
                            dataset_yaml=model_cfg['model']['vectors']['xvectors']['db_yaml'],
                            epochs=model_cfg['model']['vectors']['xvectors']['epochs'],
                            lr=model_cfg['model']['vectors']['xvectors']['lr'],
                            model_yaml=model_cfg['model']['vectors']['xvectors']['xtractor_yaml'],
                            model_name=None,
                            loss=model_cfg['model']['vectors']['xvectors']["loss"],
                            tmp_model_name=model_cfg['tmp_dir']+"/model/tmp_xtractor",
                            patience=50,
                            opt=model_cfg['model']['vectors']['xvectors']['opt'],
                            best_model_name=model_cfg['tmp_dir']+"/model/best_xtractor",
                            multi_gpu=True,
                            num_thread=model_cfg['nb_thread'])

    # Extract x-vectors
    train_diar = train_diar.filter("duration", ">=", 100)

    #############
    # Select speakers for PLDA training
    # Keep only sessions longer than model_cfg['model']['vectors']['xvectors']['duration']
    # And speakers having at least model_cfg['model']['vectors']['xvectors']['min_nb_sessions'] sessions
    #############
    train_diar = train_diar.filter("duration", ">=", int(model_cfg['model']['vectors']['xvectors']['duration'] * 100))

    training_idmap = train_diar.id_map()
    training_idmap.start = training_idmap.start * 160
    training_idmap.stop = training_idmap.stop * 160

    if not os.path.isfile(f"{model_cfg['tmp_dir']}/model/training_xv.h5"):
        training_xv = sidekit.nnet.xvector.extract_embeddings(idmap_name=training_idmap,
                                                              model_filename=model_cfg['tmp_dir']+"/model/best_xtractor.pt",
                                                              data_root_name=train_data.root_folder + '/wav/',
                                                              device=torch.device("cuda:0"),
                                                              transform_pipeline=model_cfg['model']['vectors']['xvectors']["transforms"])
        training_xv.write(f"{model_cfg['tmp_dir']}/model/training_xv.h5") 

    training_xv = sidekit.StatServer(f"{model_cfg['tmp_dir']}/model/training_xv.h5")
    # Compute normalization parameters
    training_xv, n_recc, _ = keep_recurring_speakers(training_xv,
                                                     rank_F=model_cfg['model']['vectors']['size'],
                                                     occ_number=model_cfg['model']['vectors']['xvectors']['min_nb_sessions'],
                                                     filter_by_name=True)
    training_xv = add_show_in_id(training_xv)
    training_xv_mean = training_xv.mean_stat_per_model()
    training_xv_mean = remove_show_from_id(training_xv_mean)

    norm_xv = copy.deepcopy(training_xv_mean)
    norm_mean, norm_cov = norm_xv.estimate_spectral_norm_stat1(1, 'sphNorm')
    # Train PLDA
    norm_xv.spectral_norm_stat1(norm_mean, norm_cov)
    plda_fa = sidekit.FactorAnalyser()
    plda_fa.plda(norm_xv,
                 rank_f=model_cfg['model']['classifier']['plda_rank'],
                 nb_iter=50,
                 scaling_factor=1.,
                 output_file_name=f"{model_cfg['tmp_dir']}/model/plda",
                 save_partial=False)


    model_iv = s4d.ModelIV()
    model_iv.sn_mean = norm_mean
    model_iv.sn_cov = norm_cov
    model_iv.plda_mean = plda_fa.mean
    model_iv.plda_f = plda_fa.F
    model_iv.plda_g = None
    model_iv.plda_sigma = plda_fa.Sigma
    model_iv.ivectors = training_xv
    model_iv.scores = None
    model_iv.nb_thread = 1

    model = dict()
    model["model_iv"] = model_iv
    model["global_diar"] = train_diar
    pickle.dump(model, open(f"{model_cfg['tmp_dir']}/model/model_allies_baseline_{model_cfg['model']['vectors']['type']}v.p", "wb" ))

    return model, model_cfg


def extract_vectors(model, model_cfg, current_diar, root_folder):
    """

    """
    if model_cfg["model"]["type"] == "lium_iv":
        # Load features
        fs_acoustic = sidekit.FeaturesServer(feature_filename_structure=f"{model_cfg['tmp_dir']}" + "/feat/{}.h5",
                                             dataset_list = ["energy", 'cep'],
                                             keep_all_features=True,
                                             delta=True,
                                             double_delta=True,
                                             feat_norm='cmvn_sliding'
                                            )
        current_im = current_diar.id_map()
        # Extract i-vectors
        current_vec = model["model_iv"].train_per_segment(fs_acoustic,current_im, normalization=False)

    elif model_cfg["model"]["type"] == "lium_xv":
        # extract x-vectors
        current_im = current_diar.id_map()
        current_im.start = current_im.start * 160 
        current_im.stop = current_im.stop * 160 
        current_vec = sidekit.nnet.xvector.extract_embeddings(idmap_name=current_im,
                                                              model_filename=model_cfg['tmp_dir']+"/model/best_xtractor.pt",
                                                              data_root_name=root_folder + '/wav/',
                                                              device=torch.device("cuda:0"),
                                                              transform_pipeline=model_cfg["model"]["vectors"]["xvectors"]["transforms"],
                                                              num_thread=10)

    return current_vec

def allies_init_seg(th_W, model, system_config, show, file_info, filename, root_folder):
    """

    """
    if isinstance(system_config, str):
        with open(system_config, 'r') as fh:
            model_cfg = yaml.load(fh, Loader=yaml.FullLoader)
    else:
        model_cfg = system_config

    if not os.path.isdir(f"{model_cfg['tmp_dir']}/seg/first/"):
        os.makedirs(f"{model_cfg['tmp_dir']}/seg/first/")

    # Perform first seg if it doesn't exist
    if not os.path.isfile(f"{model_cfg['tmp_dir']}/seg/first/{show}.seg"):
        # perform first seg
        if model_cfg["first_seg"]["type"] == "bic":

            if not os.path.isfile(f"{model_cfg['tmp_dir']}/feat/{show}.h5"):
                # Load MFCC
                fe = sidekit.FeaturesExtractor(audio_filename_structure="",
                                               feature_filename_structure="",
                                               sampling_frequency=16000,
                                               lower_frequency=133.3333,
                                               higher_frequency=6855.4976,
                                               filter_bank="log",
                                               filter_bank_size=40,
                                               window_size=0.025,
                                               shift=0.01,
                                               ceps_number=13,
                                               pre_emphasis=0.97,
                                               keep_all_features=True, #was 'percentile' before
                                               vad=None,
                                               save_param=["energy", "cep", "vad"])

                fe.save(show,
                        channel=0,
                        input_audio_filename=filename,
                        output_feature_filename=f"{model_cfg['tmp_dir']}/feat/{show}.h5")

            fs_seg = sidekit.FeaturesServer(feature_filename_structure=f"{model_cfg['tmp_dir']}/feat/{{}}.h5",
                                            dataset_list = ['energy', 'cep'],
                                            keep_all_features=True,
                                            delta=False,
                                            double_delta=False)

            cep, _= fs_seg.load(show)

            if model_cfg["model"]["vad"]["type"] == "none":
                init_diar = s4d.segmentation.init_seg(cep, show)

            elif model_cfg["model"]["vad"]["type"] == "from_file":
                print(f"Load ref segmentation: {model_cfg['model']['vad']['dir']}/{show}.mdtm")
                #init_diar = s4d.Diar.read_seg(f"{model_cfg['model']['vad']['dir']}/{show}.seg")              
                init_diar = s4d.Diar.read_mdtm(f"{model_cfg['model']['vad']['dir']}/{show}.mdtm")

            if model_cfg["first_seg"]["bic_lin"]:
                # Bic_lin is not useful when loading the reference and hurts a lot
                current_diar = s4d.segmentation.segmentation(cep, init_diar)
                current_diar = s4d.segmentation.bic_linear(cep, current_diar, model_cfg['first_seg']['thr_l'], sr=False)
            else:
                current_diar = init_diar


            if model_cfg["first_seg"]["hac_bic"]:
                hac = s4d.clustering.hac_bic.HAC_BIC(cep, current_diar, model_cfg['first_seg']['thr_h'], sr=False)
                current_diar = hac.perform()

            if model_cfg["first_seg"]["viterbi"]:
                current_diar = s4d.viterbi.viterbi_decoding(cep, current_diar, model_cfg['first_seg']['thr_vit'])

        else:
            #slidding window
            nfo = soundfile.info(filename)
            # Get beginning and end of the file
            start = 0.0
            end = float(nfo.frames) / 16000.

            current_diar = s4d.Diar()
            current_diar.add_attribut(new_attribut='gender', default='U')
            s = 0.0
            e = float(model_cfg["first_seg"]["sliding_window"])
            idx = 0
            while e < end:
                current_diar.append(show=show,
                                    cluster=f"tmp{idx}",
                                    start=int(s * 100),
                                    stop=int((s + e) * 100),
                                    gender='U')

                idx += 1
                s += float(model_cfg["first_seg"]["sliding_shift"])
                e += float(model_cfg["first_seg"]["sliding_window"])

        s4d.Diar.write_seg(f"{model_cfg['tmp_dir']}/seg/first/{show}.seg", current_diar)
        allies_write_diar(current_diar, f"{model_cfg['tmp_dir']}/seg/first/{show}.mdtm")

    # load the first seg
    first_pass_diar = s4d.Diar.read_seg(f"{model_cfg['tmp_dir']}/seg/first/{show}.seg")
    current_diar = copy.deepcopy(first_pass_diar)

    if model_cfg["second_seg"] == "true":

        # Extract segment representation (i-vectors or x-vectors)
        if not os.path.isfile(f"{model_cfg['tmp_dir']}/seg/first/{show}_{model_cfg['model']['vectors']['type']}v.h5"):
            current_vec = extract_vectors(model, model_cfg, current_diar, root_folder)
            current_vec.write(f"{model_cfg['tmp_dir']}/seg/first/{show}_{model_cfg['model']['vectors']['type']}v.h5")
        else:
            print(f"Load {model_cfg['tmp_dir']}/seg/first/{show}_{model_cfg['model']['vectors']['type']}v.h5")
            current_vec = sidekit.StatServer(f"{model_cfg['tmp_dir']}/seg/first/{show}_{model_cfg['model']['vectors']['type']}v.h5")

        scores = None

        first_pass_vec = copy.deepcopy(current_vec)

        # Perform HAC-xv if necessary
        current_diar, current_vec, scores = perform_iv_seg(model["model_iv"].sn_mean,
                                                           model["model_iv"].sn_cov,
                                                           model["model_iv"].plda_mean,
                                                           model["model_iv"].plda_f,
                                                           model["model_iv"].plda_sigma,
                                                           th_W,
                                                           current_diar,
                                                           current_vec,
                                                           model_cfg["within_show"]["hac_method"],
                                                           scores)

    else:
        current_vec = None
        first_pass_vec = None
        scores = None

    if not os.path.isdir(f"{model_cfg['tmp_dir']}/seg/within_{th_W}/"):
        os.makedirs(f"{model_cfg['tmp_dir']}/seg/within_{th_W}/")

    s4d.Diar.write_seg(f"{model_cfg['tmp_dir']}/seg/within_{th_W}/{show}.seg", current_diar)
    allies_write_diar(current_diar, f"{model_cfg['tmp_dir']}/seg/within_{th_W}/{show}.mdtm")

    return current_diar, first_pass_diar, current_vec, first_pass_vec, scores, th_W


def allies_within_show_HAL(current_diar,
                           first_pass_diar,
                           current_vec,
                           first_pass_vec,
                           scores_per_cluster,
                           th,
                           model_cfg,
                           model,
                           file_info,
                           user,
                           uem,
                           ref):
    """
    At the moment only correct the diarization using Active Learning
    :param current_diar:
    :param current_vec:
    :param scores:
    :param th:
    :param model_cfg:
    :param model:
    :param file_info:
    :param user:
    :param uem:
    :param ref:
    :return:
    """

    if len(current_diar.unique("cluster")) < 2:
        hal = False
        der_track = None
        new_diar = current_diar
        new_vec = current_vec
    else:
        hal = True

    while hal:

        # If the mode is "active learning"
        if 'process_all_nodes' in model_cfg['within_show']:
            p_a_n=model_cfg['within_show']['process_all_nodes']
        else:
            p_a_n=False
        if 'selection_method' in model_cfg['within_show']:
            seg_met=model_cfg['within_show']['selection_method']
        else:
            seg_met='longest'
        if 'conditional_questioning' in model_cfg['within_show']:
            cond_q=model_cfg['within_show']['conditional_questioning']
        else:
            cond_q=False
        if 'hac_method' in model_cfg['within_show']:
            hac_method=model_cfg['within_show']['hac_method']
        else:
            hac_method='complete'

        if seg_met in ["cluster_center_score", "max", "min"]:
            # Compute scores between all pairs of segments as they are needed for those criteria
            # Normalize i-vectors
            first_pass_vec.spectral_norm_stat1(model["model_iv"].sn_mean[:1], model["model_iv"].sn_cov[:1])
            # Compute scores
            ndx = sidekit.Ndx(models=first_pass_vec.modelset, testsegs=first_pass_vec.modelset)
            scores_per_segment = sidekit.iv_scoring.fast_PLDA_scoring(first_pass_vec, first_pass_vec, ndx,
                                                                      model["model_iv"].plda_mean,
                                                                      model["model_iv"].plda_f,
                                                                      model["model_iv"].plda_sigma,
                                                                      p_known=0.0,
                                                                      scaling_factor=1.0,
                                                                      check_missing=False)
            scores_per_segment.scoremat = 0.5 * (scores_per_segment.scoremat + scores_per_segment.scoremat.transpose())
        else:
            scores_per_segment = None


        hal, new_diar, new_vec, der_track = active_learning_tree_two_options(current_diar,
                                                                            first_pass_diar,
                                                                            current_vec,
                                                                            scores_per_cluster,
                                                                            scores_per_segment,
                                                                            th,
                                                                            user,
                                                                            file_info,
                                                                            uem,
                                                                            ref,
                                                                            process_all_nodes=p_a_n,
                                                                            clustering_method=hac_method,
                                                                            selection_method=seg_met,
                                                                            conditional_questioning=cond_q)

    return new_diar, new_vec, der_track

def allies_cross_show_clustering(show_idx, model, model_cfg, current_diar, current_vec, th_x, adapt=False):
    """

    """
    if show_idx == 0:
        model["previous_vec"] = copy.deepcopy(current_vec)
        model["previous_diar"] = current_diar

    else:
        #previous_diar.segments += within_diar.segments
        # Apply cross-show clustering
        previous_vec, previous_diar, current_diar = cross_show(model=model,
                                                               model_cfg=model_cfg,
                                                               previous_iv=model["previous_vec"],
                                                               previous_diar=model["previous_diar"],
                                                               within_iv=current_vec,
                                                               within_diar=current_diar,
                                                               th_x=th_x,
                                                               incremental=True)

        model["previous_vec"] = previous_vec
        model["previous_diar"] = previous_diar

        if adapt:
            norm_iv = sidekit.StatServer.read('tmp/model/training_xv.h5'.format('ester_repere'))
            model['model_iv'] = adapt_model(model['model_iv'], previous_vec, norm_iv, 0.2)

    return model, current_diar


def allies_write_diar(current_diar, filename):
    """

    """
    cdiar = copy.deepcopy(current_diar)
    for idx, seg in enumerate(cdiar):
        cdiar.segments[idx]['start'] = float(seg['start']) / 100.
        cdiar.segments[idx]['stop'] = float(seg['stop']) / 100.


    cdiar.sort(['show', 'start'])
    with open(filename, 'w', encoding="utf8") as fic:
        for line in s4d.Diar.to_string_seg(cdiar, time_float=True):
            fic.write(line)


