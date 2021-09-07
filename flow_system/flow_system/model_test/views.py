from django.shortcuts import render
from model_train.tls.DS import test as DS_test
from model_train.hae.hae_dec import HAE_test
from model_train.MeanTeacher.tensorflow.train_compare import MT_test
def test_tls(request):
    DS_test()
    HAE_test()
    MT_test()
    return render(request, 'model_test/test_tls.html')

# Create your views here.
# def test_xx(request):
#     ...
#     return render(request, 'model_test/test_1.html')
