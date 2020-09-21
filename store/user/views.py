import hashlib
import json
import random
from urllib.parse import urlencode

import requests
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import UserAccount, WeiboProfile, UserDetails
from .tasks import send_sms
from django.conf import settings
from tools.logging_dec import logging_check


# 　返回注册页面
def register(request):
    return render(request, 'user/register.html')


# 注册
def register_ajax(request):
    print('*'*10)
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
    print('/' * 10)
    print(password_h)

    try:  # 防止上面查的时候该用户名没有注册，到了这一步正巧有人抢先注册了  因为username字段设置了unique=True唯一性，所以不能重复
        user = UserAccount.objects.create(username=username, password=password_h)
        print(user)
    except Exception as e:
        print('create error is %s' % e)
        return HttpResponse('用户已存在')
    return HttpResponse("注册成功")


@logging_check
def login_view(request):
    return HttpResponse('您已登录!')


# 正式登录
def login_ajax(request):
    username = request.GET['username']
    password = request.GET['password']
    print(username, password)
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
    # else:
    #     resp.set_cookie("uid", old_user.id)
    #     resp.set_cookie("username", old_user.username)
    return resp

# 首页验证登录状态
def check_session(request):
    if 'username' in request.session or 'uid' in request.session:
        data = {"code": 200}
        return JsonResponse(data)
    else:
        data = {"code": 404}
    return JsonResponse(data)


# 注销
def logout_view(request):
    # 删除session
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    
    # 删除cookies
    # if 'username' in request.COOKIES:
    #     resp.delete_cookie('username')
    # if 'uid' in request.COOKIES:
    #     resp.delete_cookie('uid')
    # return render(request, 'index.html')
    return HttpResponseRedirect('/')


# 个人中心
@logging_check
def personal_center(request):
    uid = request.session.get('uid')
    username = request.session.get('username')
    print(uid, username)
    return render(request, 'user/personal_center.html')


# 编辑资料
@logging_check
def edit_data(request):
    # 检查session判断是否已登录，这个'username'和"uid"是下面生成的，是字典里的键，只是字符串
    if 'username' in request.session and "uid" in request.session:
        return render(request, 'user/edit_data.html')
    # 检查cookies　判断是否已登录  这个get里面的参数'username'和"uid"是下面生成的，是字典里的键，只是字符串
    username = request.COOKIES.get('username')
    uid = request.COOKIES.get('uid')
    if username and uid:  # 如果username和uid　不为空，说明获取到了  则更新一下session里面的username和uid
        # 　这里记住session回血一下
        # 存进django_session表里面两条数据{'username'：username}和{'uid'uid}，但是键和值都分别是长乱码
        request.session['username'] = username
        request.session['uid'] = uid
        return render(request, 'user/edit_data.html')
    # 证明没缓存，得重新登录
    return render(request, 'user/login.html')


def set_phone(request):
    return render(request, 'user/set_phone.html')


def save_phone(request):
    json_str = request.body
    json_obj = json.loads(json_str.decode())
    code = json_obj['code']
    phone = json_obj['phone']
    print('*' * 100, code, phone)
    cache_key = 'sms_%s' % phone
    old_code = str(cache.get(cache_key))
    if code == old_code:
        result = {'code': 200}
        # 先检查 该手机用户是否第一次进入我们的网站，如果第一次登录则存下来,外键可以暂时为空
        try:
            # 如果没报错，说明获取到了，说明这个用户之前已经注册过
            phone_user = UserDetails.objects.get(mobile=phone)
        except Exception as e:
            # 该用户手机第一次,所以插入表中
            username = '手机用户{}'.format(phone)
            password = phone
            # hash算法加密
            md5 = hashlib.md5()  # 拿到ｍd５对象
            md5.update(password.encode())  # 把密码转成hash密码  参数只能传二进制数据
            password_h = md5.hexdigest()  # 16进制加密     # password_h为加密之后的密码
            user = UserAccount.objects.create(username=username, password=password_h)
            print('-' * 100)
            phone_user = UserDetails.objects.create(mobile=phone, uid=user)
            print('+' * 100)
            uid = user.id
            # 在session保存登录状态
            request.session['uid'] = uid
            request.session['username'] = username
            print('+1' * 100)
            return JsonResponse({'code': 200})
        print('*' * 100)
        user = UserAccount.objects.get(id=phone_user.uid_id)
        print('+3' * 100)
        request.session['uid'] = phone_user.uid
        request.session['username'] = user.username
        print('+2' * 100)
        return JsonResponse({'code': 200})

    else:
        result = {'code': 10113, 'error': '输入的验证码有误'}
        return JsonResponse(result)


def sms_view(request):
    # 获取　{'phone':phone}
    json_str = request.body
    print(type(json_str))  # <class 'bytes'>
    json_obj = json.loads(json_str.decode())
    print(type(json_obj))  # <class 'dict'>
    phone = json_obj['phone']

    print(phone)

    print(phone, '*' * 100)

    cache_key = 'sms_%s' % phone
    # 查找缓存中有没有这个cache_key,防止用户多次点击按钮重复发送验证码
    old_code = cache.get(cache_key)
    print('+' * 100)
    # 如果已存在
    if old_code:
        result = {'code': 10112, 'error': '请勿重复发送'}
        return JsonResponse(result)
    code = random.randint(1000, 9999)
    print(code)
    # 保存到redis缓存中
    cache.set(cache_key, code, 65)
    a = cache.get(cache_key)
    print(a, '11111111111111111111111111111111111')
    # 　同步发送
    # x = YunTongXun(settings.SMS_ACCOUNT_ID,settings.SMS_ACCOUNT_TOKEN,settings.SMS_APP_ID,settings.SMS_TEMPLATE_ID)
    # res = x.run('13713788072',code)    # 向指定手机发送指定验证码
    # print(res,'2222222222222')  # 查看是否６个０　　６个０表示发送成功

    # 异步发送
    send_sms.delay(phone, code)

    return JsonResponse({'code': 200, 'error': '出错啦'})


def weibo_authorization(request):
    # 获取微博授权地址
    params = {
        'response_type': 'code',
        'client_id': settings.WEIBO_CLIENT_ID,
        'redirect_uri': settings.WEIBO_REDIRECT_URI  # 客户授权成功后跳转到哪个url,而且还得在微博那边设置一样的url
    }

    weibo_url = 'https://api.weibo.com/oauth2/authorize?'
    # a = {'name':'jay','age':18}
    # urlencode(a) 可以把字典类型的数据转换成查询字符串  'name=jay&age=18'
    url = weibo_url + urlencode(params)
    return JsonResponse({'code': 200, 'oauth_url': url})


def weibo_users(request):
    code = request.GET.get('code')
    print('这是从微博带回来的授权码code', code)
    # 给微博服务器发请求  用授权码交换用户的token
    token_url = 'https://api.weibo.com/oauth2/access_token'
    req_data = {
        'client_id': settings.WEIBO_CLIENT_ID,
        'client_secret': settings.WEIBO_CLIENT_SECRET,
        'grant_type': 'authorization_code',  # 固定写法
        'code': code,
        'redirect_uri': settings.WEIBO_REDIRECT_URI  # 客户授权成功后跳转到哪个url
    }
    response = requests.post(token_url, data=req_data)
    # 如果响应码是200
    if response.status_code == 200:
        res_data = json.loads(response.text)
    else:
        print('change code error ', response.status_code)
        return HttpResponse('微博错误1')
    if res_data.get('error'):
        print('change error', res_data.get('error'))
        return HttpResponse('微博错误2')
    print(res_data)  # expires_in  代表这个token的过期时间
    # {'access_token': '2.00Hl1zYCtNSelCf6c9dd91d22fKjlD', 'remind_in': '157679999',
    # 'expires_in': 157679999, 'uid': '2349278897', 'isRealName': 'true'}

    weibo_uid = res_data['uid']
    access_token = res_data['access_token']

    # 先检查 该微博用户是否第一次进入我们的网站，如果第一次登录则存下来,外键可以暂时为空
    try:
        # 如果没报错，说明获取到了，说明这个用户之前已经注册过
        weibo_user = WeiboProfile.objects.get(w_uid=weibo_uid)
        user = weibo_user.user_profile_id
    except Exception as e:
        # 该用户第一次登录,所以插入表中
        username = '微博用户_{}'.format(weibo_uid)
        password = weibo_uid
        # hash算法加密
        md5 = hashlib.md5()  # 拿到ｍd５对象
        md5.update(password.encode())  # 把密码转成hash密码  参数只能传二进制数据
        password_h = md5.hexdigest()  # 16进制加密     # password_h为加密之后的密码
        user = UserAccount.objects.create(username=username, password=password_h)
        print('-' * 100)
        WeiboProfile.objects.create(access_token=access_token, w_uid=weibo_uid, user_profile=user)
        print('+' * 100)
        uid = user.id
        # 在session保存登录状态
        request.session['uid'] = user.id
        request.session['username'] = username
        return render(request, 'user/callback.html', locals())
    print('*' * 100)
    # user = UserAccount.objects.get(id=uid)
    request.session['uid'] = user.id
    request.session['username'] = user.username
    return render(request, 'user/callback.html', locals())
