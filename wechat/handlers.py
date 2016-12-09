# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
from wechat.backInterface import *

__author__ = "Epsirom"


class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，服务器现在有点忙，暂时不能给您答复 T T')


class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，没有找到您需要的信息:(')

class recentConferenceHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['recent_conference'])

    def handle(self):

        response = loginToChinaByWeixin(null,self.user.open_id, null, 0, null, null)
        response1 = upcomingConfList(response['data']['id'], 1, 10)
        if len(response1['data']) == 0:
            return self.reply_text("近期没有可参加的会议~")
        all_conferences = []
        for conf in response1['data']:
            all_conferences.append({
                    'Title': conf['name'],
                    #'Description': tickets[tic].activity.description,
                    'PicUrl': "http://60.205.137.139/adminweb/"+ conf['image'],
                    'Url': '',
            })
        return self.reply_news(all_conferences)

class allConferenceHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['more_history'])

    def handle(self):

        response = loginToChinaByWeixin(null,self.user.open_id, null, 0, null, null)
        response1 = allConfList(response['data']['id'], 1, 10)
        if len(response1['data']) == 0:
            return self.reply_text("当前还没有任何会议~")
        all_conferences = []
        for conf in response1['data']:
            all_conferences.append({
                    'Title': conf['name'],
                    #'Description': tickets[tic].activity.description,
                    'PicUrl': "http://60.205.137.139/adminweb/"+ conf['image'],
                    'Url': '',
            })
        return self.reply_news(all_conferences)


class myConferenceHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['my_conference'])

    def handle(self):

        response = loginToChinaByWeixin(null,self.user.open_id, null, 0, null, null)
        response1 = favoriteConfList(response['data']['id'], 1, 10)
        if len(response1['data']) == 0:
            return self.reply_text("当前您还没有参加或收藏任何会议~")
        all_conferences = []
        for conf in response1['data']:
            all_conferences.append({
                    'Title': conf['name'],
                    #'Description': tickets[tic].activity.description,
                    'PicUrl': "http://60.205.137.139/adminweb/"+ conf['image'],
                    'Url': '',
            })
        return self.reply_news(all_conferences)

class SubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_event('scan', 'subscribe')

    def handle(self):
        return self.reply_text("欢迎关注会佳~")



