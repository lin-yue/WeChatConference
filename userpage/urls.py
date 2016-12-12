# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from userpage.views import *


__author__ = "Epsirom"


urlpatterns = [
    url(r'^user/bind/?$', UserBind.as_view()),
    url(r'^conf/detail/?$', ConfDetail.as_view()),
    url(r'^user/joinconf/?$', JoinConf.as_view()),
]
