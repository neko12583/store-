from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render


# 装饰器
def logging_check(func):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session or "uid" not in request.session:
            username = request.COOKIES.get('username')
            uid = request.COOKIES.get('uid')
            if not (username and uid):
                return render(request, 'user/login.html')
            else:
                request.session['username'] = username
                request.session['uid'] = uid
        a = request.session
        return func(request, *args, **kwargs)

    return wrap
