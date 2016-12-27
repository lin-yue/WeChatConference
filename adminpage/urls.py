# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from adminpage.views import *


__author__ = "Epsirom"


urlpatterns = [
    url(r'^conf/signUpMoudle/?$', ConfSignUpMoudle.as_view()),
    url(r'^conf/confMembers/?$', ConfMembers.as_view()),
    url(r'^conf/user/detail/?$', ConfMemberDetail.as_view()),
    url(r'^conf/confReminds?$', ConfReminds.as_view()),

]
