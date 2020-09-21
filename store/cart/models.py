from django.db import models
from user.models import UserAccount
from commodity.models import CommodityInfo


# Create your models here.
class Cart(models.Model):
    user_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    commodity_name = models.ForeignKey(CommodityInfo, on_delete=models.CASCADE)
    pound = models.IntegerField(verbose_name='磅数')
    count = models.IntegerField(verbose_name='商品数量')
    price = models.DecimalField(verbose_name='价格小计', max_digits=10, decimal_places=1)

    class Meta:
        db_table = 'cart'
        verbose_name = '购物车列表'
        verbose_name_plural = verbose_name

