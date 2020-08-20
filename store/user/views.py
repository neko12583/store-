import hashlib

from django.http import HttpResponse
from django.shortcuts import render
from .models import UserAccount


# 注册
def register(request):
    if request.method == "GET":
        return render(request, 'user/register.html')
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


# 登录
def login_view(request):
    if request.method == "GET":
        # 检查session判断是否已登录，这个'username'和"uid"是下面生成的，是字典里的键，只是字符串
        if 'username' in request.session and "uid" in request.session:
            return HttpResponse('您已登录!')
        # 检查cookies　判断是否已登录  这个get里面的参数'username'和"uid"是下面生成的，是字典里的键，只是字符串
        username = request.COOKIES.get('username')
        uid = request.COOKIES.get('uid')
        if username and uid:  # 如果username和uid　不为空，说明获取到了  则更新一下session里面的username和uid
            # 　这里记住session回血一下
            # 存进django_session表里面两条数据{'username'：username}和{'uid'uid}，但是键和值都分别是长乱码
            request.session['username'] = username
            request.session['uid'] = uid
            return HttpResponse("你已经登录")
        return render(request, 'user/login.html')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            old_user = UserAccount.objects.get(username=username)  # 使用get没获取到　则会报错
        except Exception as e:
            print("login get error is %s" % e)
            return HttpResponse("用户名或密码错误")

        md5 = hashlib.md5()
        md5.update(password.encode())
        password_h = md5.hexdigest()
        if password_h != old_user.password:
            return HttpResponse("用户名或密码错误")
        resp = HttpResponse('登录成功')

        # 在session保存登录状态
        request.session['uid'] = old_user.id
        request.session['username'] = old_user.username

        # 根据用户的选择保存登录状态,是否勾选记住用户名
        if 'remember' in request.POST:  # 用户勾选了记住用户名点提交，提交过来的数据里才会有{remember:on}
            resp.set_cookie("uid", old_user.id, 3600 * 24 * 7)
            resp.set_cookie("username", old_user.username, 3600 * 24 * 7)
        return resp


# 注销
def logout_view(request):
    # 删除session
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']

    # 删除cookies
    resp = HttpResponse("已注销")
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')

    return resp