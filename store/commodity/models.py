from django.db import models


# Create your models here.
class CommodityInfo(models.Model):
    name = models.CharField('商品名称', max_length=100)
    tips = models.CharField('商品小贴士', max_length=100)
    info = models.CharField('商品描述信息', max_length=200)
    price = models.DecimalField('商品价格', max_digits=10, decimal_places=1)
    imgurl = models.CharField('图片路径', max_length=100)

    class Meta:
        db_table = 'CommodityInfo'
        verbose_name = '商品信息表'
        verbose_name_plural = verbose_name
