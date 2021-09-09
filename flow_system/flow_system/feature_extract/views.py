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
    pre_flow_flow("./data_cut/flow/", './data_feature/flow/show.npy', 'test')
    return render(request, 'feature_extract/extract_flow.html')


def feature_extract_image(request):
    pre_flow_image("./data_cut/flow/", './data_feature/MT/show.npy', 'test')
    return render(request, 'feature_extract/extract_image.html')