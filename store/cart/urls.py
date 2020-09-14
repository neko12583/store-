from django.contrib import admin
from django.urls import path

from cart import views

urlpatterns = [
    path('index', views.CartView.as_view()),
]