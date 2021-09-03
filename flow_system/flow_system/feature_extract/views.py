from django.shortcuts import render
from django.http import HttpResponse
from feature_extract.feature_extract import pre_flow
# Create your views here.
def feature_extract(request):
    pre_flow("/Users/xuhao/研一项目/检测系统/flow_system/flow_system/flow_system/data_cut/tls/", '/Users/xuhao/研一项目/检测系统/flow_system/flow_system/flow_system/data_feature/black.npy', 'black')
    return render(request, 'feature_extract/extract.html')
