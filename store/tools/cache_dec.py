from .logging_dec import get_user_by_request
from django.core.cache import cache


def topic_cache(expire):
    def _topic_cache(func):
        def wrapper(request, *args, **kwargs):
            username = get_user_by_request(request)
            cache_key='user:%s'%username
            print('--cache key is %s' % (cache_key))
            # 以下代码体现我们学习过的缓存思想
            res = cache.get(cache_key)
            if res:
                print('--cache in--')
                return  res
            # 缓存中无数据，调用视图函数走视图
            res = func(request, *args, **kwargs)
            # 视图结果保存到缓存中
            cache.set(cache_key,res,expire)
            return res

        return wrapper

    return _topic_cache
