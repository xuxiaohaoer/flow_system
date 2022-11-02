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

    black_top = {}
    for key in black_list:
        src_list, tem, dst_list = key.name.partition("->")
        
        src_ip, sign, src_port = src_list.partition("-")
        dst_ip, sign, dst_port = dst_list.partition("-")
        if src_ip not in black_top.keys():
            black_top[src_ip] = 1
        else:
            black_top[src_ip] += 1
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
    })