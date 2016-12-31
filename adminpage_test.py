from django.test import TestCase
import adminpage.urls
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from codex.baseerror import *
from unittest.mock import Mock, MagicMock, patch, NonCallableMock
from wechat.models import *
from adminpage.views import *
from datetime import datetime
from django.utils import timezone
from django.utils.dateformat import format
from WeChatTicket.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET, SITE_DOMAIN
from wechat.wrapper import WeChatLib
from wechat.views import CustomWeChatView
import urllib
import json
import os

class ConfSignUpMoudle_test(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ConfSignUpMoudle_test, cls).setUpClass()

        theParts = ChoosedSignUpParts()
        theParts.confid = 222
        theParts.maxJoinNum =1000
        theParts.setSignUpParts([1, 2, 3, 4, 5, 6])
        theParts.save()


    def test_this_get(self):
        response = self.client.get("/api/a/conf/signUpMoudle", {"confid":"222"})
        #print(response.json())
        self.assertEqual(response.json()['data']['moduleList'], [1,2,3,4,5,6])

    #def test_this_post(self):
        #response = self.client.post("/api/a/conf/signUpMoudle", {"confid":"222222","moduleList":["1","2","3","4","5"]})
        #print(response.json())


class PriceMoudle_test(TestCase):
    @classmethod
    def setUpClass(cls):
        super(PriceMoudle_test, cls).setUpClass()
        theParts = ChoosedSignUpParts()
        theParts.confid = 3
        theParts.maxJoinNum = 1000
        theParts.setSignUpParts([1, 2, 3, 4, 5, 6])
        theParts.save()

    def test_this_post(self):
        response = self.client.post("/api/a/conf/postFee", {"confid":"3","price_description":"保护费","price_amount":123})
        print(response.json())


class ConfMembers_test(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ConfMembers_test, cls).setUpClass()

        test = User()
        test.open_id = "t"
        test.union_id = 'e'
        test.nickname ='s'
        test.headimgurl = 't'
        test.pageNum = 1
        test.pageState = 1
        test.searchWords = 'i'
        test.userid = '1'
        test.save()

        test = User()
        test.open_id = "tt"
        test.union_id = 'ee'
        test.nickname ='s'
        test.headimgurl = 't'
        test.pageNum = 1
        test.pageState = 1
        test.searchWords = 'i'
        test.userid = '2'
        test.save()

        userinfo = UserSignUpDetail()
        userinfo.user = User.objects.get(userid = '1')
        userinfo.confid = '10'
        userinfo.sex = 1
        userinfo.name ="cc"
        userinfo.telephone = "1"
        userinfo.email ="110"
        userinfo.checked_status =1
        userinfo.signup_time = '2017-1-1 0:0:0'
        userinfo.save()

        userinfo = UserSignUpDetail()
        userinfo.user = User.objects.get(userid='2')
        userinfo.confid = '10'
        userinfo.sex = 1
        userinfo.name = "cc"
        userinfo.telephone = "1"
        userinfo.email = "110"
        userinfo.checked_status = 1
        userinfo.signup_time = '2017-1-1 0:0:0'
        userinfo.save()

    def test_this_get(self):
        response = self.client.get("/api/a/conf/confMembers", {"confid": "10"})
        print(response.json())


    def test_this_post(self):
        response = self.client.post("/api/a/conf/confMembers", {"confid": "10", "personList":[1,2] })
        print(response.json())


class ConfReminds_test(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ConfReminds_test, cls).setUpClass()
        remind1 = Reminds.objects.create(confid="3", info="you.", publish_time="2018-1-1 0:0:0")
        remind2 = Reminds.objects.create(confid="3", info="you!", publish_time="2018-1-1 0:0:1")
        remind1.save()
        remind2.save()
    def test_this_get(self):
        response = self.client.get("/api/a/conf/confReminds", {"confid": "3"})
        print(response.json())
    def test_this_post(self):
        response = self.client.post("/api/a/conf/confReminds", {"confid": "3","remind":"uuuu"})
        print(response.json())


class ConfMemberDetail_test(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ConfMemberDetail_test, cls).setUpClass()
        user = User.objects.create(userid="1")
        user.save()
        userinfo = UserSignUpDetail.objects.create(confid='1',user=user, sex = 0,checked_status=1,signup_time='2020-1-1 1:1:1')
        userinfo.save()
        moduleList = ChoosedSignUpParts()

        moduleList.confid='1'
        moduleList.setSignUpParts([1,2,3,4,5,6])
        moduleList.maxJoinNum =1000
        moduleList.save()
        priceinfo1=PriceInfo.objects.create(confid='1',price_description='fuck',price_amount=1111)
        priceinfo1.save()
        priceinfo2 = PriceInfo.objects.create(confid='1', price_description='fuck you', price_amount=11111)
        priceinfo2.save()
        store=UserSignUpExtendAddress.objects.create(basicInfo=userinfo,country=1,address= 'aderess')
        store.save()
        store2=UserSignUpExtendPostcode.objects.create(basicInfo=userinfo,postcode='10086')
        store2.save()
        store3=UserSignUpExtendCompanyInfo.objects.create(basicInfo=userinfo,company_name="移动")
        store3.save()
        store4=UserSignUpExtendAccommodation.objects.create(basicInfo=userinfo,accommodation_type=1)
        store4.save()
        store5=UserSignUpExtendCost.objects.create(basicInfo=userinfo,cost_type=1,user_pay_status=1)
        store5.save()
        store6=UserSignUpExtendExtraInfo.objects.create(basicInfo=userinfo,extra_description='extra_description')
        store6.save()


    def test_this_get(self):
        response = self.client.get("/api/a/conf/user/detail", {"confid": "1"})
        print(response.json())