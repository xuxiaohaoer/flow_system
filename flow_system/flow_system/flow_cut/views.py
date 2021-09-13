from django.shortcuts import render
from django.http import HttpResponse
from .pre import flow_pre_cut
def cut(request):
    num_flow, num_tls = flow_pre_cut()

    
    return render(request, 'flow_cut/cut.html', {"num_flow":num_flow,
                                                 "num_tls":num_tls,
    })
# Create your views here.
