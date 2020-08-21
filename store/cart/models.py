from django.db import models
from user.models import UserAccount
from commodity.models import CommodityInfo

# Create your models here.
class Cart(models.Model):
    user_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE,varbose_name='用户id')
    commoditysid = models.ForeignKey(CommodityInfo, on_delete=models.CASCADE,varbose_name='商品id')
    count = models.IntegerField('商品数量', default=1)

    class Meta:
        db_table = 'cart'
        varbose_name = '购物车列表'
        varbose_name_plural = varbose_name
