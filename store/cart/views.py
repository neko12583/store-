from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from cart.models import Cart
import redis

# Create your views here.
r = redis.Redis(host='*', port=6379, password='123456', db=1)


def cartview(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponse('请先登录')
    commoditys = Cart.objects.filter(userid=user.id)
    return render(request, 'cart/index', locals())


def addcart(request):
    uid=request.GET.get('uid')
    cid = request.GET.get('cid')
    try:
        commodity = Cart.objects.get(userid=uid, commoditysid=cid)
    except Exception as e:
        print(e)
        Cart.objects.create(userid=uid, commoditysid=cid)
    commodity.count+=1
    commodity.save()
    return HttpResponseRedirect(request.path)
