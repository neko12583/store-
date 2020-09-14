import json

import redis
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from tools.logging_dec import logging_check
from cart.models import Cart
from commodity.models import CommodityInfo

# Create your views here.
r = redis.Redis(host='*', port=6379, password='123456', db=1)

class CartView(View):
    @method_decorator(logging_check)
    def get(request):
        user = request.user
        cache_key = 'user:%s' % user.id
        commoditys = Cart.objects.filter(user_id=user.id)
        if r.exists(cache_key):
            commoditys = r.hgetall(cache_key)
            commoditys_dict = {m.decode(): v.decode() for m, v in commoditys.items()}
            return JsonResponse({'code': 200, 'data': commoditys_dict})
        else:
            for commodity in commoditys:
                good = {}
                good['name'] = CommodityInfo.objects.get(id=commodity.commoditysid).Name
                good['size'] = CommodityInfo.objects.get(id=commodity.commoditysid).Size
                good['price'] = CommodityInfo.objects.get(id=commodity.commoditysid).Price
                good['count'] = Cart.objects.get(user_id=user.id,
                                                 commoditysid=commodity.commoditysid).count
                good['total'] = int(good['price']) + int(good['count'])
                r.hmset(cache_key, mapping=good)
                return JsonResponse({'code': 200, 'data': good})


    @method_decorator(logging_check)
    def post(request):
        user = request.user
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
    def delete(request):
        user = request.user
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
    def put(request):
        user = request.user
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
