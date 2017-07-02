# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 01:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20170702_0145'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaseorderline',
            old_name='preorder',
            new_name='purchase_order',
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='title',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='标题'),
        ),
    ]