from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from flow_collect.models import Pcap
import os
import time 
def index(request):
    os.system("pwd")
    name = time.asctime(time.localtime(time.time()))
    # os.system("tshark -c5 -i en0 -w ./data_raw/{}.pcap".format(str(tem).replace(" ","_")))
    pub_date = timezone.now()

    os.system("sudo tcpdump -c100 -i en0 -w ./data_raw/{}.pcap".format(str(name).replace(" ","_")))
    tem = Pcap(name=str(name), date=pub_date)
    tem.save()
    return render(request, 'flow_collect/collect.html')
# Create your views here.
