# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-31 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0011_choosedsignupparts_maxjoinnum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='headimgurl',
            field=models.CharField(max_length=512),
        ),
    ]