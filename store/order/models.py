from django.db import models
from django.contrib.postgres.fields import ArrayField



# Create your models here.
class Content(models.Model):
    O_Choices = (
        (1, "待支付"),
        (2, "待发货"),
        (3, "待收货"),
        (4, "待评价"),
        (5, "已完成"),
        (6, "已取消"),
    )

    O_Get =(
        (1, "自取"),
        (2, "快递"),
            )

    O_Pay=(
        (1, "支付宝"),
        (2, "微信"),
    )

    oway = models.CharField(verbose_name='订单id', max_length=50, property_key=True)
    onum = models.CharField('订单号', max_length=50)
    uid = models.CharField('用户', max_length=10)
    sid = models.CharField('商品', max_length=30)
    onumber = models.CharField('购买数量', max_length=50)
    osubtotal = models.DecimalField('小计',max_digits=10000,decimal_places=2)
    ostime = models.DateTimeField('下单时间', max_length=20, auto_now_add=True)
    ostatus = models.SmallIntegerField(verbose_name='订单状态',choices=O_Choices, max_length=10)
    opay = models.SmallIntegerField('支付方式',choices=O_Pay, max_length=10)
    odistribution = models.SmallIntegerField('取货方式',choices=O_Get, max_length=10)
    oetime = models.DateTimeField('配送/自取时间', max_length=20)

    # MEDIA_ROOT + myfile









