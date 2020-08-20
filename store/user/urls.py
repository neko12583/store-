

from django.urls import path
from . import views

urlpatterns = [
    # 127.0.0.1:8000/user/register
    path('register', views.register),
    # 127.0.0.1:8000/user/login
    path('login',views.login_view),
    # 127.0.0.1:8000/user/register
    path('logout',views.logout_view),
]