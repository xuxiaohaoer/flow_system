from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    return render(request, 'flow_collect/collect.html')
# Create your views here.
