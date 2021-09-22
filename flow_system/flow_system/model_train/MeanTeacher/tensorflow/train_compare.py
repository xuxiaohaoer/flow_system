# Copyright (c) 2018, Curious AI Ltd. All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial
# 4.0 International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

"""Train ConvNet Mean Teacher on SVHN training set and evaluate against a validation set

This runner converges quickly to a fairly good accuracy.
On the other hand, the runner experiments/svhn_final_eval.py
contains the hyperparameters used in the paper, and converges
much more slowly but possibly to a slightly better accuracy.
"""
import tensorflow.compat.v1 as tf

import numpy as np
tf.disable_v2_behavior()

tf.reset_default_graph()
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import logging
from datetime import datetime

from .experiments.run_context import RunContext
from .datasets import COMPARE
from .mean_teacher.model import Model
from .mean_teacher import minibatching


logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger('main')

#总的训练样本有319000


def MT_train(data_seed=0):
    n_labeled = 320
    n_extra_unlabeled = 0

    model = Model(RunContext(__file__, 0))
    model['rampdown_length'] = 0
    model['rampup_length'] = 4000
    model['training_length'] = 6000
    model['max_consistency_cost'] = 50.0

    tensorboard_dir = model.save_tensorboard_graph()
    LOG.info("Saved tensorboard graph to %r", tensorboard_dir)

    trojan = COMPARE(data_seed, n_labeled, n_extra_unlabeled, True)
    training_batches = minibatching.training_batches(trojan.training, n_labeled_per_batch=50)
    evaluation_batches_fn = minibatching.evaluation_epoch_generator(trojan.evaluation)
    model.train(training_batches, evaluation_batches_fn)

    model.train(training_batches, evaluation_batches_fn)

import numpy as np
def MT_test(data_seed=0):
    tf.reset_default_graph()
    n_labeled = 320
    n_extra_unlabeled = 0

    model = Model(RunContext(__file__, 0))
    model['rampdown_length'] = 0
    model['rampup_length'] = 4000
    model['training_length'] = 6000
    model['max_consistency_cost'] = 50.0

    # tensorboard_dir = model.save_tensorboard_graph()
    # LOG.info("Saved tensorboard graph to %r", tensorboard_dir)

    trojan = COMPARE(data_seed, n_labeled, n_extra_unlabeled, True)
    evaluation_batches_fn = minibatching.evaluation_epoch_generator(trojan.evaluation)
    model.load("./modelSaved/meanTeacher/train_compare/savedModel/0/transient/")
 
    preds=model.evaluate(evaluation_batches_fn) #返回预测值
    ip_ports = np.load('./data_feature/MT/data/images/ip_ports.npy', allow_pickle=True)
    ip_ports = ip_ports[:35436, :4]  # 测试数据对应的源ip，源port，目的IP、目的port
    print("测试完成")


    # for key in preds:
    #         from model_test.models import ImageRes
    #         result = "white" if key else "black"
    #         t = ImageRes(result =result)
    #         t.save()
    for i in range(len(preds)):
        from model_test.models import ImageRes
        name = ip_ports[i][0] + '-'+ str(int(ip_ports[i][1]))+ '->' + ip_ports[i][2] + '-' + str(int(ip_ports[i][3]))
        result = "white" if preds[i] else "black"
        t = ImageRes(name = name, result =result)
        t.save()
