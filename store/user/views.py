import hashlib

from django.http import HttpResponse
from django.shortcuts import render
from .models import UserAccount

# Create your views here.

# 登录
def login(request):
    return None

# 注册
def register(request):
    if request.method == "GET":
        return render(request,'user/register.html')
    elif request.method == "POST":
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']
        if not username or not password_1:
            return HttpResponse('用户名或密码不能为空')
        if password_1 != password_2:
            return HttpResponse('两次密码不一致')
        old_user = UserAccount.objects.filter(username=username)
        if old_user:
            return HttpResponse("用户已存在")

        # hash算法加密
        md5 = hashlib.md5()  # 拿到ｍd５对象
        md5.update(password_1.encode())  # 把密码转成hash密码  参数只能传二进制数据
        password_h = md5.hexdigest()  # 16进制加密     # password_h为加密之后的密码

        try:  # 防止上面查的时候该用户名没有注册，到了这一步正巧有人抢先注册了  因为username字段设置了unique=True唯一性，所以不能重复
            user = UserAccount.objects.create(username=username, password=password_h)
        except Exception as e:
            print('create error is %s' % e)
            return HttpResponse('该用户已经被注册')
        return HttpResponse("注册成功")
