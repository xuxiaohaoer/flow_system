from django.shortcuts import render
from django.http import HttpResponse
from feature_extract.tls.feature_extract import pre_flow
from feature_extract.flow.feature_extract import pre_flow_flow
from feature_extract.image.feature_extract import pre_flow_image
import os
# Create your views here.
def feature_extract_tls(request):
    pre_flow("./data_cut/tls/", './data_feature/tls/show.npy', 'test')
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
    return render(request, 'feature_extract/extract_flow.html', {"f_spot":f_spot.tolist(),
                                                                 "f":f})


def feature_extract_image(request):
    pre_flow_image("./data_cut/flow/", './data_feature/MT/show.npy', 'test')
    return render(request, 'feature_extract/extract_image.html')