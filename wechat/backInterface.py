import urllib.parse
import urllib.request
import json
import urllib.parse
import urllib.request
import hashlib
from WeChatTicket.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET
"""
做了一些特殊处理，因为在将返回的消息解析成字典类型时，没有 null，true，false三项
因此，做了定义
null = None
false = False
true = True
调用数据的时候注意一下
"""
null = None
false = False
true = True

#写成了函数，是这样子的，
# 1
def loginToChinaByWeixin(nickname,unionid,headimgurl,sex,location,language):
    """
    用来向会佳服务器说，有用户从微信登录了
    :param nickname: 微信昵称
    :param unionid: 微信唯一id
    :param headimgurl: 头像
    :param sex: 性别
    :param location:位置
    :param language: 语言（cn这样简写的）
    :return:
    """
    urlvalue=urllib.parse.urlencode({"nickname":nickname,"unionid":unionid,"headimgurl":headimgurl,"sex":sex,"location":location,"language":language})
    postdata=("").encode('utf-8')
    url="http://60.205.137.139/adminweb/REST/API-V2/loginToChinaByWeixin?" +urlvalue
    request = urllib.request.Request(url,postdata)
    response=urllib.request.urlopen(request)
    s = response.read().decode('utf-8')
    dic=json.loads(s)
    #print(json.dumps(dic, ensure_ascii=False))
    return dic

# 2
def allConfList(userid,page,page_size):
    """
    用来获取所有会议
    :param userid:会佳用户id
    :param page: 第几页的数据
    :param page_size: 一页有几个
    :return:
    """
    urlvalue=urllib.parse.urlencode({"userid":userid,"page":page,"page_size":page_size})
    url="http://60.205.137.139/adminweb/REST/API-V2/allConfList?"+urlvalue
    response=urllib.request.urlopen(url)
    s = response.read().decode('utf-8')
    dic=json.loads(s)
    return dic

# 3
def upcomingConfList(userid,page,page_size):
    """
    用来获取近期会议
    :param userid: 会佳用户id
    :param page: 第几页
    :param page_size: 一页几个
    :return:
    """
    urlvalue=urllib.parse.urlencode({"userid":userid,"page":page,"page_size":page_size})
    url="http://60.205.137.139/adminweb/REST/API-V2/upcomingConfList?"+urlvalue
    response=urllib.request.urlopen(url)
    s = response.read().decode('utf-8')
    dic=json.loads(s)
    return dic

# 4
def favoriteConfList(userid,page,page_size):
    """
    用来获取我的会议
    :param userid:会佳用户id
    :param page: 第几页
    :param page_size: 一页几个
    :return:
    """
    urlvalue=urllib.parse.urlencode({"userid":userid,"page":page,"page_size":page_size})
    url="http://60.205.137.139/adminweb/REST/API-V2/favoriteConfList?"+urlvalue
    response=urllib.request.urlopen(url)
    s = response.read().decode('utf-8')
    dic=json.loads(s)
    return dic

# 5
def searchConfList(userid,content,page,page_size):
    """
    关键词搜索会议
    :param userid:会佳用户id
    :param content: 关键词
    :param page: 第几页
    :param page_size: 一页几个
    :return:
    """
    urlvalue=urllib.parse.urlencode({"userid":userid,"content":content,"page":page,"page_size":page_size})
    url="http://60.205.137.139/adminweb/REST/API-V2/searchConfList?"+urlvalue
    response=urllib.request.urlopen(url)
    s = response.read().decode('utf-8')
    dic=json.loads(s)
    return dic

# 6
def confDetail(confid):
    """
    获取会议详情
    :param confid:会议id
    :return:
    """
    urlvalue=urllib.parse.urlencode({"confid":confid})
    url="http://60.205.137.139/adminweb/REST/API-V2/confDetail?"+urlvalue
    response=urllib.request.urlopen(url)
    s = response.read().decode('utf-8')
    dic=json.loads(s)
    return dic



# 7
def confInfo(confid):
    """
    获取会议详情1
    :param confid:会议id
    :return:
    """
    urlvalue=urllib.parse.urlencode({"confid":confid})
    url="http://60.205.137.139/adminweb/REST/API-V2/confInfo?"+urlvalue
    response=urllib.request.urlopen(url)
    s = response.read().decode('utf-8')
    dic=json.loads(s)
    return dic


# 8
def joinConf(userid,confid,type,code):
    """
    用来跟会佳服务器说有用户要加入某个会议
    :param userid: 会佳用户id
    :param confid: 会佳会议id
    :param type: 类型。。（会佳接口有说明）
    :param code: 邮箱
    :return:
    """
    urlvalue=urllib.parse.urlencode({"userid":userid,"confid":confid,"type":type,"code":code})
    postdata=("").encode('utf-8')
    url="http://60.205.137.139/adminweb/REST/API-V2/joinConf?" +urlvalue
    request = urllib.request.Request(url,postdata)
    response=urllib.request.urlopen(request)
    s = response.read().decode('utf-8')
    dic=json.loads(s)
    return dic

# 9
def cancelConf(userid,confid):
    """
    用来告诉会佳服务器某个用户想退出某个会议了
    :param userid: 会佳用户ID
    :param confid: 会佳会议id
    :return:
    """
    urlvalue = urllib.parse.urlencode({"userid": userid, "confid": confid})
    postdata = ("").encode('utf-8')
    url = "http://60.205.137.139/adminweb/REST/API-V2/cancelConf?" + urlvalue
    request = urllib.request.Request(url, postdata)
    response = urllib.request.urlopen(request)
    s = response.read().decode('utf-8')
    dic = json.loads(s)
    return dic
#10
def myAllConfs(userid):
    confList = []
    totalCount = 0
    pageNum = 1
    result = favoriteConfList(userid, pageNum, 20)
    totalCount = int(result['total_size'])
    confList += result['data']
    while pageNum * 20 < totalCount:
        pageNum += 1
        result = favoriteConfList(userid, pageNum, 20)
        confList += result['data']

    return confList

#11
def getUnionId(access_token, openId):
    url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN"%(access_token,openId)
    #print (url)
    response = urllib.request.urlopen(url)
    s = response.read().decode("utf-8")
    dic = eval(s)
    return dic
    #https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN
# 要注意
appId = WECHAT_APPID
appSecret = WECHAT_SECRET
def getAccessToken(appId,appSecret):
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(appId,appSecret)
    response=urllib.request.urlopen(url)
    s = response.read().decode('utf-8')
    s = eval(s)
    return s

#accessToken = getAccessToken(appId,appSecret)
#s = getUnionId(accessToken["access_token"],"ophyUwgr6IAzdQqENeW-2OFENy-Y")
def postRemind(template_id,conf,remind,openid,tempurl):
    print("this is done")
    AAA_token = getAccessToken(appId,appSecret)["access_token"]
    url='https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s'%AAA_token
    template_id =template_id
    postdata='{"touser":"%s","template_id":"%s","url":"%s","data":{"conf": {"value":"%s"},"remind":{"value":"%s"}}}'%(openid,template_id,tempurl,conf,remind)
    #print(postdata)
    postdata=postdata.encode('utf-8')
    request = urllib.request.Request(url,postdata)
    response=urllib.request.urlopen(request)
    s = response.read().decode('utf-8')
    dic=eval(s)
    ###print(dic)

#conf="联合峰会"
#remind="注意老人和小孩的安全"
#openid = "opLZjwZ4nid4yL10YUjVJ8K97-D0"
#tempurl=""#"http://www.baidu.com/"

#postRemind(conf,remind,openid,tempurl)

