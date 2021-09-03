from django.shortcuts import render
from .DS import train as DS_train
def train(request):
    DS_train()
    return render(request, "model_train/train.html")
# Create your views here.
