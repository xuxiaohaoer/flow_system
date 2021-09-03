from django.shortcuts import render
from model_train.DS import test as DS_test
def test(request):
    DS_test()
    return render(request, 'model_test/test.html')
# Create your views here.
