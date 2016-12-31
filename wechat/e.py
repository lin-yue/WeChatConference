import urllib.parse
import urllib.request
import json
from d import accessToken
#这是设置所属行业

AAA_token= accessToken["access_token"]
#url='https://api.weixin.qq.com/cgi-bin/template/api_set_industry?access_token=%s'%AAA_token
#leixing = 2#IT软件与服务
#postdata='{"industry_id1":1,"industry_id2":4}'
#
#postdata=postdata.encode('utf-8')
#request = urllib.request.Request(url,postdata)
#response=urllib.request.urlopen(request)
#s = response.read().decode('utf-8')
#dic=eval(s)
#print(dic)

#获取template_id
url='https://api.weixin.qq.com/cgi-bin/template/api_add_template?access_token=%s'%AAA_token
postdata='{"template_id_short":"TM00015"}'
postdata=postdata.encode('utf-8')
request = urllib.request.Request(url,postdata)
response=urllib.request.urlopen(request)
s = response.read().decode('utf-8')
dic=eval(s)
print(dic)

#发送模板消息
url='https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s'%AAA_token
openid = "opLZjwZ4nid4yL10YUjVJ8K97-D0"
template_id = "eC4o4s9de0DkKz9IjdtvIJf7wew6OYuwMzTG-fj2jWE"
tempurl="http://www.baidu.com/"
postdata='{"touser":"%s","template_id":"%s","url":"%s","data":{"first": {"value":"谢谢"},"keyword1":{"value": "0000 0000"},"keyword2":{"value": " 某先生"},"keyword3":{"value": "1234566"},"keyword4":{"value":"2015.09.09"},"remark":{"value": "谢谢"}}}'%(openid,template_id,tempurl)
#print(postdata)
postdata=postdata.encode('utf-8')
request = urllib.request.Request(url,postdata)
response=urllib.request.urlopen(request)
s = response.read().decode('utf-8')
dic=eval(s)
print(dic)