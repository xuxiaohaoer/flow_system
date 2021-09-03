from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score

def cal_index(y_batch, pred):
    print(confusion_matrix(y_batch, pred, labels=[1, 0]))
    acc = accuracy_score(y_batch, pred)
    pre = precision_score(y_batch, pred)
    rec = recall_score(y_batch, pred)
    f1 = f1_score(y_batch, pred)
    print("acc:{:.4}".format(accuracy_score(y_batch, pred)))
    print("pre:{:.4}".format(precision_score(y_batch, pred)))
    print("rec:{:.4}".format(recall_score(y_batch, pred)))
    print("f1:{:.4}".format(f1_score(y_batch, pred)))
    return acc, pre, rec, f1