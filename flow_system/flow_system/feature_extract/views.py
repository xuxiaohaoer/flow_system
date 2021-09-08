from django.shortcuts import render
from django.http import HttpResponse
from feature_extract.tls.feature_extract import pre_flow
import os
# Create your views here.
def feature_extract_tls(request):
    pre_flow("./data_cut/tls/", './data_feature/tls/black.npy', 'black')
    return render(request, 'feature_extract/extract_tls.html')


def feature_extract_flow(request):

    return render(request, 'feature_extract/extract_flow.html')


def feature_extract_image(request):

    return render(request, 'feature_extract/extract_image.html')