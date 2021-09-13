from django.shortcuts import render
from model_train.tls.DS import test as DS_test
from model_train.hae.hae_dec import HAE_test
from model_train.MeanTeacher.tensorflow.train_compare import MT_test
import numpy as np
import pandas as pd
def test_tls(request):
    DS_test()

    return render(request, 'model_test/test_tls.html')

# Create your views here.
def test_HAE(request):
    pre_data, view_feas = HAE_test()
    idx_ben=np.where(pre_data==0)
    #展示的特征：流持续时间,上⾏流数据包总数,下⾏流数据包总数,上⾏数据包总⻓度,下⾏数据包总⻓度
    #每秒流字节数，每秒流包数，FIN包数量，SYN包数量，RST包数量，PSH包数量，ACK包数量
    #URG包数量，CWR包数量，ECE包数量，下载上传⽐率，包平均⼤⼩
    white = view_feas[idx_ben]
    idx_abn = np.where(pre_data==1)
    black = view_feas[idx_abn]
    flow_duration_black = black[:,0]
    print(flow_duration_black[0])
    print(flow_duration_black[1])
    context = {}
    
    return render(request, 'model_test/test_HAE.html')

def test_MT(request):
    MT_test()
    return render(request, 'model_test/test_MT.html')