from collections import Counter

import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

from sklearn.model_selection import train_test_split
def read_dataset(train_path,test_path):
    train_data = np.load(train_path, allow_pickle=True)
    test_data = np.load(test_path, allow_pickle=True)
    train_ids= train_data[:, 79:]
    test_ids = test_data[:,79:]
    train_data=train_data[:,:79]
    test_data=test_data[:,:79]
    return train_data.astype(np.float32), train_ids, test_data.astype(np.float32), test_ids

def evaluation(val_labels, pre_labels):
    me = confusion_matrix(val_labels, pre_labels)
    print(me)
    acc = accuracy_score(val_labels, pre_labels)
    pre = precision_score(val_labels, pre_labels)
    re = recall_score(val_labels, pre_labels)
    f1 = f1_score(val_labels, pre_labels)
    print(acc, pre, re, f1)

def evaluation_types(pred, test_classes_types):
    labels = np.unique(test_classes_types)
    for label in labels:
        ll = np.argwhere(test_classes_types == label).flatten()
        kk = [pred[i] for i in ll]
        if label == 'BENIGN':
            print(Counter(kk).get(0))
            print(label, '召回率：%.2f' % (100 * Counter(kk).get(0) / len(kk)))
        else:
            print(Counter(kk).get(1))
            print(label, '召回率：%.2f' % (100 * Counter(kk).get(1) / len(kk)))

from sklearn.metrics import roc_curve, auc, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
def plot_roc(test_binary_labels, val_losses2):
    fpr, tpr, thresholds = roc_curve(test_binary_labels, val_losses2)
    maxindex = (tpr-fpr).tolist().index(max(tpr-fpr))
    threshold = thresholds[maxindex]
    print('异常阈值:',threshold)
    roc_auc = auc(fpr, tpr)
    print('auc:%.2f'% roc_auc)
    # plt.figure()
    # lw = 2
    # plt.figure(figsize=(10, 10))
    # plt.plot(fpr, tpr, color='darkorange',
    #          lw=lw
    #          , label='ROC curve (area = %0.2f)' % roc_auc)  ###假正率为横坐标，真正率为纵坐标做曲线
    # plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    # plt.xlim([0.0, 1.0])
    # plt.ylim([0.0, 1.05])
    # plt.xlabel('False Positive Rate')
    # plt.ylabel('True Positive Rate')
    # plt.title('ROC curve')
    # plt.legend(loc="lower right")
    # plt.show()
    return threshold