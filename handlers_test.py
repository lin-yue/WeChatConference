from django.test import TestCase
import adminpage.urls
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from codex.baseerror import *
from unittest.mock import Mock, MagicMock, patch, NonCallableMock
from wechat.models import *
from wechat.handlers import *
from adminpage.views import *
from datetime import datetime
from django.utils import timezone
from django.utils.dateformat import format
from django.contrib.auth.models import User as DjangoUser
from WeChatTicket.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET, SITE_DOMAIN
from wechat.wrapper import WeChatLib
from wechat.views import CustomWeChatView
import urllib
import json
import os


class SubscribeHandler_test(TestCase):
    @classmethod
    def setUpClass(cls):
        super( SubscribeHandler_test, cls).setUpClass()
        cls.view = Mock()
        cls.view.event_keys = CustomWeChatView.event_keys
    def test_this_check(self):
        test = User.objects.create(open_id = "t",union_id = 'e',nickname ='s',headimgurl = 't',pageNum = 1,pageState = 1,searchWords = 'i',userid = '1')
        test.save()
        self.user = test
        self.input = dict(MsgType='event', Event='subscribe', EventKey='MORE_SEARCH', ToUserName="bb", FromUserName="cc")
        handler = SubscribeHandler(self.view, self.input, self.user)
        print(handler.check())


    def test_this_handle(self):
        test = User.objects.create(open_id="ophyUwgM0HfqOQvIdH6cqwa-PntE")
        test.save()
        self.user = test

        self.input =dict(ToUserName="bb", FromUserName="cc")

        handler = SubscribeHandler(self.view, self.input, self.user)
        print(handler.handle())

class SearchConfHandler_test(TestCase):
    @classmethod
    def setUpClass(cls):
        super( SearchConfHandler_test, cls).setUpClass()
        cls.view = Mock()
        cls.view.event_keys = CustomWeChatView.event_keys

    def test_this_handle(self):
        test = User.objects.create(userid="223")
        test.save()
        self.user = test

        self.input = dict(ToUserName="bb", FromUserName="cc",Content="会佳")

        handler = SearchConfHandler(self.view, self.input, self.user)
        print(handler.handle())

class SearchWaysHandler_test(TestCase):
    @classmethod
    def setUpClass(cls):
        super( SearchWaysHandler_test, cls).setUpClass()
        cls.view = Mock()
        cls.view.event_keys = CustomWeChatView.event_keys

    def test_this_handle(self):
        test = User.objects.create(
        open_id = "t",
        union_id = 'e',
        nickname ='s',
        headimgurl = 't',
        pageNum = 1,
        pageState = 1,
        searchWords = 'i',
        userid = '1')
        test.save()
        self.user = test
        self.input =dict(MsgType = 'event', Event = 'CLICK', EventKey ='more_search',ToUserName="bb",FromUserName="cc")
        handler = SearchWaysHandler(self.view,self.input,self.user)
        print(handler.handle())

    def test_this_check(self):
        test = User.objects.create(open_id = "t",union_id = 'e',nickname ='s',headimgurl = 't',pageNum = 1,pageState = 1,searchWords = 'i',userid = '1')
        test.save()
        self.user = test
        self.input = dict(MsgType='event', Event='CLICK', EventKey='MORE_SEARCH', ToUserName="bb", FromUserName="cc")
        handler = SearchWaysHandler(self.view, self.input, self.user)
        print(handler.check())

class myConferenceHandler_test(TestCase):
    @classmethod
    def setUpClass(cls):
        super( myConferenceHandler_test, cls).setUpClass()
        cls.view = Mock()
        cls.view.event_keys = CustomWeChatView.event_keys

    def test_this_handle(self):
        test = User.objects.create(userid="227")
        test.save()
        self.user = test
        self.input = dict(ToUserName="bb", FromUserName="cc",Content="会佳")
        handler = myConferenceHandler(self.view, self.input, self.user)
        print(handler.handle())

class allConferenceHandler_test(TestCase):
    @classmethod
    def setUpClass(cls):
        super( allConferenceHandler_test, cls).setUpClass()
        cls.view = Mock()
        cls.view.event_keys = CustomWeChatView.event_keys

    def test_this_handle(self):
        test = User.objects.create(userid="227")
        test.save()
        self.user = test
        self.input = dict(ToUserName="bb", FromUserName="cc")
        handler = allConferenceHandler(self.view, self.input, self.user)
        print(handler.handle())

class recentConferenceHandler_test(TestCase):
    @classmethod
    def setUpClass(cls):
        super( recentConferenceHandler_test, cls).setUpClass()
        cls.view = Mock()
        cls.view.event_keys = CustomWeChatView.event_keys

    def test_this_handle(self):
        test = User.objects.create(userid="227")
        test.save()
        self.user = test
        self.input = dict(ToUserName="bb", FromUserName="cc")
        handler = recentConferenceHandler(self.view, self.input, self.user)
        print(handler.handle())


class NextPageHandler_test(TestCase):
    @classmethod
    def setUpClass(cls):
        super( NextPageHandler_test, cls).setUpClass()
        cls.view = Mock()
        cls.view.event_keys = CustomWeChatView.event_keys

    def test_this_handle(self):
        test = User.objects.create(userid="227",pageState=1)
        test.save()
        self.user = test
        self.user.pageNum=0
        self.input = dict(ToUserName="bb", FromUserName="cc")
        handler = NextPageHandler(self.view, self.input, self.user)
        print(handler.handle())