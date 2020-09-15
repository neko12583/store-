from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse


# Create your views here.
class OrderViews(View):
    # 生成订单请求
    def post(self, request):
        user_id = request.get('user_id')
        user_address = request.get('user_address')
        # commodity_data = {'commodity_id':[commodity_id1,commodity_id2...],
        # 'commodity_pound' :[pound1,pound2...],
        # 'commodity_number’：[commodity_number1,commodity_number2...],
        # }
        commodity_data = request.get('commodity_data')
        # 计算订单种每种商品的价格的价格：磅数价格*数量

        # 计算订单总价：每种商品的价格的和

        # 生成订单编号

        # 生成订单时间

        # 向数据库写入数据

        # 组织返回的数据：{用户id:用户id,订单状态：待支付，订单编号：生成的订单编号，商业数据：commodity_data，订单时间：生成的订单时间}

        # 返回json数据

    # 获取历史订单请求
    def get(self, request):
        pass

    # 取消订单请求
    def put(self, request):
        pass
