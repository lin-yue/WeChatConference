from codex.baseerror import *
from codex.baseview import APIView
from wechat.backInterface import *
from wechat.models import User


class UserBind(APIView):

    def validate_user(self):
        """
        input: self.input['student_id'] and self.input['password']
        raise: ValidateError when validating failed
        """
        raise NotImplementedError('You should implement UserBind.validate_user method')

    def get(self):
        self.check_input('openid')
        return User.get_by_openid(self.input['openid']).student_id

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        user = User.get_by_openid(self.input['openid'])
        self.validate_user()
        user.student_id = self.input['student_id']
        user.save()


class ConfDetail(APIView):

    def get(self):
        self.check_input('confid')
        info = confInfo(self.input['confid'])
        return info['data']

class JoinConf(APIView):

    def post(self):
        self.check_input('userid','confid','code')
        confinfo = confDetail(confid = self.input['confid'])
        if confinfo['data']['type'] == 0:
            result0 = joinConf(userid=self.input['userid'],confid=self.input['confid'],type=0 ,code = null)
            return result0
        if confinfo['data']['type'] == 1:
            result1 = joinConf(userid=self.input['userid'], confid=self.input['confid'], type=1, code=self.input['code'])
            return result1
        if confinfo['data']['type'] == 2:
            result2 = joinConf(userid=self.input['userid'], confid=self.input['confid'], type=2, code=self.input['code'])
            return result2
        if confinfo['data']['type'] == 3:
            result3 = joinConf(userid=self.input['userid'], confid=self.input['confid'], type=3, code=self.input['code'])
            return result3
        if confinfo['data']['type'] == 4:
            result4 = joinConf(userid=self.input['userid'], confid=self.input['confid'], type=4, code=self.input['code'])
            return result4