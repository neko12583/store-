from django.http import JsonResponse
from django.conf import settings
import jwt
from ..user.models import UserAccount


def logging_check(func):
    def wrap(request, *args, **kwargs):
        # 获取请求头中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result = {'code': 403, 'error': 'please login'}
            return JsonResponse(result)
        # 校验token
        try:
            res = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithm='HS256')
        except Exception as e:
            print('check login is %s' % 3)
            result = {'code': 403, 'error': 'please login'}
            return JsonResponse(result)
        username = res['username']
        user = UserAccount.objects.get(username=username)
        request.myuser = user
        return func(request, *args, **kwargs)

    return wrap


def get_user_by_request(request):
    # 从token中解析出用户名【登录的用户】
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    try:
        res = jwt.decode(token, settings.JWT_TOKEN_KEY)
    except Exception as e:
        print('get user jwt error %s' % e)
        return None
    username = res['username']
    return username
