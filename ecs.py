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
AccessKeyId = "AccessKeyId"
AccessKeySecret = "AccessKeySecret"
URL = 'https://ecs.aliyuncs.com/?'
DEBUG=False
#DEBUG=True
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
    "Version":"2014-05-26",
    "Timestamp":otherStyleTime}
    dict.update(userdict)
    Signature = percent_encode(sign(AccessKeySecret.encode("utf-8"), dict).decode("utf-8"))
    for k, v in dict.items():
        url = url+"&"+k+"="+v
    url = url+"&Signature="+Signature
    return (url)
    
def get_result(userdict,DEBUG=DEBUG):

    url = make_url(URL,userdict)
    if DEBUG:
        print (url)
    else:
        try:
            result = request.urlopen(url)
            res = result.read().decode("utf-8")
            return(res)
        except urllib.error.HTTPError as e:
            res = e.read().decode("utf-8")
            print (e.read())
            return(res)

def CreateEcs(ImageId=None,SecurityGroupId=None,Password=None,RegionId="cn-hongkong",\
InstanceType="ecs.n1.tiny",ZoneId=None,InternetChargeType="PayByTraffic",\
InternetMaxBandwidthOut="5",InstanceChargeType="PostPaid",SystemDisk_Category="cloud_efficiency",\
IoOptimized = "none",SystemDiskSize="40",**dicargs):
    #系列 II："ecs.n1.small"，系列 I：非 I/O 优化："ecs.t1.small",I/O 优化实例:"ecs.s2.large"
    #"cn-hongkong","cn-beijing","cn-qingdao","cn-shanghai"
    if (ImageId is None) or (SecurityGroupId is None) or (Password is None):
        return ({"缺少参数"})
    userdict = {
    "Action":"CreateInstance",
    "RegionId":RegionId,
    "ImageId":ImageId,
    "InstanceType":InstanceType,
    "SecurityGroupId":SecurityGroupId,
    "InstanceChargeType":InstanceChargeType,
    "InternetChargeType":InternetChargeType,
    "InternetMaxBandwidthOut":InternetMaxBandwidthOut,
    "Password":Password,
    "IoOptimized":IoOptimized,
    "SystemDisk.Category":SystemDisk_Category,
    "SystemDiskSize":str(SystemDiskSize)
    }
    if ZoneId is not None:
        userdict["ZoneId"]=ZoneId
    #pprint.pprint(userdict)
    res = json.loads(get_result(userdict))
    #pprint.pprint(res)
    return (res)

def TestCreateEcs(ImageId,SecurityGroupId,Password):
    #系列 II："ecs.n1.tiny"，系列 I：非 I/O 优化："ecs.t1.small",I/O 优化实例:"ecs.s2.large"
    #"cn-hongkong","cn-beijing","cn-qingdao","cn-shanghai"
    userdict = {
    "Action":"CreateInstance",
    "RegionId":"cn-beijing",
    "ImageId":ImageId,
    "InstanceType":"ecs.n1.tiny",
    "SecurityGroupId":SecurityGroupId,
    "InstanceChargeType":"PostPaid",
    "InternetChargeType":"PayByTraffic",
    "InternetMaxBandwidthOut":"5",
    "Password":Password,
    "IoOptimized":"optimized",
    "SystemDisk.Category":"cloud_efficiency",
    "SystemDiskSize":"40"
    }
    res = json.loads(get_result(userdict))
    #pprint.pprint(res)
    return (res)

def StopEcs(InstanceId,ForceStop=False):
    #必须先停止才能关闭
    userdict = {
    "Action":"StopInstance",
    "InstanceId":InstanceId,
    "ForceStop":str(ForceStop)
    }
    res = json.loads(get_result(userdict))
    #pprint.pprint(res)
    return (res)

def StartEcs(InstanceId):
    #必须先停止才能关闭
    userdict = {
    "Action":"StartInstance",
    "InstanceId":InstanceId
    }
    res = json.loads(get_result(userdict))
    #pprint.pprint(res)
    return (res)
    
def DeleteEcs(InstanceId):
    userdict = {
    "Action":"DeleteInstance",
    "InstanceId":InstanceId,
    }
    res = json.loads(get_result(userdict))
    #pprint.pprint(res)
    return (res)

def GetEcsInfo(RegionId,InstanceIds=None):
    #获得实例信息
    userdict = {
    "Action":"DescribeInstances",
    "RegionId":RegionId
    }
    if (RegionId is not None):
        userdict["InstanceIds"] = str([InstanceIds])
    res = json.loads(get_result(userdict))
    #pprint.pprint(res)
    return (res)

def GetEcsState(RegionId,InstanceIds=None):
    #获得实例运行状态
    userdict = {
    "Action":"DescribeInstanceStatus",
    "RegionId":RegionId
    }
    res = json.loads(get_result(userdict))
    if(InstanceIds is None):
        pprint.pprint(res)
    else:
        for ecs in res["InstanceStatuses"]["InstanceStatus"]:
            if ecs["InstanceId"] == InstanceIds:
                #pprint.pprint(ecs["Status"])
                return (ecs["Status"])
        return (res)
    return (res)

def GetEcsIp(InstanceId):
    #没有ip时将分配一个ip给实例，实例重启后生效
    userdict = {
    "Action":"AllocatePublicIpAddress",
    "InstanceId":InstanceId
    }
    res = json.loads(get_result(userdict))
    return (res)
# userdict = {
# "Action":"DescribeInstanceTypes",
# "RegionId":"cn-qingdao"
# }

# pprint.pprint(json.loads(get_result(userdict)))