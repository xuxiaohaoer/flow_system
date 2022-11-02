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
    pcap_name = str(name).replace(" ","_")
    password = '980421'
    command = 'tcpdump -c10 -i en0 -w ./data_raw/{}.pcap'.format(pcap_name)
    # os.system("sudo tcpdump -c100 -i en0 -w ./data_raw/.pcap")
    os.system('echo %s | sudo -S %s' % (password, command))
    tem = Pcap(name=str(name), date=pub_date)
    tem.save()
    pcap_all = Pcap.objects.all()
    
    num = len(pcap_all)
    pcap_name = []
    if num < 5:
        for i in range(num):
            pcap_name.append(pcap_all[num-i-1].name)
    else:
        for i in range(5):
            pcap_name.append(pcap_all[num-i-1].name)
    
    return render(request, 'flow_collect/collect_new.html', {'pcap_name':pcap_name})
# Create your views here.
