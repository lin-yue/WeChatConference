from codex.baseerror import *
from codex.baseview import APIView
from wechat.backInterface import *
from wechat.models import User


class CancelConf(APIView):

    def post(self):
        pass

class UserConfReminds(APIView):
    def get(self):
        pass

class UserConfRemindsDetail(APIView):
    def get(self):
        pass

class SignUpConf(APIView):

    def get(self):
        pass

    def post(self):
        pass

class ConfDetail(APIView):

    def get(self):
        self.check_input('confid')
        info = confInfo(self.input['confid'])
        #info['data']['basic']['privateType'] = 1
        #info['data']['basic']['status'] = 2
        #myAllConfs(200)

        return info['data']

class JoinConf(APIView):

    def post(self):
        self.check_input('userid','confid','type','code')
        result = joinConf(self.input['userid'], self.input['confid'], self.input['type'], self.input['code'])
        print(result)
        return result
