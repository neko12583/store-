from django.conf.urls import url

from order import views

urlpatterns = [
    url(r'^order/(?P<page>\d+)$', views.AdvanceView.as_view()),
    # 用户中心-订单页
    url(r'^order/(?P<page>\d+)$', views.OrderInfo.as_view())
]

