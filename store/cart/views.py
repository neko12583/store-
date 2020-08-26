import redis
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from cart.models import Cart

# Create your views here.
r = redis.Redis(host='*', port=6379, password='123456', db=1)


def cartview(request):
    user_id = request.POST.get('uid')
    cache_key = 'user:%s' % user_id
    commoditys = Cart.objects.filter(user_id=user_id)
    if r.exists(cache_key):
        commoditys = r.hgetall(cache_key)
        commoditys_dict = {m.decode(): v.decode() for m, v in commoditys.items()}
        return render(request, 'cart/index', locals())
    else:
        commoditys_dict={}
        for n in commoditys:
            commoditys_dict[n.commoditysid]=n.count
        return render(request, 'cart/index', locals())


def addcart(request):
    user_id = request.POST.get('uid')
    cache_key = 'user:%s' % user_id
    cid = request.POST.get('cid')
    count = request.POST.get('count')
    try:
        commodity = Cart.objects.get(user_id=user_id, commoditysid=cid)
    except Exception as e:
        print(e)
        Cart.objects.create(user_id=user_id, commoditysid=cid)
    else:
        commodity.count += 1
        commodity.save()
    if r.exists(cache_key):
        if r.hexists(cache_key, cid):
            r.hincrby(cache_key, cid, count)
        else:
            r.hset(cache_key, cid, count)
            r.expire(cache_key, 60 * 60 * 12)
    else:
        r.hset(cache_key, cid, count)
        r.expire(cache_key, 60 * 60 * 12)

    return HttpResponseRedirect(request.path)


def deletecart(request):
    user_id = request.POST.get('uid')
    cid = request.POST.get('cid')
    cache_key = 'user:%s' % user_id
    try:
        commodity = Cart.objects.get(user_id=user_id, commoditysid=cid)
        commodity.delete()
        r.delete(cache_key)
    except Exception as e:
        print(e)
        return HttpResponse('delete error')
    return HttpResponseRedirect('cart/index')


def updatecart(request):
    user_id = request.POST.get('uid')
    cache_key = 'user:%s' % user_id
    cid = request.POST.get('cid')
    count = request.POST.get('count')
    try:
        commodity = Cart.objects.get(user_id=user_id, commoditysid=cid)
    except Exception as e:
        print(e)
        return HttpResponse('error')
    commodity.count = count
    commodity.save()
    r.delete(cache_key)
    return HttpResponseRedirect('cart/index')
