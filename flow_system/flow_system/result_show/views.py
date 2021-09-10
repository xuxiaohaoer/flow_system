from django.shortcuts import render
from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, Paginator


def show_tls(request):
    from model_test.models import TlsRes
    black_list = TlsRes.objects.filter(result='black')
    num_black = len(black_list)
    white_list = TlsRes.objects.filter(result='white')
    num_white = len(white_list)
    #使用Paginator模块对数据分页，一页5条数据
    paginator = Paginator(black_list, 30)
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
    return render(request, "result_show/show_tls.html", {'subject_list': contacts,
                                                     'page_range':pageRange, 
                                                     'num_black':num_black,
                                                     'num_white':num_white,
                                                     'now':page,
    })


def show_MT(request):
    from model_test.models import ImageRes
    black_list = ImageRes.objects.filter(result='black')
    num_black = len(black_list)
    white_list = ImageRes.objects.filter(result='white')
    num_white = len(white_list)
    #使用Paginator模块对数据分页，一页5条数据
    paginator = Paginator(black_list, 30)
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
    return render(request, "result_show/show_tls.html", {'subject_list': contacts,
                                                     'page_range':pageRange, 
                                                     'num_black':num_black,
                                                     'num_white':num_white,
                                                     'now':page,
    })


def show_HAE(request):

    from model_test.models import FlowRes
    black_list = FlowRes.objects.filter(result='abnormal')
    num_black = len(black_list)
    white_list = FlowRes.objects.filter(result='normal')
    num_white = len(white_list)
    #使用Paginator模块对数据分页，一页5条数据
    paginator = Paginator(black_list, 30)
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
    return render(request, "result_show/show_HAE.html", {'subject_list': contacts,
                                                     'page_range':pageRange, 
                                                     'num_black':num_black,
                                                     'num_white':num_white,
                                                     'now':page,
    })
    