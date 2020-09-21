from django.db import models
from user.models import UserAccount


# Create your models here.
class Status(models.Model):
    #     (1, '待支付'),
    #     (2, '待发货'),
    #     (3, '待收货'),
    #     (4, '已完成'),
    #     (5, '已取消'),
    order_status = models.CharField(verbose_name='订单状态', max_length=50)


class OrderInfo(models.Model):
    """订单模型类"""
    order_num = models.CharField(max_length=128, verbose_name='订单编号')
    total_price = models.DecimalField(verbose_name='订单总价', max_digits=10, decimal_places=1)
    order_time = models.CharField(verbose_name='下单时间', max_length=50)
    commodity_list = models.TextField(verbose_name='商品列表')
    user_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE)



