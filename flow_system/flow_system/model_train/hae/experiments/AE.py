from numpy.random import seed
seed(1)
import tensorflow as tf
tf.random.set_seed(2)
import sys
sys.path.append('../../')

import tensorflow as tf
import os
import numpy as np
from git_HAE.models import ae_2layer
from time import time
from git_HAE.tools import read_dataset, evaluation, evaluation_types,plot_roc
import matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 屏蔽通知信息和警告信息
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

tf.debugging.set_log_device_placement(True)


if __name__ == '__main__':
    train_path = "../../dataset/CICIDS2017/train_data.npy"
    test_path = "../../dataset/CICIDS2017/test_data.npy"
    saved_model_path = './savedModel/AE/'

    # 模型训练与测试
    print("Read data......")
    train_data, train_ids, test_data, test_ids = read_dataset(train_path, test_path)  # ids:[sip,sport,dip,dport,types,labels]

    autoencoder = ae_2layer(train_data.shape[1])
    # 训练
    # t1=time()
    # history = autoencoder.fit(train_data, train_data, epochs=30, batch_size=128, validation_data=None)
    # print(time()-t1)
    # autoencoder.save_weights(saved_model_path)
    # plt.plot(history.history['loss'])
    # plt.title('model loss')
    # plt.ylabel('loss')
    # plt.xlabel('epoch')
    # plt.savefig('train_loss')
    # plt.show()


    # 测试集评估
    autoencoder.load_weights(saved_model_path)
    t2 = time()
    pre_data = autoencoder.predict(test_data)
    print('预测时间',time()-t2)


    test_labels = test_ids[:, -1]
    test_types=test_ids[:, -2]
    test_binary_labels = np.array(test_labels).astype(int)
    test_losses = tf.losses.mean_squared_error(test_data, pre_data).numpy()
    threshold = plot_roc(test_binary_labels, test_losses) #根据roc曲线确定最佳阈值
    pred=[]
    for loss in test_losses:
        if loss > threshold:
            pred.append(1)
        else:
            pred.append(0)
    evaluation(test_binary_labels, pred)
    evaluation_types(pred, test_types)
