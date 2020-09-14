import json

import redis
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from tools.cache_dec import topic_cache
from tools.logging_dec import logging_check
from cart.models import Cart
from commodity.models import CommodityInfo

# Create your views here.
r = redis.Redis(host='*', port=6379, password='123456', db=1)

class CartView(View):
    @method_decorator(topic_cache(12*3600))
    @method_decorator(logging_check)
    def get(self,request):
        user = request.myuser
        goods = Cart.objects.filter(user_id=user.id)
        for commodity in goods:
            good = {}
            good['name'] = CommodityInfo.objects.get(id=commodity.commoditysid).Name
            good['size'] = CommodityInfo.objects.get(id=commodity.commoditysid).Size
            good['price'] = CommodityInfo.objects.get(id=commodity.commoditysid).Price
            good['count'] = Cart.objects.get(user_id=user.id,
                                             commoditysid=commodity.commoditysid).count
            good['total'] = int(good['price']) + int(good['count'])
            return JsonResponse({'code': 200, 'data': good})


    @method_decorator(logging_check)
    def post(self,request):
        user = request.myuser
        cache_key = 'user:%s' % user.id
        json_str = request.body
        json_obj = json.loads(json_str)
        cid = json_obj['cid']
        count = json_obj['count']
        if count == 0:
            return JsonResponse({'code': 10400, 'error': '数量不能为零'})
        try:
            commodity = Cart.objects.get(user_id=user.id, commoditysid=cid)
        except Exception as e:
            print(e)
            Cart.objects.create(user_id=user.id, commoditysid=cid)
        else:
            commodity.count += count
            commodity.save()
        r.delete(cache_key)
        return JsonResponse({'code': 200, 'success': '加车成功'})


    @method_decorator(logging_check)
    def delete(self,request):
        user = request.myuser
        cid = request.POST.get('cid')
        cache_key = 'user:%s' % user.id
        try:
            commodity = Cart.objects.get(user_id=user.id, commoditysid=cid)
            commodity.delete()
            r.delete(cache_key)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 10404, 'error': '删除失败'})
        return JsonResponse({'code': 200})


    @method_decorator(logging_check)
    def put(self,request):
        user = request.myuser
        cache_key = 'user:%s' % user.id
        json_str = request.body
        json_obj = json.loads(json_str)
        cid = json_obj['cid']
        count = json_obj['count']
        try:
            commodity = Cart.objects.get(user_id=user.id, commoditysid=cid)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 10404, 'error': '删除失败'})
        commodity.count = count
        commodity.save()
        r.delete(cache_key)
        return JsonResponse({'code': 200})
