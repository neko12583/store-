from django.db import models
from user.models import UserAccount
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

    order_num = models.CharField(max_length=128, primary_key=True, verbose_name='订单编号')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='送货费用')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总价')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name='支付方式')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
    order_time = models.DateTimeField('下单时间', auto_now_add=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
