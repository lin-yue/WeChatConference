# -*- coding: utf-8 -*-
#
import urllib.parse
import urllib.request
from wechat.wrapper import WeChatHandler
from wechat.backInterface import *
from wechat.models import *
from WeChatTicket.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET, SITE_DOMAIN
from wechat.wrapper import WeChatLib

__author__ = "Epsirom"


class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        self.changePageUserState()
        return self.reply_text('对不起，服务器现在有点忙，暂时不能给您答复 T T')


class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        self.changePageUserState()
        return self.reply_text('对不起，没有找到您需要的信息:(')

class NextPageHandler(WeChatHandler):

    def check(self):
        print(self.is_text("next") and not (self.user.pageState == User.PAGE_NOTLIST))
        print("pageState:")
        print(self.user.pageState)
        return self.is_text("next") and not (self.user.pageState == User.PAGE_NOTLIST)


    def handle(self):
        if self.user.pageState == self.user.PAGE_RECENTCONF:
            response1 = upcomingConfList(self.user.userid, self.user.pageNum, 9)    #pageToShow
            response2 = upcomingConfList(self.user.userid, self.user.pageNum + 1, 9)    #pageBefore
            return self.showPagesAndUpdateUserState(response1['data'], response2['data'], (self.user.pageNum + 1), response1['total_size'], CONFERENCELIST_RECENT)
        elif self.user.pageState == self.user.PAGE_ALLCONF:
            response1 = allConfList(self.user.userid, self.user.pageNum, 9)
            response2 = allConfList(self.user.userid, self.user.pageNum + 1, 9)
            return self.showPagesAndUpdateUserState(response1['data'], response2['data'], (self.user.pageNum + 1),response1['total_size'], CONFERENCELIST_ALL)
        elif self.user.pageState == self.user.PAGE_MYCONF:
            response1 = favoriteConfList(self.user.userid, self.user.pageNum, 9)
            response2 = favoriteConfList(self.user.userid, self.user.pageNum + 1, 9)
            return self.showPagesAndUpdateUserState(response1['data'], response2['data'], (self.user.pageNum + 1),response1['total_size'], CONFERENCELIST_MY)
        elif self.user.pageState == self.user.PAGE_ALLCONF:
            response1 = searchConfList(self.user.userid, self.user.pageNum, 9)
            response2 = searchConfList(self.user.userid, self.user.pageNum + 1, 9)
            return self.showPagesAndUpdateUserState(response1['data'], response2['data'], (self.user.pageNum + 1),response1['total_size'], CONFERENCELIST_SEARCH)
        else:
            return self.reply_text('对不起，没有找到要翻页对应的项目:(')





class recentConferenceHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['recent_conference'])

    def handle(self):


        response1 = upcomingConfList(self.user.userid, 1, 9)

        if len(response1['data']) == 0:
            self.changePageUserState()
            return self.reply_text("近期没有可参加的会议~")
        return self.showInitialPageAndUpdateUserState(response1['data'], response1['total_size'], CONFERENCELIST_RECENT, None)

class allConferenceHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['more_history'])

    def handle(self):

        response1 = allConfList(self.user.userid, 1, 9)
        if len(response1['data']) == 0:
            self.changePageUserState()
            return self.reply_text("目前还没有收录会议或会议历史已清空~")
        return self.showInitialPageAndUpdateUserState(response1['data'], response1['total_size'], CONFERENCELIST_ALL, None)


class myConferenceHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['my_conference'])

    def handle(self):

        response1 = favoriteConfList(self.user.userid, 1, 9)
        if len(response1['data']) == 0:
            self.changePageUserState()
            return self.reply_text("当前您还没有参加任何会议~")
        return self.showInitialPageAndUpdateUserState(response1['data'], response1['total_size'], CONFERENCELIST_MY, None)

class SearchWaysHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['more_search'])

    def handle(self):
        self.changePageUserState()
        return self.reply_text("请直接在输入框输入 “关键字”，其中“关键字”将在会议的名称、地点、标签信息中查找~")




class SearchConfHandler(WeChatHandler):

    def check(self):
        return self.is_msg_type('text')

    def handle(self):

        Content = self.input['Content']
        response1 = searchConfList(self.user.userid,Content,1,9)
        print(response1)
        if len(response1['data']) == 0:
            self.changePageUserState()
            return self.reply_text("没有找到符合搜索的会议~")
        return self.showInitialPageAndUpdateUserState(response1['data'], response1['total_size'], CONFERENCELIST_SEARCH, self.input['Content'])




#nickname,unionid,headimgurl,sex,location,languag
class SubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_event('scan', 'subscribe')

    #nickname, unionid, headimgurl, sex, location, language
    def handle(self):

        response = WeChatLib.getUnionId(self.user.open_id)
        print(response)

        self.user.headimgurl = response['headimgurl']
        self.user.nickname = response['nickname']
        self.user.union_id = response['unionid']
        #self.user.union_id = response['']
        response = loginToChinaByWeixin(self.user.nickname, self.user.union_id, response['headimgurl'], response['sex'], response['city'], response['language'])
        self.user.userid = response['data']['id']
        self.user.pageState = User.PAGE_NOTLIST
        self.user.save()
        return self.reply_text("欢迎关注会佳~")



