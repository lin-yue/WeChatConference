#fasdfacveoijcmljzpajidfwaioedhwqihxnwjddiwjediowefhuehde
import urllib.parse
import urllib.request
import hashlib
def getUnionId(access_token, openId):
    url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN"%(access_token,openId)
    #print (url)
    response = urllib.request.urlopen(url)
    s = response.read().decode("utf-8")
    dic = eval(s)
    return dic
    #https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN

appId = "wx5419526a55a19d30"
appSecret = "b2296729700c665c9981d8bf24334957"
def getAccessToken(appId,appSecret):
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(appId,appSecret)
    response=urllib.request.urlopen(url)
    s = response.read().decode('utf-8')
    s = eval(s)
    return s

accessToken = getAccessToken(appId,appSecret)
#print(accessToken)
#ha_access_token = {'access_token': 'yd61ZL2c0PBMw3zIvX-nu0d481xadUiBQJU7pmEYB2_WmNhE7L3jrADenkTBonXcX4Te9_AinSW4l1Jok0uIf0nZUHQZC7ZeDu-szurneWEO7T5HL3c-IR1T5riy_0jZMKQjACAXVB', 'expires_in': 7200}
#print(accessToken["access_token"])
s = getUnionId(accessToken["access_token"],"ophyUwgr6IAzdQqENeW-2OFENy-Y")
#print(s)
##############################################################################
#token = "fasdfacveoijcmljzpajidfwaioedhwqihxnwjddiwjediowefhuehde"
#url="https://api.weixin.qq.com/scan/merchantinfo/get?access_token=" +accessToken["access_token"]
#response=urllib.request.urlopen(url)
#s = response.read().decode('utf-8')
#print (s)

###########################################################
#url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi"%(accessToken["access_token"])
#response=urllib.request.urlopen(url)
#s = response.read().decode('utf-8')
#print (s)

#ha_jsapi_ticket = {"errcode":0,"errmsg":"ok","ticket":"kgt8ON7yVITDhtdwci0qecqhbsNHfP5ty6gm6EJwZoFj-6ARFTa836wwKgq3_Cc6hy9xHFXvfjGCUoWn2xZ2MQ","expires_in":7200}

#获取签名
#tt = "jsapi_ticket=sM4AOVdWfPE4DxkXGEs8VMCPGGVi4C3VM0P37wVUCFvkVAy_90u5h9nbSlYy3-Sl-HhTdfl2fzFy1AOcHKP7qg&noncestr=Wm3WZYTPz0wzccnW&timestamp=1414587457&url=http://mp.weixin.qq.com?params=value"
#sha = hashlib.sha1(tt.encode("utf-8"))
#s = sha.hexdigest()
#print(s)
#############################################################


############################################################
#调用统一支付api
#temp = '<xml><appid>wxd930ea5d5a258f4f</appid><attach>支付测试</attach><body>test</body><mch_id>10000100</mch_id><device_info>1000</device_info><nonce_str>ibuaiVcKdpRxkhJA</nonce_str><notify_url>http://wxpay.wxutil.com/pub_v2/pay/notify.v2.php</notify_url><openid>oUpF8uMuAJO_M2pxb1Q9zNjWeS6o</openid><out_trade_no>1415659990</out_trade_no><spbill_create_ip>14.23.150.211</spbill_create_ip><total_fee>1</total_fee><trade_type>JSAPI</trade_type><sign>9A0A8659F005D6984697E2CA0A9CF3B7</sign></xml>'

#
#url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
#
#print(temp)
#req = urllib.request.Request(url=url,headers={"Content-Type":"text/xml"},data=temp.encode("utf-8"))
#res = urllib.request.urlopen(req)
#print(res.read().decode("utf-8"))

#################################################################
#假装得到了prepay_id和code_url（二维码链接）
#生成二维码






