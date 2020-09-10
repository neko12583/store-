import datetime
import json

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from cart.views import cartview
from commodity.models import CommodityInfo
from user.models import UserDetails
from .models import OrderInfo
from django.conf import settings


class AdvanceView(View):
    def get_address(self, user_id):
        all_address = UserDetails.objects.filter(user_profile_id=user_id, is_active=True)
        # 默认地址要显示在所有地址最前面
        if not all_address:
            # 如果刚注册成没有地址，返回空
            return []

        address_default = []
        address_normal = []
        for addr in all_address:
            addr_dic = {
                'id': addr.id,
                'name': addr.receiver,
                'mobile': addr.receiver_mobile,
                'title': addr.tag,
                'address': addr.address
            }
            if addr.is_default:
                address_default.append(addr_dic)
            else:
                address_normal.append(addr_dic)
        return address_default + address_normal

    def get(self, request, username):
        user = request.myuser
        settlement = int(request.GET.get['settlement'])
        if settlement == 0:
            # 购物车点的　确认订单
            # 获取地址
            address_list = self.get_address(user.id)
            # 获取购物车中勾选的物品信息

            skus_list = 购物车返回的函数(user.id)
            selected_carts = [s for s in skus_list if s['selected'] == 1]
            data = {}
            data['addresses'] = address_list
            data['sku_list'] = selected_carts
            return JsonResponse({'code': 200, 'data': data, 'base_url': settings.PIC_URL})
        else:
            # 点了商品详情页中的立即购买进入确认订单
            pass


class OrderInfo(View):
    # 校验登录状态
    def post(self, request, username):
        user = request.myuser
        address_id = json.loads(request.body).get('address_id')
        try:
            address = UserDetails.objects.get(id=address_id, is_active=True)
        except Exception as e:
            return JsonResponse({'code': 10500, 'error': 'address is error'})

        # 开启事务
        with transaction.atomic():
            # 事务下的语句将会包裹在里面
            sid = transaction.savepoint()
            # 以当前状态设置一个节点,在某些特定情况下可以回滚到这里
            # 设置唯一订单　时间＋用户主键
            now = datetime.datetime.now()
            order_id = "%s%02d" % (now.strftime('%Y%m%d%h%m%s'), user.id)
            order = OrderInfo.objects.create(
                order_id=order_id,
                user_profile=user,
                address=address.address,
                receiver=address.receiver,
                receiver_mobile=address.receiver_mobile,
                tag=address.tag,
                total_amount=0,
                total_count=0,
                freight=10,
                pay_method=1,
                status=1
            )
            # 把购物车要购买的数据函数调包
            cares_obj = 取出购物车数据()
            all_carts = cares_obj.get_carts_all_data(user.id)
            carts_data = {k: v for k, v in all_carts.items() if v[1] == 1}
            skus = 购物车models.objects.filter(id_in=carts_data.keys())
            for sku in skus:
                carts_count = int(carts_data[sku.id][0])
                if sku.stock < carts_count:
                    # 如果库存不够　　回滚　回滚到上个节点
                    transaction.savepoint_rollback(sid)
                    return JsonResponse({'code': 10501, 'error': 'stock error'})

                # 修改库存
                old_version = CommodityInfo.version
                result = CommodityInfo.objects.filter(
                    id=CommodityInfo.id,
                    version=old_version).update(stock=CommodityInfo.数量 - carts_count,
                                                sales=CommodityInfo.sales + carts_count, version=old_verson + 1)
                if result ==0:
                    transaction.savepoint_rollback(sid)
                    return JsonResponse({'code':10502,'error':'库存有变化，请稍后再试'})