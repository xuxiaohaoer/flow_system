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
    # view_feas = raw_df[[' Flow Duration',' Total Fwd Packets',' Total Backward Packets','Total Length of Fwd Packets',' Total Length of Bwd Packets',
    #                 'Flow Bytes/s',' Flow Packets/s','FIN Flag Count',' SYN Flag Count',' RST Flag Count',' PSH Flag Count',' ACK Flag Count',
    #                 ' URG Flag Count',' CWE Flag Count',' ECE Flag Count',' Down/Up Ratio',' Average Packet Size']].values
    #展示的特征：流持续时间,上⾏流数据包总数,下⾏流数据包总数,上⾏数据包总⻓度,下⾏数据包总⻓度
    #每秒流字节数，每秒流包数，FIN包数量，SYN包数量，RST包数量，PSH包数量，ACK包数量
    #URG包数量，CWR包数量，ECE包数量，下载上传⽐率，包平均⼤⼩
    white = view_feas[idx_ben]
    idx_abn = np.where(pre_data==1)
    black = view_feas[idx_abn]
    flow_dur_black = np.mean(black[:,0])
    tot_fwd_pac_black = np.mean(black[:,1])
    tot_bak_pac_black = np.mean(black[:,2])
    flow_bytes_black = np.mean(black[:,5])
    flow_packet_black = np.mean(black[:,6])
    ack_black = np.mean(black[:,11])


    flow_dur_white = np.mean(white[:,0])
    tot_fwd_pac_white = np.mean(white[:,1])
    tot_bak_pac_white = np.mean(white[:,2])
    flow_bytes_white = np.mean(white[:,5])
    flow_packet_white = np.mean(white[:,6])
    ack_white = np.mean(black[:,11])    
    context = {"f1_b":flow_dur_black,
               "f1_w":flow_dur_white,
               "f2_b":tot_fwd_pac_black,
               "f2_w":tot_fwd_pac_white,
               "f3_b":tot_bak_pac_black,
               "f3_w":tot_bak_pac_white,
               "f4_b":flow_bytes_black,
               "f4_w":flow_bytes_white,
               "f5_b":flow_packet_black,
               "f5_w":flow_packet_white,
               "f6_b":ack_black,
               "f6_w":ack_white}
    print(context)
    return render(request, 'model_test/test_HAE.html', context)

def test_MT(request):
    MT_test()
    return render(request, 'model_test/test_MT.html')