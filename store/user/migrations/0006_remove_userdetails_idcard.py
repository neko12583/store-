# Generated by Django 2.2.13 on 2020-08-21 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_useraccount_nickname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='idcard',
        ),
    ]
