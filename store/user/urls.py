from django.urls import path
from . import views

urlpatterns = [
    # 127.0.0.1:8000/user/register
    path('register', views.register),
    # 127.0.0.1:8000/user/register_ajax
    path('register_ajax', views.register_ajax),

    # 127.0.0.1:8000/user/login
    path('login', views.login_view),
    # 127.0.0.1:8000/user/login_ajax
    path('login_ajax', views.login_ajax),

    # 首页验证登录状态
    path('check_session', views.check_session),

    # 127.0.0.1:8000/user/logout
    path('logout', views.logout_view),

    # 进到欢迎回来页面
    # 127.0.0.1:8000/user/personal_center
    path('personal_center', views.personal_center),

    # 127.0.0.1:8000/user/edit_data
    path('edit_data', views.edit_data),

    # 127.0.0.1:8000/user/edit_data_ajax
    path('edit_data_ajax', views.edit_data_ajax),

    # 127.0.0.1:8000/user/set_phone

    path('set_phone',views.set_phone),
    # 127.0.0.1:8000/user/set_phone_ajax
    path('set_phone_ajax',views.set_phone_ajax),


    # 127.0.0.1:8000/user/sms
    path('sms', views.sms_view),

    # 127.0.0.1:8000/user/save_phone
    # 检验短信验证码，并储存手机号
    path('save_phone',views.save_phone),

    # 微博相关
    # 127.0.0.1:8000/user/weibo/authorization
    path('weibo/authorization',views.weibo_authorization),

    # 127.0.0.1:8000/user/weibo/users
    path('weibo/users',views.weibo_users),

]
