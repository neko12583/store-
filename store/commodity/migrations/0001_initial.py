# Generated by Django 2.2.13 on 2020-08-28 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ImgUrl', models.CharField(max_length=100, verbose_name='大图片路径')),
                ('ImgDesc', models.CharField(max_length=100, verbose_name='小图片路径')),
            ],
            options={
                'verbose_name': '图片表',
                'verbose_name_plural': '图片表',
                'db_table': 'ImageInfo',
            },
        ),
        migrations.CreateModel(
            name='ProductsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '类别表',
                'verbose_name_plural': '类别表',
                'db_table': 'ProductsCategory',
            },
        ),
        migrations.CreateModel(
            name='CommodityInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(default='', max_length=100, verbose_name='商品名称')),
                ('Info', models.CharField(max_length=200, verbose_name='商品描述信息')),
                ('Material', models.CharField(default='', max_length=100, verbose_name='商品原材料')),
                ('Price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='商品价格')),
                ('Size', models.DecimalField(decimal_places=1, default=0.0, max_digits=2, verbose_name='商品尺寸')),
                ('Cisrec', models.IntegerField(default=True, verbose_name='是否推荐')),
                ('Sell', models.IntegerField(default=0, verbose_name='商品销售量')),
                ('Best', models.IntegerField(default=0, verbose_name='好评数')),
                ('Badc', models.IntegerField(default=0, verbose_name='差评数')),
                ('ImageInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commodity.ImageInfo')),
                ('ProductsCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commodity.ProductsCategory')),
            ],
            options={
                'verbose_name': '商品表',
                'verbose_name_plural': '商品表',
                'db_table': 'CommodityInfo',
            },
        ),
    ]
