import redis
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from tools.logging_dec import logging_check
from cart.models import Cart
from commodity.models import CommodityInfo


# Create your views here.
# r = redis.Redis(host='*', port=6379, password='123456', db=1)

@logging_check
def get_html(request):
    user_id = request.session.get('uid')
    cart_data_obj = Cart.objects.filter(user_id_id=user_id)
    # 购物车中信息：[{commodity_name:xx,pound:xx,count:xx,price:xx},...]
    data = []
    for data_obj in cart_data_obj:
        data_dict = {'commodity_name': data_obj.commodity_name.name, 'pound': data_obj.pound, 'count': data_obj.count,
                     'price': data_obj.price}
        data.append(data_dict)

    return render(request, 'cart.html', locals())


# ajax请求，不能使用装饰器
def add_cart(request):
    user_id = request.session.get('uid')
    if not user_id:
        return JsonResponse({'code': 101})
    json_str = request.body
    # {'commodity_name': 'Gelato榴莲冰淇淋蛋糕', 'pound': 1, 'count': '2'， price:xx}
    json_obj = json.loads(json_str)
    commidity_obj = CommodityInfo.objects.filter(name=json_obj['commodity_name'])
    # 向购物车表写入user_name、commodity_name、pound、count
    cart_obj = Cart.objects.create(user_id_id=user_id, commodity_name_id=commidity_obj[0].id, pound=json_obj['pound'],
                                   count=json_obj['count'], price=json_obj['price'])
    return JsonResponse({'code': 200})


# 删除商品请求，ajax
def del_cart(request):
    user_id = request.session.get('uid')
    if not user_id:
        return JsonResponse({'code': 101})
    json_str = request.body
    c_name = json.loads(json_str)['c_name']
    c_id = CommodityInfo.objects.filter(name=c_name)[0].id
    c_obj = Cart.objects.get(commodity_name=c_id)
    c_obj.delete()
    data = {"code": 200}
    return JsonResponse(data)

# def cartview(request):
#     user_id = request.POST.get('uid')
#     cache_key = 'user:%s' % user_id
#     commoditys = Cart.objects.filter(user_id=user_id)
#     if r.exists(cache_key):
#         commoditys = r.hgetall(cache_key)
#         commoditys_dict = {m.decode(): v.decode() for m, v in commoditys.items()}
#         return render(request, 'cart/index', locals())
#     else:
#         commoditys_dict = {}
#         for n in commoditys:
#             commoditys_dict[n.commoditysid] = n.count
#         return render(request, 'cart/index', locals())


# def addcart(request):
#     user_id = request.POST.get('uid')
#     cache_key = 'user:%s' % user_id
#     cid = request.POST.get('cid')
#     count = request.POST.get('count')
#     try:
#         commodity = Cart.objects.get(user_id=user_id, commoditysid=cid)
#     except Exception as e:
#         print(e)
#         Cart.objects.create(user_id=user_id, commoditysid=cid)
#     else:
#         commodity.count += 1
#         commodity.save()
#     if r.exists(cache_key):
#         if r.hexists(cache_key, cid):
#             r.hincrby(cache_key, cid, count)
#         else:
#             r.hset(cache_key, cid, count)
#             r.expire(cache_key, 60 * 60 * 12)
#     else:
#         r.hset(cache_key, cid, count)
#         r.expire(cache_key, 60 * 60 * 12)

#     return HttpResponseRedirect(request.path)


# def deletecart(request):
#     user_id = request.POST.get('uid')
#     cid = request.POST.get('cid')
#     cache_key = 'user:%s' % user_id
#     try:
#         commodity = Cart.objects.get(user_id=user_id, commoditysid=cid)
#         commodity.delete()
#         r.delete(cache_key)
#     except Exception as e:
#         print(e)
#         return HttpResponse('delete error')
#     return HttpResponseRedirect('cart/index')


# def updatecart(request):
#     user_id = request.POST.get('uid')
#     cache_key = 'user:%s' % user_id
#     cid = request.POST.get('cid')
#     count = request.POST.get('count')
#     try:
#         commodity = Cart.objects.get(user_id=user_id, commoditysid=cid)
#     except Exception as e:
#         print(e)
#         return HttpResponse('error')
#     commodity.count = count
#     commodity.save()
#     r.delete(cache_key)
#     return HttpResponseRedirect('cart/index')
