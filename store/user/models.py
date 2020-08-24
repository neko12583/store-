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

    def __str__(self):
        return "用户" + self.username


class UserDetails(models.Model):
    #  1男  2女
    gender = models.IntegerField('性别', default=0)
    realname = models.CharField('真实姓名', max_length=40)
    wechat = models.CharField('微信号', max_length=40)
    email = models.CharField('邮箱', max_length=40)
    nickname = models.CharField("昵称", max_length=40)
    mobile = models.IntegerField('手机号')
    # 自己-年份-月份-日
    birthdate = models.CharField('出生日期', max_length=40)
    address = models.CharField('收货地址', max_length=80)
    uid = models.OneToOneField(UserAccount, on_delete=models.CASCADE)

    class Meta:
        db_table = 'UserDetails'

    def __str__(self):
        return "姓名" + self.realname