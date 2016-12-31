from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from wechat.backInterface import *
from wechat.wrapper import WeChatHandler
from wechat.models import *
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.utils.dateformat import format
from WeChatTicket import settings
from django.contrib.auth import authenticate, login
from django.contrib import auth



"""
发布者指定模块
"""
#网页测试get通过



class ConfSignUpMoudle(APIView):

    def get(self):
        self.check_input('confid')
        all_conf = allConfList(223, 1, 1000000000)
        flag = False
        for conf in all_conf["data"]:
            # print(conf['id'])
            if self.input["confid"] == str(conf['id']):
                flag = True
            # 判断是否已经设置报名模块
            judge_module = ChoosedSignUpParts.objects.filter(confid=self.input['confid'])

            if len(judge_module) == 0:
                module_list = None
                isSet = 0
                maxJoinNum = None
            else:
                module = judge_module.get(confid=self.input['confid'])
                module_list = module.getSignUpParts()
                isSet = 1
                maxJoinNum = module.maxJoinNum

            # 判断是否设置 price 信息
            judge_price = PriceInfo.objects.filter(confid=self.input['confid'])
            if len(judge_price) == 0:
                price_info = None
            else:
                price_list = PriceInfo.objects.filter(confid=self.input['confid'])
                price_info = []
                for price in price_list:
                    elem = {}
                    elem["id"] = price.id
                    elem["price_description"] = price.price_description
                    elem["price_amount"] = price.price_amount
                    price_info.append(elem)

            return {"moduleList": module_list, "priceInfo": price_info, "isSet" : isSet, "maxJoinNum" : maxJoinNum}
        if not flag:
            raise InputError("invalid confid")


    def post(self):
        self.check_input('confid')
        all_conf = allConfList(223, 1, 1000000000)
        flag = False
        for conf in all_conf["data"]:
            if self.input["confid"] == str(conf['id']):
                flag = True
                judge_module = ChoosedSignUpParts.objects.filter(confid=self.input['confid'])
                if len(judge_module) != 0:
                    raise InputError("报名模块已设置")
                else:
                    store_module = ChoosedSignUpParts()
                    store_module.confid = self.input['confid']
                    if len(self.input['moduleList']) > 6:
                        raise InputError("The size of moduleList must be less than 7.")
                    else:
                        for i in self.input['moduleList']:
                            if i not in [1, 2, 3, 4, 5, 6]:
                                raise InputError("wrong module id")
                        store_module.setSignUpParts(self.input["moduleList"])
                    store_module.maxJoinNum = int(self.input['maxJoinNum'])
                    store_module.save()
                if 5 in self.input['moduleList']:
                    store_price = PriceInfo()
                    store_price.confid = self.input['confid']
                    store_price.price_description = self.input['priceList'][0]['price_description']
                    store_price.price_amount = int(self.input['priceList'][0]['price_amount'])
                    store_price.save()
        if not flag:
            raise InputError("invalid confid")



class PriceMoudle(APIView):

    def post(self):
        self.check_input("confid","price_description","price_amount")
        all_conf=allConfList(223,1,1000000000)
        flag = False
        for conf in all_conf["data"]:
            if self.input["confid"]== str(conf['id']):
                flag = True
                store_price = PriceInfo()
                store_price.confid = self.input['confid']
                store_price.price_description = self.input['price_description']
                store_price.price_amount = int(self.input['price_amount'])
                store_price.save()
                tempt = ChoosedSignUpParts.objects.filter(confid=self.input['confid'])
                if len(tempt) == 1:
                    tempt = tempt.get(confid=self.input['confid'])
                    list1 = tempt.getSignUpParts()

                    if 5 not in list1:
                        list1.append(5)
                    tempt.setSignUpParts(list1)
                    tempt.save()
                elif len(tempt) == 0:
                    tempt = ChoosedSignUpParts()
                    tempt.confid = self.input['confid']
                    tempt.setSignUpParts([5])
                    tempt.save()
        if not flag:
            raise InputError("invalid confid")

"""
审核
"""
class ConfMembers(APIView):

    def get(self):
        self.check_input('confid')
        user_list = UserSignUpDetail.objects.filter(confid=self.input['confid'])
        #判断是否需要缴费
        judge_price = PriceInfo.objects.filter(confid=self.input['confid'])
        if len(judge_price) == 0:
            all_users = []

            for single_user in user_list:
                all_users.append({"userId": single_user.user.userid, "name": single_user.name, "signUpTime": format(single_user.signup_time,'U'),
                                  "checkedStatus": single_user.checked_status, "payStatus": None,"isPayBySystem": None})
        else:
            all_users = []
            for single_user in user_list:
                status1 = UserSignUpExtendCost.objects.filter(basicInfo__confid=self.input['confid'])
                status = status1.get(basicInfo__user__userid=single_user.user.userid)
                if status.user_pay_status == 1:
                    all_users.append({"userId": single_user.user.userid,"name":single_user.name, "signUpTime": format(single_user.signup_time,'U'),
                                        "checkedStatus": single_user.checked_status, "payStatus": 1,"isPayBySystem":1})
                else:
                    all_users.append({"userId": single_user.user.userid, "name": single_user.name, "signUpTime": format(single_user.signup_time,'U'),
                                        "checkedStatus": single_user.checked_status, "payStatus": 0, "isPayBySystem": 0})
        return all_users


    def post(self):
        self.check_input('confid', 'personList')
        conf_user = UserSignUpDetail.objects.filter(confid=self.input['confid'])
        for data in self.input['personList']:
            checked_user = conf_user.get(user__userid = data)
            checked_user.checked_status = 1
            checked_user.save()
            joinConf(data, self.input['confid'], 0, "")

"""
查看报名信息
"""

class ConfMemberDetail(APIView):

    def get(self):
        self.check_input('confid')
        allInfo =[]
        # 判断是否已经设置报名模块
        try:
            module = ChoosedSignUpParts.objects.get(confid=self.input['confid'])
        except:
            raise LogicError("请先设置会议报名需要的模块")
        # 未设置报名模块，不能进行报名

        module_list = module.getSignUpParts()
        #allInfo.append({"moduleList": module_list})
        # 判断是否设置 price 信息
        judge_price = PriceInfo.objects.filter(confid=self.input['confid'])
        if len(judge_price) == 0:
            price_info = None
        else:
            price_list = PriceInfo.objects.filter(confid=self.input['confid'])
            price_info = []
            for price in price_list:
                elem = {}
                elem["id"] = price.id
                elem["price_description"] = price.price_description
                elem["price_amount"] = price.price_amount
                price_info.append(elem)
        #allInfo.append({"priceInfo": price_info})

#用户信息
        store = UserSignUpDetail.objects.filter(confid=self.input['confid'])
        allInfoList = []
        for userInfo in store:
            allInfo = dict()
            allInfo.update({"name": userInfo.name, "sex": userInfo.sex, "telephone": userInfo.telephone,
                        "email": userInfo.email, "checkedStatus": userInfo.checked_status,
                        "signUpTime": format(userInfo.signup_time,'U'), "userid":userInfo.user.userid})

            if 1 in module_list:
                store1 = UserSignUpExtendAddress.objects.get(basicInfo__user__userid=userInfo.user.userid, basicInfo__confid=self.input['confid'])
                allInfo.update({"country:":store1.country,"address":store1.address})
            else:
                allInfo.update({"country:": None, "address":None})


            if 2 in module_list:
                store2 = UserSignUpExtendPostcode.objects.get(basicInfo__user__userid=userInfo.user.userid, basicInfo__confid=self.input['confid'])
                allInfo.update({"postcode":store2.postcode})
            else:
                allInfo.update({"postcode": None})

            if 3 in module_list:
                store3 = UserSignUpExtendCompanyInfo.objects.get(basicInfo__user__userid=userInfo.user.userid, basicInfo__confid=self.input['confid'])
                allInfo.update({"companyName":store3.company_name,"companyAddress":store3.company_address,"companyJob":store3.company_job})
            else:
                allInfo.update({"companyName": None, "companyAddress": None,
                            "companyJob": None})

            if 4 in module_list:
                store4 = UserSignUpExtendAccommodation.objects.get(basicInfo__user__userid=userInfo.user.userid, basicInfo__confid=self.input['confid'])
                allInfo.update({"accommodationType":store4.accommodation_type})
            else:
                allInfo.update({"accommodationType": None})

            if 5 in module_list:
                store5 = UserSignUpExtendCost.objects.get(basicInfo__user__userid=userInfo.user.userid, basicInfo__confid=self.input['confid'])
                priceinfo=[]
                for price in store5.choosed_pay_models.all():
                    priceinfo.append({"priceId":price.id, "priceDescription":price.price_description, "priceAmount":price.price_amount})
                allInfo.update({"costType":store5.cost_type,"payStatus":store5.user_pay_status,"chosedPriceList":priceinfo})
            else:
                allInfo.update({"costType": None, "payStatus": None,
                            "chosedPriceList": None})

            if 6 in module_list:
                store6 = UserSignUpExtendExtraInfo.objects.get(basicInfo__user__userid=userInfo.user.userid, basicInfo__confid=self.input['confid'])
                allInfo.update({"extraDescription":store6.extra_description})
            else:
                allInfo.update({"extraDescription": None})
            allInfoList.append(allInfo)
        print(allInfoList)

        return allInfoList

"""
发布提醒
"""
#网页测试get通过
class ConfReminds(APIView):

    def get(self):
        self.check_input('confid')
        all_conf = allConfList(223, 1, 1000000000)
        flag = False
        for conf in all_conf["data"]:
            if self.input["confid"] == str(conf['id']):
                flag = True
                theInfo = confInfo(self.input['confid'])
                allObj = Reminds.objects.filter(confid=self.input['confid'])
                alldata=[]
                for i in allObj:
                    alldata.append({"remind":i.info,"publishTime":format(i.publish_time,'U')})
                return{"confid":self.input["confid"],"reminds":alldata, "confname":theInfo['data']['basic']['name']}
        if not flag:
            raise InputError("invalid confid")


    def post(self):

        self.check_input('confid', 'remind')
        all_conf = allConfList(223, 1, 1000000000)
        flag = False
        for conf in all_conf["data"]:
            if self.input["confid"] == str(conf['id']):
                flag = True
                remind = Reminds()
                remind.confid = self.input["confid"]
                remind.info = self.input["remind"]
                remind.publish_time = timezone.now()
                remind.save()

                confid=self.input["confid"]
                info = confInfo(confid)
                confname = info['data']['basic']['name']
                remind = self.input["remind"]

                users = User.objects.all()

                for user in users:
                    allconf=myAllConfs(user.userid)
                    for conf1 in allconf:
                        if str(conf1["id"]) == str(confid):
                            template_id = "Bvk1RD_NkSt5jdgOysH1zK_E-7LbsI7Y3PzjobaG3h0"
                            openid = user.open_id
                            tempurl = "wwww.baidu.com" #settings.get_url('u/user/remindList', {'userid': user.userid, 'confid':confid})
                            postRemind(template_id, confname, remind, openid, tempurl)
                #return {"confid":self.input["confid"],"remind":self.input["remind"]}
        if not flag:
            raise InputError("invalid confid")

