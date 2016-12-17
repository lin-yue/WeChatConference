# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-14 17:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0003_auto_20161208_0004'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChoosedLoginParts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confid', models.CharField(max_length=128)),
                ('chooseParts', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='PriceInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confid', models.CharField(max_length=128)),
                ('price_discription', models.CharField(max_length=512)),
                ('price_amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Reminds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confid', models.CharField(max_length=128)),
                ('info', models.CharField(max_length=128)),
                ('publish_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserLoginDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('sex', models.IntegerField()),
                ('telphone', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=128)),
                ('checked_status', models.IntegerField()),
                ('login_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserLoginExtendAccomodation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accomodation_type', models.IntegerField()),
                ('basicInfo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wechat.UserLoginDetail')),
            ],
        ),
        migrations.CreateModel(
            name='UserLoginExtendAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.IntegerField()),
                ('address', models.CharField(max_length=256)),
                ('basicInfo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wechat.UserLoginDetail')),
            ],
        ),
        migrations.CreateModel(
            name='UserLoginExtendCompanyInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=128)),
                ('company_address', models.CharField(max_length=128, null=True)),
                ('company_job', models.CharField(max_length=128)),
                ('basicInfo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wechat.UserLoginDetail')),
            ],
        ),
        migrations.CreateModel(
            name='UserLoginExtendCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_type', models.IntegerField()),
                ('user_pay_status', models.IntegerField()),
                ('basicInfo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wechat.UserLoginDetail')),
                ('choosed_pay_models', models.ManyToManyField(to='wechat.PriceInfo')),
            ],
        ),
        migrations.CreateModel(
            name='UserLoginExtendExtraInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_discription', models.CharField(max_length=512)),
                ('basicInfo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wechat.UserLoginDetail')),
            ],
        ),
        migrations.CreateModel(
            name='UserLoginExtendMailcode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_code', models.CharField(max_length=64)),
                ('basicInfo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wechat.UserLoginDetail')),
            ],
        ),
        migrations.RenameField(
            model_name='user',
            old_name='student_id',
            new_name='system_id',
        ),
        migrations.AddField(
            model_name='user',
            name='pageNum',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='pageState',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userlogindetail',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wechat.User'),
        ),
        migrations.AddField(
            model_name='user',
            name='reminds',
            field=models.ManyToManyField(to='wechat.Reminds'),
        ),
    ]
