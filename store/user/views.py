import hashlib
import json
import random

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import UserAccount
from tools.sms import YunTongXun
from django.conf import settings


# 　返回注册页面
def register(request):
    return render(request, 'user/register.html')


# 注册
def register_ajax(request):
    username = request.GET['username']
    password_1 = request.GET['password_1']
    password_2 = request.GET['password_2']
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
        return HttpResponse('用户已存在')
    return HttpResponse("注册成功")


# 返回登录页面
def login_view(request):
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

# 正式登录
def login_ajax(request):
    username = request.GET['username']
    password = request.GET['password']
    print(username,password)
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


# 个人中心
def personal_center(request):
    return render(request, 'user/personal_center.html')


# 编辑资料
def edit_data(request):
    if request.method == "GET":
        return render(request, 'user/edit_data.html')
    elif request.method == "POST":
        pass
        # username = request.POST['username']
        # old_user = UserAccount.objects.filter(username=username)
        # if old_user:
        #     return HttpResponse("用户已存在")
        #
        # # hash算法加密
        # md5 = hashlib.md5()  # 拿到ｍd５对象
        # md5.update(password_1.encode())  # 把密码转成hash密码  参数只能传二进制数据
        # password_h = md5.hexdigest()  # 16进制加密     # password_h为加密之后的密码
        #
        # try:  # 防止上面查的时候该用户名没有注册，到了这一步正巧有人抢先注册了  因为username字段设置了unique=True唯一性，所以不能重复
        #     user = UserAccount.objects.create(username=username, password=password_h)
        # except Exception as e:
        #     print('create error is %s' % e)
        #     return HttpResponse('该用户已经被注册')
        # return HttpResponse("注册成功")



def sms_view(request):
    # 获取　{'phone':phone}
    json_str = request.body
    print(type(json_str))    # <class 'bytes'>
    json_obj = json.loads(json_str.decode())
    print(type(json_obj))   # <class 'dict'>
    phone = json_obj['phone']
    print(phone)
    cache_key = 'sms_%s'%phone
    # 查找缓存中有没有这个cache_key,防止用户多次点击按钮重复发送验证码
    old_code = cache.get(cache_key)
    # 如果已存在
    if old_code:
        result = {'code':10112,'error':'请勿重复发送'}
        return JsonResponse(result)
    code = random.randint(1000,9999)
    print(code)
    # 保存到redis缓存中
    cache.set(cache_key,code,65)
    a = cache.get(cache_key)
    print(a,'11111111111111111111111111111111111')
    #　同步发送
    x = YunTongXun(settings.SMS_ACCOUNT_ID,settings.SMS_ACCOUNT_TOKEN,settings.SMS_APP_ID,settings.SMS_TEMPLATE_ID)
    res = x.run('13713788072',code)    # 向指定手机发送指定验证码
    print(res,'2222222222222')  # 查看是否６个０　　６个０表示发送成功

    # 异步发送
    # send_sms.delay(phone,code)


    return JsonResponse({'code':200,'error':'出错啦'})