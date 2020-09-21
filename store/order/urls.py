from django.urls import path
from . import views

urlpatterns = [
    # 生成订单请求
    path('add_order', views.add_order),
    #  获取历史订单请求
    path('get_order', views.get_order),
    #  取消订单请求
    path('del_order', views.del_order),
    # 订单详情
    # path('order_info', views.order_info),
]