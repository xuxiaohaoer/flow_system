from django.shortcuts import render
from .tls.DS import train as DS_train
from .hae.hae_dec import HAE_train
from .MeanTeacher.tensorflow.train_compare import MT_train

def train_tls(request):
    DS_train()
    return render(request, "model_train/train_tls.html")
# Create your views here.

def train_HAE(request):
    HAE_train()
    return render(request, "model_train/train_HAE.html")

def train_MT(request):
    MT_train()
    return render(request, "model_train/train_MT.html")