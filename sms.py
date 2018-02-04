#encoding=utf-8  
import urllib
from hashlib import sha1
import base64
import hmac
import time
import datetime
import random
from urllib import request
try: import httplib
except ImportError:
    import http.client as httplib
import pprint
import json
#------------------------------------------------------------------------------
AccessKeyId = "LTAIO00TT5qdVshx"
AccessKeySecret = "iiJ1I0LJp3F8pJBQWqir7gjevsxAr2"
URL = 'http://dysmsapi.aliyuncs.com/?'

#------------------------------------------------------------------------------
def sign(accessKeySecret, parameters):
    #===========================================================================
    # '''签名方法
    # @param secret: 签名需要的密钥
    # @param parameters: 支持字典和string两种
    # '''
    #===========================================================================
    # 如果parameters 是字典类的话
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])

    canonicalizedQueryString = ''
    for (k,v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)

    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])

    h = hmac.new(accessKeySecret + b"&", stringToSign.encode('utf8'), sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature

def percent_encode(encodeStr):
    encodeStr = str(encodeStr)
    res = urllib.parse.quote(encodeStr, '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res

def make_url(url,userdict):
    #------------------------------------------------------------------------------
    now = datetime.datetime.utcnow()
    otherStyleTime = now.strftime("%Y-%m-%dT%H:%M:%SZ")#2015-01-09T12:00:00Z
    randomint = random.randint(11111111111111,99999999999999)
    #------------------------------------------------------------------------------
    dict = {
    "Format":"json",
    "AccessKeyId":AccessKeyId,
    "SignatureMethod":"HMAC-SHA1",
    "SignatureNonce":str(randomint),
    "SignatureVersion":"1.0",
    "Version":"2017-05-25",
	"RegionId":"cn-hangzhou",
    "Timestamp":otherStyleTime}
    dict.update(userdict)
    Signature = percent_encode(sign(AccessKeySecret.encode("utf-8"), dict).decode("utf-8"))
    for k, v in dict.items():
        url = url+"&"+k+"="+urllib.parse.quote(v)
    url = url+"&Signature="+Signature
    print(url)
    return (url)
    
def get_result(userdict):
    url = make_url(URL,userdict)
    with request.urlopen(url) as result:
        if result.status == 400:
            return("{"+result.reason+"}")
        res = result.read().decode("utf-8")
        return(res)
        
def SensMsg(PhoneNumbers,SignName,TemplateCode,TemplateDict):
    userdict={
    "Action":"SendSms",
	"PhoneNumbers":PhoneNumbers,
	"SignName":SignName,
	"TemplateCode":TemplateCode,
	"TemplateParam":json.dumps(TemplateDict)
	}
    recoder = get_result(userdict)
    recoder_dict = json.loads(recoder)
    return(recoder_dict)

SensMsg('18110020002', '智能床垫', 'SMS_125020022', {"Code":"1234"})