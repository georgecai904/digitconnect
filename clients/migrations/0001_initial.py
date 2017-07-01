# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-01 13:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(default='', max_length=20, verbose_name='价格')),
                ('amount', models.CharField(default='', max_length=20, verbose_name='数量')),
            ],
        ),
        migrations.CreateModel(
            name='Purchaser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20, verbose_name='名称')),
                ('phone', models.CharField(default='', max_length=20, verbose_name='电话')),
                ('address', models.CharField(default='', max_length=100, verbose_name='地址')),
                ('location', models.CharField(default='', max_length=20, verbose_name='区域')),
                ('license', models.CharField(default='', max_length=20, verbose_name='营业执照')),
                ('area', models.CharField(default='', max_length=20, verbose_name='领域')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20, verbose_name='名称')),
                ('phone', models.CharField(default='', max_length=20, verbose_name='电话')),
                ('address', models.CharField(default='', max_length=100, verbose_name='地址')),
                ('location', models.CharField(default='', max_length=20, verbose_name='区域')),
                ('license', models.CharField(default='', max_length=20, verbose_name='营业执照')),
                ('area', models.CharField(default='', max_length=20, verbose_name='领域')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
