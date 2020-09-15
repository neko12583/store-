from django.urls import path
from . import views

urlpatterns = [
    # 生成订单请求
    path('order/make', views.OrderView.as_views()),
    #  获取历史订单请求
    path('order/get', views.OrderView.as_views()),
    #  取消订单请求
    path('order/revoke', views.OrderView.as_views()),
]