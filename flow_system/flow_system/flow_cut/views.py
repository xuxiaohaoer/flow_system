from django.shortcuts import render
from django.http import HttpResponse
from .pre import flow_pre_cut
def cut(requeset):
    flow_pre_cut('black')
    return HttpResponse("already cut")
# Create your views here.
