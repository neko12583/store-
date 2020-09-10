from django.db import models
from user.models import models, UserAccount
from commodity.models import ProductsCategory


# Create your models here.


class OrderInfo(models.Model):
    """订单模型类"""
    PAY_METHOD_CHOICES = (
        (1, '微信支付'),
        (2, '支付宝'),
    )
    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成'),
    )

    user_profile = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    total_count = models.IntegerField(default=1, verbose_name='商品总数')
    total_amount= models.DecimalField(verbose_name='商品总金额',decimal_places=2,max_length=10)
    order_id= models.CharField(max_length=128, primary_key=True, verbose_name='订单编号',default='')
    freight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='运费')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总价')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name='支付方式')
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
    order_time = models.DateTimeField('下单时间', auto_now_add=True)


    receiver=models.CharField(verbose_name='收件人',max_length=11)
    address = models.CharField(verbose_name='地址',max_length=100)
    receive_mobile =  models.CharField(verbose_name='收件人电话',max_length=11)
    tag= models.CharField(verbose_name='标签',max_length=10)

    class Meta:
        db_table = 'order_order_info'




class OrderGoods(models.Model):
    '''订单商品模型类'''
    order = models.ForeignKey('OrderInfo')
    sku = models.ForeignKey(ProductsCategory,on_delete=models.CASCADE)  #商品外键
    count = models.DecimalField(default=1, verbose_name='数量')
    price = models.DecimalField(max_length=10,decimal_places=2,verbose_name='单价')
    class Meta:
        db_table = 'order_order_goods'









