# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from userpage.views import *


__author__ = "Epsirom"


urlpatterns = [
    url(r'^conf/detail/?$', ConfDetail.as_view()),
    url(r'^user/signUpConf/?$',SignUpConf.as_view()),
    url(r'^user/joinConf/?$',JoinConf.as_view()),
    url(r'^user/cancelConf/$', CancelConf.as_view()),
    url(r'^conf/confReminds/all/?$',UserConfReminds.as_view()),
    url(r'^conf/confReminds?$', UserConfRemindsDetail.as_view()),

]
