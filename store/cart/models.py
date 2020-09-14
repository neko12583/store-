from django.db import models
from user.models import UserAccount
from commodity.models import CommodityInfo


# Create your models here.
class Cart(models.Model):
    user_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    commoditysid = models.ForeignKey(CommodityInfo, on_delete=models.CASCADE)
    count = models.IntegerField('商品数量', default=1)

    class Meta:
        db_table = 'cart'
        verbose_name = '购物车列表'
        verbose_name_plural = verbose_name

