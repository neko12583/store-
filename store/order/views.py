import json

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from tools.logging_dec import logging_check
from cart.models import Cart
from order.models import OrderInfo, Status
import time
import datetime


# Create your views here.
# 生成订单请求
@logging_check
def add_order(request):
    user_id = request.session.get('uid')
    # 获取该用户的购物车
    cart_obj = Cart.objects.filter(user_id=user_id)
    # 得到的是一个查询集
    total_price = 0
    commodity_list = []
    for item in cart_obj:
        # 计算订单总价：每种商品的价格的和
        total_price += item.price
        # 得到订单所有商品名列表
        commodity_list.append(
            {"commodity_name": item.commodity_name.name, "pound": item.pound, "count": item.count, "price": item.price})
    # 生成订单编号: uid + 时间戳%1
    order_num = user_id + int(time.time() // 1)
    # 生成订单时间
    order_time = str(datetime.datetime.now().year) + "/" + str(datetime.datetime.now().month) + "/" + str(
        datetime.datetime.now().day)
    # 向数据库写入订单数据
    order_obj = OrderInfo.objects.create(order_num=order_num, total_price=total_price, order_time=order_time, status_id_id=1, user_id_id=user_id, commodity_list=commodity_list)
    # 订单状态
    order_status = "待支付"
    # 清空该用户的购物车
    cart_obj = Cart.objects.filter(user_id=user_id)
    cart_obj.delete()
    # 组织返回的数据：{用户id:用户id,订单状态：待支付，订单编号：生成的订单编号，商品数据：commodity_dat，订单时间：生成的订单时间}
    return render(request, 'order.html', locals())


# 获取历史订单请求
@logging_check
def get_order(request):
    user_id = request.session.get('uid')
    # 查询该用户的所有订单
    order_obj = OrderInfo.objects.filter(user_id=user_id)
    data = []
    for item in order_obj:
        # order_status = Status.objects.get(id=item.status_id)
        order_status = item.status_id.order_status
        data.append({"order_num": item.order_num, "total_price": item.total_price, "order_status": order_status,
                     "order_time": item.order_time})
    # 得到查询集
    # 组织数据：订单编号  订单总价  订单日期  订单状态
    return render(request, 'all_order.html', locals())


# 取消订单请求
def del_order(request):
    user_id = request.session.get('uid')
    if not user_id:
        return JsonResponse({'code': 101})
    json_str = request.body
    order_num = json.loads(json_str)['order_num']
    order_obj = OrderInfo.objects.get(order_num=order_num)
    order_obj.status_id_id = 5
    order_obj.save()
    return JsonResponse({'code': 200})


# @logging_check
# def order_info(request):
#     order_num = request.GET['order_num']
#     order_obj = OrderInfo.objects.get(order_num=order_num)
#     # 订单信息
#     order_num = order_obj.order_num
#     total_price = order_obj.total_price
#     order_status = order_obj.status_id.order_status
#     order_time = order_obj.order_time
#     # 商品信息
#     commodity_list = order_obj.commodity_list
#     print(commodity_list)
#     commodity_list = eval(commodity_list)
#     for item in commodity_list:
#         print(item)
#         print(item.commodity_name.name)
#         print(item.pound)
#         print(item.count)
#         print(item.price)
#     return render(request, 'order_info.html', locals())
