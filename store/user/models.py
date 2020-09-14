from django.db import models


# Create your models here.


class UserAccount(models.Model):
    username = models.CharField("用户名", max_length=40, unique=True)
    password = models.CharField("密码", max_length=40)
    # 当对象第一次被创建时自动设置当前时间
    register_time = models.DateTimeField('注册时间', auto_now_add=True)
    # 每次保存对象时，自动设置该字段为当前时间
    last_visit_time = models.DateTimeField('最后访问时间', auto_now=True)

    class Meta:
        db_table = 'UserAccount'
        verbose_name = '账号信息'
        verbose_name_plural = '账号信息'


class UserDetails(models.Model):
    #  1男  2女
    gender = models.IntegerField('性别', default=0)
    realname = models.CharField('真实姓名', max_length=40,null=True)
    wechat = models.CharField('微信号', max_length=40,null=True)
    email = models.CharField('邮箱', max_length=40,null=True)
    nickname = models.CharField("昵称", max_length=40,null=True)
    mobile = models.CharField('手机号',max_length=20)
    # 自己-年份-月份-日
    birthdate = models.CharField('出生日期', max_length=40,null=True)
    address = models.CharField('收货地址', max_length=80,null=True)
    uid = models.OneToOneField(UserAccount, on_delete=models.CASCADE)

    class Meta:
        db_table = 'UserDetails'
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'


class WeiboProfile(models.Model):
    # 表一对一关联
    user_profile = models.OneToOneField(UserAccount,on_delete=models.CASCADE)
    # 微博的id
    w_uid = models.CharField(max_length=10, verbose_name='微博uid', unique=True)
    access_token = models.CharField(verbose_name='微博授权令牌', max_length=32)

    class Meta:
        db_table = 'user_weibo_profile'
