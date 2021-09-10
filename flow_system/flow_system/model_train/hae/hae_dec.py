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

train_path = "./data_feature/HAE/train_data.npy"
test_path = "./data_feature/HAE/test_data.npy"
saved_model_path = './modelSaved/hae/'

def HAE_train():
    # 模型训练与测试
    print("Read data......")

    train_data, train_ids, test_data, test_ids = read_dataset(train_path, test_path)  # ids:[sip,sport,dip,dport,types,labels]

    clf = AE_Tree(n_clf=3, original_dim=train_data.shape[1])

    # 模型训练
    print("HAE Training......")
    t1 = time()
    clf.fit(X=train_data, y=train_data, epochs=1, batch_size=128)
    print("HAE Train Time:".format(time() - t1))
    print("Saving Model......")
    clf.save(saved_model_path)


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
    
    from model_test.models import FlowRes
    for i in range(len(pre_data)):
        name = test_ip_port[i][0] + '-'+ str(test_ip_port[i][1])+ '->' + test_ip_port[i][2] + '-' + str(test_ip_port[i][3])
        result = "abnormal" if pre_data[i] else "normal"
        t = FlowRes(name=name, result=result)
        t.save()
    # evaluation(test_binary_labels, pre_data) #整体性能评估
    # evaluation_types(pre_data, test_types) #攻击类别评估

    # # 模型预测(单条流)
    # flow=test_data[0]
    # print("load model.....")
    # clf.load(saved_model_path)
    # normal = clf.online_dect(flow)
    # if normal == False:
    #     print('异常')

if __name__ == '__main__':
    HAE_train()
    HAE_test()
   
