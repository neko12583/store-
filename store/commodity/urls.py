from django.urls import path
from . import views

urlpatterns = [
    # 商品详情页面请求
    path('pay/<str:commodity_name>', views.commodity_info),
]
