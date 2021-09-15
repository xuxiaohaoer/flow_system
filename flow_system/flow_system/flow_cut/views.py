from django.shortcuts import render
from django.http import HttpResponse
from .pre import flow_pre_cut
def cut(request):
    num_tot_flow, num_tot_tls = flow_pre_cut()
    while (len(num_tot_flow)<5):
        num_tot_flow.append(0)
        num_tot_tls.append(0)   
    return render(request, 'flow_cut/cut.html', {"num_tls":num_tot_tls,
                                                 "num_flow":num_tot_flow
    })

# Create your views here.
