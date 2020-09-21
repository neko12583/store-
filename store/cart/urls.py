from django.contrib import admin
from django.urls import path
from cart import views

urlpatterns = [
    # 进入购物车页面
    path('get_html', views.get_html),
    # path('index', views.cartview),
    # 加入购物车
    path('add_cart', views.add_cart),
    # 删除单种商品
    path('del_cart', views.del_cart),
]