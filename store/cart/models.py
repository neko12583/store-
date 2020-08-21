from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField('用户名',max_length=30,unique=True)
    commodity=models.CharField('商品名称',max_length=30)
    count=models.IntegerField('数量')
