# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 07:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0004_supplier_user'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='suppliers.Supplier'),
        ),
    ]
