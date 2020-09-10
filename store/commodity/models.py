from django.db import models


# Create your models here.
class ProductsCategory(models.Model):
    CategoryName = models.CharField("类别名称", max_length=50)

    class Meta:
        db_table = 'ProductsCategory'
        verbose_name = '类别表'
        verbose_name_plural = '类别表'


class ImageInfo(models.Model):
    ImgUrl = models.CharField('大图片路径', max_length=100)
    ImgDesc = models.CharField('小图片路径', max_length=100)

    class Meta:
        db_table = 'ImageInfo'
        verbose_name = '图片表'
        verbose_name_plural = '图片表'


class CommodityInfo(models.Model):
    Name = models.CharField('商品名称', max_length=100)
    Info = models.CharField('商品描述信息', max_length=200)
    Material = models.CharField('商品原材料', max_length=100)
    Price = models.DecimalField('商品价格', max_digits=5, decimal_places=1)
    Size = models.DecimalField('商品磅数', max_digits=3, decimal_places=1)
    Cisrec = models.IntegerField('是否上架', default=True)
    Sell = models.IntegerField('商品销售量', default=0)
    Best = models.IntegerField('好评数', default=0)
    Badc = models.IntegerField('差评数', default=0)
    ProductsCategory = models.ForeignKey(ProductsCategory, on_delete=models.CASCADE)
    ImageInfo = models.ForeignKey(ImageInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'CommodityInfo'
        verbose_name = '商品表'
        verbose_name_plural = '商品表'
