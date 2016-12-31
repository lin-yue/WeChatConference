from codex.baseerror import *
from codex.baseview import APIView
from wechat.backInterface import *
from wechat.models import *
from django.utils import timezone
from django.utils.dateformat import format


class CancelConf(APIView):

    def post(self):
        pass

class UserConfReminds(APIView):
    def get(self):
        self.check_input('userid')
        confList = myAllConfs(self.input['userid'])

        data=[]
        numConf = len(confList)
        for i in range(0,numConf):
            oneConfRemindsNum = len(Reminds.objects.filter(confid=confList[i]['id']))

            data.append({'confid':str(confList[i]['id']),'totalRemindsNum':oneConfRemindsNum, 'confName':confList[i]['name']})
        print(data)
        return data

class UserConfRemindsDetail(APIView):
    def get(self):
        self.check_input('confid')
        theInfo = confInfo(self.input['confid'])
        print(theInfo)
        allObj = Reminds.objects.filter(confid=self.input['confid'])
        alldata = []
        for i in allObj:
            alldata.append({"remind": i.info,"publishTime":format(i.publish_time,'U')})
        print(alldata)
        return {"confid": self.input["confid"], "reminds": alldata, "confname":theInfo['data']['basic']['name']}

"""
报名
"""
class SignUpConf(APIView):

    def get(self):

        all_user = UserSignUpDetail.objects.filter(confid=self.input['confid'])
        print(all_user)
        for user1 in all_user:
            if user1.user.userid == self.input['userid'] and user1.checked_status == 1:
                raise SignedUpError("审核通过")
            elif user1.user.userid == self.input['userid']:
                raise SignedUpError("用户正在等待审核")


#判断是否已经设置报名模块
        judge_module = ChoosedSignUpParts.objects.filter(confid=self.input['confid'])
#未设置报名模块，不能进行报名
        if len(judge_module) == 0:
            raise ModuleListIsNullError("当前会议尚未准备好报名，请稍后再试")
#已经设置报名模块，传modulelist给前端
        else:
            module = judge_module.get(confid=self.input['confid'])
            module_list = module.getSignUpParts()

#判断是否设置 price 信息
        judge_price = PriceInfo.objects.filter(confid=self.input['confid'])
        if len(judge_price) == 0:
            price_info = None
        else:
            price_list = PriceInfo.objects.filter(confid=self.input['confid'])
            price_info = []
            for price in price_list:
                elem={}
                elem["id"] = str(price.id)
                elem["name"] = price.price_description
                elem["money"] = str(price.price_amount)
                elem["select_id"] = "forpay_" + str(price.id)
                price_info.append(elem)

        return {"moduleList": module_list, "priceInfo": price_info}

    def post(self):
        print(self.input)
        all_user = UserSignUpDetail.objects.filter(confid=self.input['confid'])
        for user1 in all_user:
            if user1.user.userid == self.input['userid']:
                raise SignedUpError("The user has signed")

        user_detail = UserSignUpDetail()
        if "userid" in self.input:
            user_detail.user = User.objects.get(userid = self.input['userid'])
        if "confid" in self.input:
            user_detail.confid = self.input['confid']
        if "name" in self.input:
            user_detail.name = self.input['name']
        if "sex" in self.input:
            user_detail.sex = self.input['sex']
        if "telephone" in self.input:
            user_detail.telephone = self.input['telephone']
        if "email" in self.input:
            user_detail.email = self.input['email']

#waiting
        user_detail.checked_status = 3
        user_detail.signup_time = timezone.now()
        user_detail.save()

        # 判断是否已经设置报名模块
        judge_module = ChoosedSignUpParts.objects.filter(confid=self.input['confid'])

        # 未设置报名模块，不能进行报名
        if len(judge_module) == 0:
            raise ModuleListIsNullError("The conference has not set module.")
            # 已经设置报名模块，传modulelist给前端
        else:
            #module逻辑上是有一个confid
            module = judge_module.get(confid=self.input['confid'])
            module_list = module.getSignUpParts()

            # 判断是否设置 price 信息
            judge_price = PriceInfo.objects.filter(confid=self.input['confid'])
            if len(judge_price) == 0:
                price_list = []
            else:
                price_list = PriceInfo.objects.filter(confid=self.input['confid'])



# 国家地址

        if 1 in module_list:
            store1 = UserSignUpExtendAddress()
            store1.basicInfo = UserSignUpDetail.objects.get(user__userid=self.input['userid'],  confid = self.input['confid'])
            if "country" in self.input:
                store1.country = self.input["country"]
            if "address" in self.input:
                store1.address = self.input['address']
            store1.save()

#邮编
        if 2 in module_list:
            store2 = UserSignUpExtendPostcode()
            store2.basicInfo = UserSignUpDetail.objects.get(user__userid=self.input['userid'], confid = self.input['confid'])
            if "postcode" in self.input:
                store2.postcode = self.input['postcode']
            store2.save()

#公司
        if 3 in module_list:
            store3 = UserSignUpExtendCompanyInfo()
            store3.basicInfo = UserSignUpDetail.objects.get(user__userid=self.input['userid'], confid = self.input['confid'])
            if "company_name" in self.input:
                store3.company_name = self.input['company_name']
            if "company_address" in self.input:
                store3.company_address = self.input['company_address']
            if "company_job" in self.input:
                store3.company_job = self.input['company_job']
            store3.save()

#住宿类型 accommodation
        if 4 in module_list:
            store4 = UserSignUpExtendAccommodation()
            store4.basicInfo = UserSignUpDetail.objects.get(user__userid=self.input['userid'], confid = self.input['confid'])
            if "accommodation_type" in self.input:
                store4.accommodation_type = self.input['accommodation_type']
            store4.save()

#缴费
        if 5 in module_list:
            store5 = UserSignUpExtendCost()
            store5.basicInfo = UserSignUpDetail.objects.get(user__userid=self.input['userid'], confid = self.input['confid'])
            if "cost_type" in self.input:
                store5.cost_type = self.input['cost_type']
            if "user_pay_status" in self.input:
                store5.user_pay_status = self.input['user_pay_status']
            store5.save()
            #前端传 price_id 数组
            if "priceList" in self.input:
                price_list = self.input['priceList']
                theList = []
                if len(price_list) != 0:
                    for price_id in price_list:
                        tempt = PriceInfo.objects.get(id = int(price_id))
                        theList.append(tempt)
            store5.choosed_pay_models = theList
            store5.save()

#额外的个人介绍
        if 6 in module_list:
            store6 = UserSignUpExtendExtraInfo()
            store6.basicInfo = UserSignUpDetail.objects.get(user__userid=self.input['userid'], confid = self.input['confid'])
            if "extra_description" in self.input:
                store6.extra_description = self.input['extra_description']
            store6.save()








class ConfDetail(APIView):

    def get(self):
        self.check_input('confid')
        info = confInfo(self.input['confid'])
        if str(self.input['confid']) == str(1) or str(self.input['confid']) == str(3) or str(self.input['confid']) == str(10):
            info['data']['basic']['privateType'] = 2
        #info['data']['basic']['status'] = 2
        #myAllConfs(200)

        return info['data']

class JoinConf(APIView):

    def post(self):
        self.check_input('userid','confid','type','code')
        result = joinConf(self.input['userid'], self.input['confid'], self.input['type'], self.input['code'])
        return result
#new1 = ChoosedSignUpParts.objects.get(confid = "7")
#new1.setSignUpParts([1,2,3,4,5])
#new1.save()

