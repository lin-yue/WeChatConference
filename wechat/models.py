from django.db import models

from codex.baseerror import LogicError
import json

CONFERENCELIST_RECENT = 1
CONFERENCELIST_ALL = 2
CONFERENCELIST_MY = 3
CONFERENCELIST_SEARCH = 4

class User(models.Model):
    open_id = models.CharField(max_length=64, unique=True, db_index=True)
    userid = models.CharField(max_length=32, unique=True,  null = True)#db_index=True,
    union_id = models.CharField(max_length=64, unique=True, db_index=True)
    nickname = models.CharField(max_length=64)
    headimgurl = models.CharField(max_length=512)
    pageNum = models.IntegerField(null=True)
    pageState = models.IntegerField(null=True)

    searchWords = models.CharField(max_length=64,  null = True)

    reminds = models.ManyToManyField('Reminds')

    @classmethod
    def get_by_openid(cls, openid):
        try:
            return cls.objects.get(open_id=openid)
        except cls.DoesNotExist:
            raise LogicError('User not found')

    PAGE_ALLCONF = 1
    PAGE_RECENTCONF = 2
    PAGE_MYCONF = 3
    PAGE_SERACHCONF = 4
    PAGE_NOTLIST = -1

class UserSignUpDetail(models.Model):
    user = models.ForeignKey(User)
    confid =  models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    sex = models.IntegerField()
    telephone = models.CharField(max_length=64)
    email = models.CharField(max_length = 128)
    checked_status = models.IntegerField()
    signup_time = models.DateTimeField()

    # user状态：被会议发布者拒绝，审核通过，审核被拒绝，等待审核
    USER_CHECKED = 1
    USER_REFUSED = 2
    USER_WAITING = 3
    USER_CANCELED = 4


    SEX_MAN = 1
    SEX_WOMAN = 0


class UserSignUpExtendAddress(models.Model):
    basicInfo = models.OneToOneField(UserSignUpDetail)
    country = models.IntegerField()
    address = models.CharField(max_length=256)

    COUNTRY_CHINA = 1
    COUNTRY_AMERICA = 2
    COUNTRY_JAPAN = 3
    COUNTRY_RUSSISA = 4

class UserSignUpExtendPostcode(models.Model):
    basicInfo = models.OneToOneField(UserSignUpDetail)
    postcode = models.CharField(max_length=64)

class UserSignUpExtendCompanyInfo(models.Model):
    basicInfo = models.OneToOneField(UserSignUpDetail)
    company_name = models.CharField(max_length=128)
    company_address = models.CharField(max_length=128, null=True)   #选填
    company_job = models.CharField(max_length=128)

class UserSignUpExtendAccommodation(models.Model):
    basicInfo = models.OneToOneField(UserSignUpDetail)
    accommodation_type = models.IntegerField()

    ACCOMODATION_CHAEAP = 1
    ACCOMODATION_NORMAL = 2
    ACCOMODATION_GOOD = 3

class UserSignUpExtendCost(models.Model):
    basicInfo = models.OneToOneField(UserSignUpDetail)
    cost_type = models.IntegerField()
    user_pay_status = models.IntegerField()
    choosed_pay_models = models.ManyToManyField('PriceInfo')  # 用户选择的价格模块和一个会议的全部价格模块是多对多关系

    # 电子支付未支付和已支付
    # 其他支付状态（如自行转账）同cost_type    user_type =  cost_type

    USER_HAS_NOT_PAY = 0
    USER_PAYED = 1

    COST_PAYNOW = 1
    COST_PAY_WHEN_ARRIVE = 2
    COST_PAY_BUY_ACCOUNT = 3


class UserSignUpExtendExtraInfo(models.Model):
    basicInfo = models.OneToOneField(UserSignUpDetail)
    extra_description = models.CharField(max_length=512)

#用于描述每个会议报名时每个可选的价格项
class PriceInfo(models.Model):
    confid =  models.CharField(max_length=128)
    price_description = models.CharField(max_length=512)
    price_amount = models.IntegerField()

#用于记录会议者选择的模块
class ChoosedSignUpParts(models.Model):
    confid = models.CharField(max_length=128)

    #choose parts是一个列表的json串,一个使用的例子是：
    # theParts = ChoosedSignUpParts()
    # theParts.setSignUpParts([1, 3, 5])
    # theParts.save()
    # print(theParts.getSignUpParts())

    chooseParts = models.CharField(max_length=256)
    maxJoinNum = models.IntegerField()
    def setSignUpParts(self,theList):
        self.chooseParts = json.dumps(theList)

    def getSignUpParts(self):
        return json.loads(self.chooseParts)

    PART_ADDRESS = 1
    PART_MAILCODE = 2
    PART_COMPANY = 3
    PART_ACCOMMODATION = 4
    PART_COST = 5
    PART_EXTRAINFO = 6

#会议发布者发布的提醒
class Reminds(models.Model):
    confid = models.CharField(max_length=128)
    info = models.CharField(max_length=512)
    publish_time = models.DateTimeField()

class Reviews(models.Model):
    user = models.ForeignKey(User)
    confid =  models.CharField(max_length=128)
    detail = models.CharField(max_length=512)
    publish_time = models.DateTimeField()



