from numpy.random import seed

seed(1)
import tensorflow as tf

tf.random.set_seed(4)
import sys

import numpy as np
import os
from .models import AE_Tree
from .tools import read_dataset, evaluation, evaluation_types
from time import time

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
raw_features = [' Source IP', ' Source Port', ' Destination IP', ' Destination Port', ' Flow Duration',
                ' Total Fwd Packets', ' Total Backward Packets',
                'Total Length of Fwd Packets', ' Total Length of Bwd Packets',
                ' Fwd Packet Length Max', ' Fwd Packet Length Min',
                ' Fwd Packet Length Mean', ' Fwd Packet Length Std',
                'Bwd Packet Length Max', ' Bwd Packet Length Min',
                ' Bwd Packet Length Mean', ' Bwd Packet Length Std', 'Flow Bytes/s',
                ' Flow Packets/s', ' Flow IAT Mean', ' Flow IAT Std', ' Flow IAT Max',
                ' Flow IAT Min', 'Fwd IAT Total', ' Fwd IAT Mean', ' Fwd IAT Std',
                ' Fwd IAT Max', ' Fwd IAT Min', 'Bwd IAT Total', ' Bwd IAT Mean',
                ' Bwd IAT Std', ' Bwd IAT Max', ' Bwd IAT Min', 'Fwd PSH Flags',
                ' Bwd PSH Flags', ' Fwd URG Flags', ' Bwd URG Flags', ' Fwd Header Length',
                ' Bwd Header Length', 'Fwd Packets/s', ' Bwd Packets/s',
                ' Min Packet Length', ' Max Packet Length', ' Packet Length Mean',
                ' Packet Length Std', ' Packet Length Variance', 'FIN Flag Count',
                ' SYN Flag Count', ' RST Flag Count', ' PSH Flag Count', ' ACK Flag Count',
                ' URG Flag Count', ' CWE Flag Count', ' ECE Flag Count', ' Down/Up Ratio',
                ' Average Packet Size', ' Avg Fwd Segment Size', ' Avg Bwd Segment Size',
                'Fwd Avg Bytes/Bulk', ' Fwd Avg Packets/Bulk', ' Fwd Avg Bulk Rate',
                ' Bwd Avg Bytes/Bulk', ' Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate',
                'Subflow Fwd Packets', ' Subflow Fwd Bytes', ' Subflow Bwd Packets',
                ' Subflow Bwd Bytes', 'Init_Win_bytes_forward', ' Init_Win_bytes_backward',
                ' act_data_pkt_fwd', ' min_seg_size_forward', 'Active Mean', ' Active Std',
                ' Active Max', ' Active Min', 'Idle Mean', ' Idle Std', ' Idle Max',
                ' Idle Min', ' Label', ' Protocol_0.0', ' Protocol_6.0', ' Protocol_17.0', 'types']

train_path = "./data_feature/HAE/train_data.npy"
test_path = "./data_feature/HAE/test_data.npy"
raw_test_path = "./data_feature/HAE/raw_test.npy"
saved_model_path = "./modelSaved/hae/"


def HAE_train():
    # 模型训练与测试
    print("Read data......")

    train_data, train_ids, test_data, test_ids = read_dataset(train_path,
                                                              test_path)  # ids:[sip,sport,dip,dport,types,labels]

    clf = AE_Tree(n_clf=3, original_dim=train_data.shape[1])

    # 模型训练
    print("HAE Training......")
    t1 = time()
    clf.fit(X=train_data, y=train_data, epochs=1, batch_size=128)
    print("HAE Train Time:".format(time() - t1))
    print("Saving Model......")
    clf.save(saved_model_path)


import pandas as pd


def HAE_test():
    # 模型训练与测试
    print("Read data......")
    train_data, train_ids, test_data, test_ids = read_dataset(train_path,
                                                              test_path)  # ids:[sip,sport,dip,dport,types,labels]

    clf = AE_Tree(n_clf=2, original_dim=train_data.shape[1])

    # 测试集评估
    print("load model.....")
    clf.load(saved_model_path)
    t1 = time()
    pre_data, losses = clf.predict(test_data)
    print('HAE Test Time:', time() - t1)

    print("Test Metrics")
    test_labels = test_ids[:, -1]
    test_types = test_ids[:, -2]
    test_binary_labels = np.array(test_labels).astype(int)
    pre_data = pre_data.astype(int)  # 测试样本预测值，0，1序列
    test_ip_port = test_ids[:, :4]  # 源ip，源port，目的IP、目的port

    raw_data = np.load(raw_test_path, allow_pickle=True)  # 测试数据对应的原始特征值（归一化之前）
    raw_df = pd.DataFrame(raw_data, columns=raw_features)
    # 展示的特征：流持续时间,上⾏流数据包总数,下⾏流数据包总数,上⾏数据包总⻓度,下⾏数据包总⻓度
    # 每秒流字节数，每秒流包数，FIN包数量，SYN包数量，RST包数量，PSH包数量，ACK包数量
    # URG包数量，CWR包数量，ECE包数量，下载上传⽐率，包平均⼤⼩
    view_feas = raw_df[
        [' Flow Duration', ' Total Fwd Packets', ' Total Backward Packets', 'Total Length of Fwd Packets',
         ' Total Length of Bwd Packets',
         'Flow Bytes/s', ' Flow Packets/s', 'FIN Flag Count', ' SYN Flag Count', ' RST Flag Count', ' PSH Flag Count',
         ' ACK Flag Count',
         ' URG Flag Count', ' CWE Flag Count', ' ECE Flag Count', ' Down/Up Ratio', ' Average Packet Size']].values

    from model_test.models import FlowRes
    for i in range(len(pre_data)):
        name = test_ip_port[i][0] + '-' + str(int(test_ip_port[i][1])) + '->' + test_ip_port[i][2] + '-' + str(int(
            test_ip_port[i][3]))
        result = "abnormal" if pre_data[i] else "normal"
        t = FlowRes(name=name, result=result)
        t.save()
    return pre_data, view_feas


if __name__ == '__main__':
    HAE_train()
    HAE_test()
