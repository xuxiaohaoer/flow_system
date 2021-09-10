import tensorflow as tf

from tensorflow.keras.layers import Input, Dense, Lambda
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import RMSprop, Adam
from tensorflow.keras import regularizers
import math
import numpy as np
import matplotlib.pyplot as plt

def ae_2layer(original_dim):
    input_img = Input(shape=(original_dim,))
    encoded = Dense(32, activation='relu')(input_img)
    encoded = Dense(16, activity_regularizer=regularizers.l1(10e-5), activation='relu')(encoded)

    decoded = Dense(32, activation='relu')(encoded)
    decoded = Dense(original_dim, activation='sigmoid')(decoded)

    op = Adam(learning_rate=0.0001)
    autoencoder = Model(inputs=input_img, outputs=decoded)
    autoencoder.compile(optimizer=op, loss='mse')
    return autoencoder

class ae_model():
    def __init__(self, name=None, original_dim=76):
        self.name = str(name)
        self.original_dim = original_dim
        self.model = ae_2layer(original_dim)
        self.c = None

    def fit(self, X, y, batch_size=128, sample_weight=None, epochs=10, validation_data=None):
        history = self.model.fit(X, y, batch_size=batch_size, epochs=epochs, sample_weight=sample_weight,
                                 validation_data=validation_data)
        return history

    def predict(self, X):
        y_pre = self.model.predict(X)
        return y_pre

    def save_weights(self, path):
        self.model.save_weights(path)

    def load_weights(self, path):
        self.model.load_weights(path)


class AE_Tree():
    def __init__(self, n_clf=5, original_dim=76):
        self.n_clf = n_clf
        self.unfit_clfs = []
        for i in range(self.n_clf):
            self.unfit_clfs.append(ae_model(name=i, original_dim=original_dim))

    def fit(self, X, y, epochs=20, batch_size=128, validation_data=None):
        self.clfs = []
        for clf in self.unfit_clfs:
            # 构建AE并训练
            clf.fit(X, X, batch_size=batch_size, epochs=epochs,
                    validation_data=validation_data)

            self.clfs.append(clf)
            y_pre = clf.predict(X)
            loss = ((X-y_pre)**2).mean(axis=1)
            # 选异常分数最高的2/3数据作为下一个模型迭代的训练数据，并吧中间的异常分数作为该ae的阈值
            bad_samp_len = int(len(loss)*2/3) #学得不好的样本数目
            idx = np.argpartition(loss, -bad_samp_len)[-bad_samp_len:] #学得不好的样本索引
            X = X[idx]#学得不好的样本
            clf.c = np.min(loss[idx])


    def predict(self, X):
        index = np.arange(len(X))
        result_list = np.zeros(len(X))
        losses = np.zeros(len(X))
        k = len(self.clfs)
        i = 0
        for clf in self.clfs:
            predictions = clf.predict(X)
            loss = ((X-predictions)**2).mean(axis=1)
            top_x_ind = np.where(loss > clf.c)
            low_x_ind=np.where(loss <= clf.c)
            index_tmp = index[top_x_ind]
            low_index_tmp=index[low_x_ind]
            X = X[top_x_ind]
            losses[low_index_tmp]=loss[low_x_ind]
            index = index_tmp
            if i==k-1:
                losses[index_tmp]=loss[top_x_ind]
                result_list[index] = 1
            i+=1
        return result_list, losses

    def online_dect(self, item)->bool:
        for clf in self.clfs:
            pred=clf.predict(item)
            loss = ((item-pred)**2).mean(axis=1)
            if loss<clf.c:
                return True
        return False

    def save(self, path, thre='thresolds'):
        thresolds = []
        for clf in self.clfs:
            clf.save_weights(path + str(clf.name))
            thresolds.append(clf.c)
        thresolds = np.array(thresolds)
        np.save(thre, thresolds)

    def load(self, path, thre='thresolds.npy'):
        thresolds = np.load(path+thre)
        self.clfs = []
        for i in range(len(self.unfit_clfs)):
            clf = self.unfit_clfs[i]
            clf.load_weights(path + clf.name)
            clf.c = thresolds[i]
            self.clfs.append(clf)


class ADAE():

    def __init__(self, n_clf=5, original_dim=76):
        self.n_clf = n_clf
        self.unfit_clfs = []
        self.original_dim=original_dim
        for i in range(self.n_clf):
            self.unfit_clfs.append(ae_model(name=str(i),original_dim=original_dim))

    def fit(self, X, y, epochs=20, batch_size=128, validation_data=None):
        w = np.ones(len(X))
        self.clfs = []
        i = 0
        for clf in self.unfit_clfs:
            # 构建AE并训练
            clf.fit(X, y, sample_weight=w, batch_size=batch_size, epochs=epochs, validation_data=validation_data)
            # 将重建误差作为样本权重
            # y_pre = clf.predict(X)
            # loss = tf.losses.mean_squared_error(y, y_pre)
            # loss = np.array(loss)
            # d = np.max(loss)
            # loss = loss/d
            # mean_loss = np.sum(loss*w)
            # beta = mean_loss/(1-mean_loss)
            # w = w*pow(beta, (1-loss))/np.sum(w*pow(beta, (1-loss)))
            # clf.alpha = math.log(1/beta)
            # i = i+1
            # print("第",i,"个自编码器的系数是",clf.alpha)
            y_pre = clf.predict(X)
            w = ((y-y_pre)**2).mean(axis=1)
            clf.c = 1 / (0.5 * math.log(np.square(np.sum(w))))
            self.clfs.append(clf)

    def plot_loss(self, path=None):
        for clf in self.clfs:
            his= clf.history
            plt.plot(his.history['loss'])
            plt.plot(his.history['val_loss'])
            plt.title('model loss')
            plt.ylabel('loss')
            plt.xlabel('epoch')
            plt.legend(['train', 'test'], loc='upper left')
            plt.savefig(path+clf.name)
            plt.show()
            plt.close()

    def predict(self, X):
        y_pred = np.zeros((X.shape[0], self.original_dim))
        for clf in self.clfs:
            predictions = clf.predict(X)
            print(clf.c)
            y_pred += clf.c * predictions
        return y_pred

    def save(self, path):
        alpha_list = []
        for clf in self.clfs:
            clf.save_weights(path + clf.name)
            alpha_list.append(clf.c)
        np.save(path + 'adaboost_ae', np.array(alpha_list))

    def load(self, path):
        alpha_array = np.load(path + 'adaboost_ae.npy', allow_pickle=True)
        print(alpha_array)
        self.clfs = []
        for i in range(len(self.unfit_clfs)):
            clf = self.unfit_clfs[i]
            clf.load_weights(path + clf.name)
            clf.c = alpha_array[i]
            self.clfs.append(clf)
