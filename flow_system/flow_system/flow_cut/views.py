from django.shortcuts import render
from django.http import HttpResponse
from .pre import flow_pre_cut
def cut(request):
    keys = flow_pre_cut()
    dsts = []
    srcs = []
    connect = []
    for key in keys:
        tem = key.split("->")
        srcs.append(tem[0])
        dsts.append(tem[1])
        connect.append(con(tem[0], tem[1]))
    length  = len(srcs)
    print(connect[0].dst)
    print(dsts[0])
    print(srcs[0])
    return render(request, 'flow_cut/cut.html', {"dsts":dsts,
                                                 "srcs":srcs,
                                                 "connect":connect,
                                                 "length":length,
    })
class con():
    def __init__(self, a, b):
        self.dst = a
        self.src = b 
# Create your views here.
