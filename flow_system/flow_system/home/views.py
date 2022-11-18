from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, request
from django.shortcuts import render
from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, Paginator


def index_test(request):
    # return render(request, 'home/index.html')
    return render(request, 'home/index_old.html')
def login(request):
    # return render(request, 'home/index.html')
    return render(request, 'home_new/pages-login.html')

def pages_recoverpw(request):
    return render(request, 'home_new/pages-recoverpw.html')


def pages_register(request):
    return render(request, 'home_new/pages-register.html')



def index(request):
    from flow_cut.models import pcap_cut
    flow_all = pcap_cut.objects.all()
    flow_num = len(flow_all)
    from flow_collect.models import Pcap
    pcap_all = Pcap.objects.all()
    pcap_num = len(pcap_all)

    from model_test.models import TlsRes
    black_list = TlsRes.objects.filter(result='black')
    num_black = len(black_list)
    white_list = TlsRes.objects.filter(result='white')
    num_white = len(white_list)
    #使用Paginator模块对数据分页，一页5条数据
    paginator = Paginator(black_list, 12)
    #使用request.GET.get()函数获取uri中的page参数的数值
    try:
        page = request.GET.get('page')
        currentPage = int(page)
    except TypeError as e:
        currentPage = 1
    if paginator.num_pages > 15:
        if currentPage-5 < 1:
            pageRange = range(1,11)
        elif currentPage+5 > paginator.num_pages:
            pageRange = range(currentPage-5,paginator.num_pages)
        else:
            pageRange = range(currentPage-5,currentPage+5)
    else:
        pageRange = paginator.page_range

    try:
        #通过获取上面的page参数，查询此page是否为整数并且是否可用
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except (EmptyPage, InvalidPage):
        contacts = paginator.page(paginator.num_pages)

    black_top, white_top = {}, {}
    

    for key in black_list:
        src_list, tem, dst_list = key.name.partition("->")
        
        src_ip, sign, src_port = src_list.partition("-")
        dst_ip, sign, dst_port = dst_list.partition("-")
        if src_ip not in black_top.keys():
            black_top[src_ip] = 1
        else:
            black_top[src_ip] += 1
        if dst_ip not in black_top.keys():
            black_top[dst_ip] = 1
        else:
            black_top[dst_ip] += 1

    for key in white_list:    
        if src_ip not in white_top.keys():
            white_top[src_ip] = 1
        else:
            white_top[src_ip] += 1
        if dst_ip not in white_top.keys():
            white_top[dst_ip] = 1
        else:
            white_top[dst_ip] += 1
    ip_attack_num, ip_normal_num = len(black_top.keys()), len(white_top.keys())
    ip_tot_num = ip_attack_num + ip_normal_num


    black_order = sorted(black_top.items(), key = lambda x:x[1], reverse=True)
    black_len = len(black_order)
    black_top10 = []
    class black_sample(object):
        def __init__(self, ip, num):
            super().__init__()
            self.ip = ip
            self.num = num

    for i in range(min(4, black_len)):
        black_top10.append(black_sample(black_order[i][0], black_order[i][1]))
    
    while len(black_top10)<4:
        black_top10.append(black_sample("###", 0))
    

    import os
    if os.path.exists("restore.txt"):
        with open("restore.txt", "r") as f:
            record = f.readline()
        f.close()
        with open("restore.txt", "w+") as f:
            f.writelines([str(pcap_num), ' ', str(flow_num), ' ', str(num_black), ' ', str(num_white)])    
        f.close()
        
        record_old = record.split(' ')
        record_new = [pcap_num, flow_num, num_black, num_white]
        restore = []
        
        for i in range(4):
            r_1 = int(record_old[i])
            r_2 = record_new[i]
            
            if r_1 == 0:
                restore.append(0)
            else:
                restore.append(int((r_2 - r_1)/r_1 * 100))
    else:
        with open("restore.txt", "w") as f:
            f.writelines([str(pcap_num), ' ', str(flow_num), ' ', str(num_black), ' ', str(num_white)])  
        f.close() 
        restore = [0, 0, 0, 0] 
    return render(request, "home_new/index.html", {'subject_list': contacts,
                                                     'page_range':pageRange, 
                                                     'num_black':num_black,
                                                     'num_white':num_white,
                                                     'num_tot':num_black + num_white,
                                                     'now':page,
                                                     'black_1':black_top10[0],
                                                     'black_2':black_top10[1],
                                                     'black_3':black_top10[2],
                                                     'black_4':black_top10[3],
                                                     'ip_attack_num':ip_attack_num,
                                                     'ip_tot_num':ip_tot_num,
                                                     'pcap_num':pcap_num,
                                                     'flow_num':flow_num,
                                                     'r_0':restore[0],
                                                     'r_1':restore[1],
                                                     'r_2':restore[2],
                                                     'r_3':restore[3]
    })