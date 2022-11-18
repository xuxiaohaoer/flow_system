from django.shortcuts import render
from django.http import HttpResponse
from feature_extract.flow.feature_extract import pre_flow_flow
from feature_extract.image.feature_extract import pre_flow_image
from feature_extract.tls.f_e import pre_flow
import os
import argparse
# Create your views here.
def feature_extract_tls(request):
    print("begin")
    parse = argparse.ArgumentParser()
    parse.add_argument("--d", type=str, default="normal", help="dataset")
    parse.add_argument("--f", type=str, default="mix_word_seq", help="feature_type")
    parse.add_argument("--s", type=bool, default=True, help="save or not")
    parse.add_argument("--m", type=str, default="datacon", help="dataset model")
    parse.add_argument("--l", type=int, default=95, help="word_num")
    parse.add_argument("--ip", type=bool, default=True)
    parse.add_argument("--tcp", type=bool, default=True)
    parse.add_argument("--app", type=bool, default=False)

    args = parse.parse_args()
    # pre_flow(testdir + "data_train/", '{}/train_packet_fre.npy'.format(path), '0')
    
    pre_flow(args)
    # pre_flow("./data_cut/tls/", './data_feature/tls/show.npy', 'test')
    return render(request, 'feature_extract/extract_tls.html')


def feature_extract_flow(request):
    f_spot = pre_flow_flow("./data_cut/flow/", './data_feature/flow/show.npy', 'test')
    f_1 = []
    f_1_max = 0
    f_2 = []
    f_2_max = 0
    for key in f_spot:
        if key[0]>f_1_max:
            f_1 = key
            f_1_max = key[0]
        if key[1]>f_2_max:
            f_2 = key
            f_2_max = key[1]
    f =[]
    f.append(f_1.tolist())
    f.append(f_2.tolist())
    
    class args(object):
        def __init__(self):
            self.f = "mix_word_seq" 
            self.s = True
            self.l = 95
            self.ip = True
            self.tcp = True
            self.app = True
    arg = args()

    print(arg)
    # pre_flow(testdir + "data_train/", '{}/train_packet_fre.npy'.format(path), '0')
    
    pre_flow(arg)
    return render(request, 'f_extract/extract_flow.html', {"f_spot":f_spot.tolist(),
                                                                 "f":f})


def feature_extract_image(request):
    pre_flow_image("./data_cut/flow/", './data_feature/MT/show.npy', 'test')
    return render(request, 'feature_extract/extract_image.html')