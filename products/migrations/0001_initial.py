# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 01:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_created=True, verbose_name='创建时间')),
                ('title', models.CharField(default='', max_length=20, verbose_name='标题')),
                ('status', models.CharField(default='发布', max_length=10, verbose_name='状态')),
            ],
        ),
        migrations.CreateModel(
            name='PreOrderLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(default='', max_length=20, verbose_name='地区')),
                ('preorder', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='products.PreOrder')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20, verbose_name='名称')),
                ('image', models.CharField(default='', max_length=20, verbose_name='图片')),
                ('category', models.CharField(default='', max_length=20, verbose_name='类型')),
                ('location', models.CharField(default='', max_length=20, verbose_name='地区')),
                ('purchaser', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='clients.Purchaser')),
            ],
        ),
        migrations.AddField(
            model_name='preorderline',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
        migrations.AddField(
            model_name='preorderline',
            name='purchaser',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='clients.Purchaser'),
        ),
    ]
