from numpy.random import seed

seed(1)
import tensorflow as tf

tf.random.set_seed(2)
import sys

sys.path.append('../../')
import numpy as np
import tensorflow as tf
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from time import time
from git_HAE.models import ADAE
from git_HAE.tools import evaluation, evaluation_types, read_dataset, plot_roc

if __name__ == '__main__':
    train_path = "../../dataset/CICIDS2017/train_data.npy"
    test_path = "../../dataset/CICIDS2017/test_data.npy"
    saved_model_path = './savedModel/ABAE/'

    train_data, train_ids, test_data, test_ids = read_dataset(train_path, test_path)
    clf = ADAE(n_clf=4, original_dim=train_data.shape[1])
    # 模型训练
    # t1=time()
    # clf.fit(X=train_data, y=train_data, epochs=10, batch_size=128, validation_data=None)
    # print("训练时间", time()-t1)
    # clf.save(saved_model_path)

    # 模型预测
    clf.load(saved_model_path)
    t2 = time()
    pre_data = clf.predict(test_data)
    print('预测时间：', time() - t2)

    test_labels = test_ids[:, -1]
    test_types = test_ids[:, -2]
    test_binary_labels = np.array(test_labels).astype(int)
    test_losses = tf.losses.mean_squared_error(test_data, pre_data).numpy()
    threshold = plot_roc(test_binary_labels, test_losses)  # 根据roc曲线确定最佳阈值
    pred = []
    for loss in test_losses:
        if loss > threshold:
            pred.append(1)
        else:
            pred.append(0)
    evaluation(test_binary_labels, pred)
    evaluation_types(pred, test_types)
