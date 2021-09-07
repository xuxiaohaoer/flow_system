from numpy.random import seed
seed(1)

from pyod.models.pca import PCA
from pyod.models.lof import LOF
from pyod.models.iforest import IForest
from pyod.models.hbos import HBOS
import numpy as np
# 加载数据集
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from time import time
from git_HAE.tools import read_dataset
from sklearn.linear_model import LogisticRegression



def evaluation(true_label, pre_label):
    acc = accuracy_score(true_label, pre_label)
    re = recall_score(true_label, pre_label)
    pre = precision_score(true_label, pre_label)
    f1 = f1_score(true_label, pre_label)
    print('准确率:%.2f' % (100 * acc), '精确率:%.2f' % (100 * pre), '召回率:%.2f' % (100 * re), 'f1分数:%.2f' % (100 * f1))


if __name__ == "__main__":
    train_path = "../../dataset/CICIDS2017/train_data.npy"
    test_path = "../../dataset/CICIDS2017/test_data.npy"

    train_data, train_ids, test_data, test_ids = read_dataset(train_path, test_path)
    print(train_data.shape)
    print(test_data.shape)

    t1 = time()
    # 训练 PCA 检测器
    # clf = PCA(n_components=5, n_selected_components=3)

    # IForest
    # clf = IForest()

    # # HBOS
    clf = HBOS(11)

    clf.fit(train_data)
    print('训练时间', time() - t1)

    # 获得训练集的预测标签和异常分数
    # y_train_pred = clf.labels_  # (0: 正常, 1: 异常)
    # y_train_scores = clf.decision_scores_
    # print(y_train_scores)

    # 获得测试集的预测结果
    t2 = time()
    y_test_pred = clf.predict(test_data)
    print('测试时间', time() - t2)
    test_binary_labels = np.array(test_ids[:, -1]).astype(int)
    evaluation(test_binary_labels, y_test_pred)
