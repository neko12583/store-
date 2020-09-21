from django.shortcuts import render
from django.http import JsonResponse
from commodity.models import CommodityInfo


def commodity_info(request, commodity_name):
    commodity_all = CommodityInfo.objects.all()
    for commodity_obj in commodity_all:
        if commodity_obj.name == commodity_name:
            commodity_info = commodity_obj.info
            commodity_pic_address = commodity_obj.imgurl
            commodity_price = commodity_obj.price
            result = {'commodity_name': commodity_name, 'commodity_info': commodity_info,
              'commodity_pic_address': commodity_pic_address,'commodity_price':commodity_price}
            return render(request, 'pay.html', locals())

    
    
    

    # commodity_obj = CommodityInfo.objects.filter(commodity_name = commodity_name)
    # commodity_info = commodity_obj.info
    # commodity_price = commodity_obj.price
    # commodity_imgurl = commodity_obj.imgurl
    # data = {'commodity_name':commodity_name,'commodity_info':commodity_info,'commodity_price':commodity_price,'commodity_imgurl':commodity_img}
    # return render(request, 'pay.html', locals())









# import os

# from cairo._cairo import Content
# from django.conf import settings
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt

# from .models import CommodityInfo, ProductsCategory, ImageInfo


# # Create your views here.
# # 类别列表
# def productscategory_list(request):
#     productscategory_list = ProductsCategory.objects.filter(is_active=True)
#     return render(request, 'commodity/productscategory_list.html', locals())


# # 新增类别
# @csrf_exempt
# def productscategory_add(request):
#     if request.method == "GET":
#         return render(request, 'commodity/productscategory_add.html')
#     elif request.method == "POST":
#         CategoryName = request.POST['CategoryName']
#         try:
#             ProductsCategory.objects.create(CategoryName=CategoryName)
#         except Exception as e:
#             print('create error %s' % e)
#             return HttpResponse('create productscategory error')
#     return HttpResponseRedirect('/commodity/productscategory_list')


# # 删除类别
# def productscategory_delete(request):
#     pid = request.GET.get('pid')
#     if not pid:
#         return HttpResponse('--pid error--')
#     try:
#         productscategory = ProductsCategory.objects.get(id=pid, is_active=True)
#     except Exception as e:
#         print("get ProductsCategory error %s" % e)
#         return HttpResponse('get productscategory error')
#     productscategory.is_active = False
#     productscategory.save()
#     return HttpResponseRedirect('/commodity/productscategory_list')


# # 修改类别
# def productscategory_update(request, pid):
#     try:
#         productscategory = ProductsCategory.objects.get(id=pid, is_active=True)
#     except Exception as e:
#         print("get productscategory error %s" % e)
#         return HttpResponseRedirect('get productscategory error')
#     if request.method == "GET":
#         return render(request, 'commodity/productscategory_update.html', locals())
#     elif request.method == "POST":
#         CategoryName = request.POST['CategoryName']
#         productscategory.CategoryName = CategoryName
#         productscategory.save()
#         return HttpResponseRedirect('/commodity/productscategory_list')


# # 图片列表
# def Images_list(request):
#     Images_list = ImageInfo.objects.filter(is_active=True)
#     return render(request, 'commodity/Images_list.html', locals())

# # 添加大图片
# @csrf_exempt
# def MaxImages_add(request):
#     if request.method == 'GET':
#         return render(request, 'commodity/MaxImages_add.html')
#     elif request.method == 'POST':
#         title = request.POST['title']
#         a_file = request.FILES['myfile']
#         ImageInfo.objects.create(ImageName=title, ImgUrl=a_file)
#         return HttpResponse('upload success:%s,%s' % (a_file.name, title))


# # 添加小图片
# @csrf_exempt
# def MinImages_add(request):
#     if  request.method == 'GET':
#         return render(request, 'commodity/MinImages_add.html')
#     elif request.method == 'POST':
#         title = request.POST['title']
#         a_file = request.FILES['myfile']
#         ImageInfo.objects.create(ImageName=title, ImgDesc=a_file)
#         return HttpResponse('upload success:%s,%s' % (a_file.name, title))


# # 商品列表
# # 增加分页功能
# def commodity_list(request):
#     commodity_list = CommodityInfo.objects.filter(is_active=True)
#     # 每页显示的条数
#     paginator = Paginator(commodity_list, 10)
#     # 第几页
#     current_page = request.GET.get('page', 1)
#     # 页数转换为整数
#     current_page = int(current_page)
#     page = paginator.page(current_page)
#     # 展示当前页面的数据
#     commodity_list = paginator.get_page(current_page)
#     return render(request, 'commodity/commodity_list.html', locals())


# # 添加商品
# @csrf_exempt
# def commodity_add(request):
#     if request.method == 'GET':
#         return render(request, 'commodity/commodity_add.html')
#     elif request.method == 'POST':
#         name = request.POST['Name']
#         info = request.POST['Info']
#         material = request.POST['Material']
#         price = request.POST['Price']
#         size = request.POST['Size']
#         putaway = request.POST['Putaway']
#         version = request.POST['version']
#         sell = request.POST['Sell']
#         best = request.POST['Best']
#         badc = request.POST['Badc']
#         # productscategory = ProductsCategory.objects.get(id=pid)
#         try:
#             CommodityInfo.objects.create(Name=name, Info=info, Material=material,
#                                          Price=price, Size=size, Putaway=putaway,
#                                          version=version, Sell=sell, Best=best,
#                                          Badc=badc, ProductsCategory_id=1,
#                                          ImageInfo_id=2)
#         except Exception as e:
#             print('create error %s' % e)
#             return HttpResponse('create commodity error')
#     return HttpResponseRedirect('/commodity/commodity_list')


# # 删除商品信息
# def commodity_delete(request):
#     cid = request.GET.get('cid')
#     if not cid:
#         return HttpResponse('--cid error--')
#     try:
#         commodityinfo = CommodityInfo.objects.get(id=cid, is_active=True)
#     except Exception as e:
#         print('get commodityinfo error %s' % e)
#         return HttpResponse('get commodityinfo error ')
#     commodityinfo.is_active = False
#     commodityinfo.save()
#     return HttpResponseRedirect('/commodity/commodity_list')


# # 修改商品信息
# def commodity_update(request, cid):
#     try:
#         commodityinfo = CommodityInfo.objects.get(id=cid, is_active=True)
#     except Exception as e:
#         print("get commodityinfo error %s" % e)
#         return HttpResponseRedirect('get commodityinfo error')
#     if request.method == "GET":
#         return render(request, 'commodity/commodity_update.html', locals())
#     elif request.method == "POST":
#         Name = request.POST['Name']
#         Info = request.POST['Info']
#         CategoryName = request.POST['CategoryName']
#         # ImgUrl = request.POST['ImgUrl']
#         # ImgDesc = request.POST['ImgDesc']
#         Material = request.POST['Material']
#         Price = request.POST['Price']
#         Size = request.POST['Size']
#         Putaway = request.POST['Putaway']
#         commodityinfo.Name = Name
#         commodityinfo.Info = Info
#         commodityinfo.CategoryName = CategoryName
#         # commodityinfo.ImgUrl = ImgUrl
#         # commodityinfo.ImgDesc = ImgDesc
#         commodityinfo.Material =Material
#         commodityinfo.Price = Price
#         commodityinfo.Size = Size
#         commodityinfo.Putaway = Putaway
#         commodityinfo.save()
#         return HttpResponseRedirect('/commodity/commodity_list')


# # 加载商品分类
# def loadinfo(request):
#     context = {}
#     context['productscategory'] =ProductsCategory.objects.all()
#     return context


# # 首页商品展示
# def commodity_index(request, page=1):
#     commodity_list = CommodityInfo.objects.all()
#     # 分页
#     # 每页显示的条数
#     paginator = Paginator(commodity_list, 10)
#     # 第几页
#     current_page = request.GET.get('page', 1)
#     # 页数转换为整数
#     current_page = int(current_page)
#     page = paginator.page(current_page)
#     # 展示当前页面的数据
#     commodity_list = paginator.get_page(current_page)
#     return render(request, 'commodity/commodity_index.html', locals())


# #商品详情页面
# def commodity_info(request):
#     cid = request.GET.get('cid')
#     # 商品详情页
#     context = loadinfo(request)
#     # 加载商品详情信息
#     return render(request, 'commodity/commodity_info.html', locals())
