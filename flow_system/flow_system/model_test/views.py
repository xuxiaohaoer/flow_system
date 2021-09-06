from django.shortcuts import render
from model_train.DS import test as DS_test
def test_tls(request):
    DS_test()
    return render(request, 'model_test/test.html')
# Create your views here.

# def test_xx(request):
#     ...
#     return render(request, 'model_test/test_1.html')
