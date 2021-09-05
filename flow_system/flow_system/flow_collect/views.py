from django.shortcuts import render
from django.http import HttpResponse
import os
import time 
def index(request):
    os.system("pwd")
    tem = time.asctime(time.localtime(time.time()))
    # os.system("tshark -c5 -i en0 -w ./data_raw/{}.pcap".format(str(tem).replace(" ","_")))
    os.system("sudo tcpdump -c100 -i en0 -w ./data_raw/{}.pcap".format(str(tem).replace(" ","_")))
    return render(request, 'flow_collect/collect.html')
# Create your views here.
