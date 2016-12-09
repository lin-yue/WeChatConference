from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from wechat.backInterface import *

class TestAjax(APIView):

    def get(self):
        response = allConfList(200,1,10)
        print(response['data'][0]['name'])
        return {'confname':response['data'][0]['name']}
