from django.db import models


# Create your models here.
class Cart(models.Model):
    userid = models.ForeignKey('用户id', UserAccount, on_delete=models.CASCADE)
    commoditysid = models.ForeignKey('商品id', CommodityInfo, on_delete=models.CASCADE)
    count = models.IntegerField('商品数量', default=1)

    class Meta:
        db_table = 'cart'
        varbose_name = '购物车列表'
        varbose_name_plural = varbose_name
