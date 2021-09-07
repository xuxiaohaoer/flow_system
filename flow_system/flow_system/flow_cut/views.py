from django.shortcuts import render
from django.http import HttpResponse
from .pre import flow_pre_cut
def cut(request):
    flow_pre_cut()
    return render(request, 'flow_cut/cut.html')
# Create your views here.
