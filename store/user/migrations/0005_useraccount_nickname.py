# Generated by Django 2.2.13 on 2020-08-20 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_useraccount_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='nickname',
            field=models.CharField(default=models.CharField(max_length=40, unique=True, verbose_name='用户名'), max_length=40, verbose_name='昵称'),
        ),
    ]