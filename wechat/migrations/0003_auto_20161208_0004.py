# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-07 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0002_auto_20160502_1529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='activity',
        ),
        migrations.AlterField(
            model_name='user',
            name='student_id',
            field=models.CharField(max_length=32, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
