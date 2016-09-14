#香港网络组:sg-62sfxisdy 北京网络组:sg-259kdkgch
#香港镜像:m-6263nygnj 北京镜像:m-2506z0jtn
#注意10/12/13/77行的绝对路径
from pprint import pprint
import time
import datetime
import os
import ecs
import dns
logurl = 'D:\\python\\aliyun api\\log.txt'
log = open(logurl, 'a+', encoding='utf-8')
newlog = open(r'D:\python\aliyun api\%s.txt'%(str(str(time.strftime('%Y-%m-%d %H-%M-%S')))), 'a+', encoding='utf-8')
newdelete = open(r'C:\Users\Zhang\Desktop\%s.py'%(str(str(time.strftime('%Y-%m-%d %H-%M-%S')))),'a', encoding='utf-8')
HKinfo = {
    "RegionId":"cn-hongkong",
    "ImageId":"m-6263nygnj",
    "InstanceType":"ecs.n1.tiny",
    "SecurityGroupId":"sg-62sfxisdy",
    "InstanceChargeType":"PostPaid",
    "InternetChargeType":"PayByTraffic",
    "InternetMaxBandwidthOut":"5",
    "Password":"UserPass",
    "IoOptimized":"optimized",
    "SystemDisk_Category":"cloud_efficiency",
    "SystemDiskSize":"40"
    }
def AutoDeleteEcs(InstanceId,RegionId="cn-hongkong"):
    import ecs
    log = open(r'D:\python\aliyun api\log.txt', 'a+')
    state = ecs.GetEcsState(RegionId=RegionId,InstanceIds=InstanceId)
    ecs.StopEcs(InstanceId,ForceStop=True)
    while state != "Stopped":
        print(state)
        time.sleep(1)
        state = ecs.GetEcsState(RegionId=RegionId,InstanceIds=InstanceId)
    ecs.DeleteEcs(InstanceId)
    print(InstanceId,"Delete")
    return None
    
res = ecs.CreateEcs(**HKinfo)
log.write(str(time.strftime('%Y-%m-%d %H-%M-%S'))+":"+str(res)+"\n")

id = res["InstanceId"]
newlog.write("id:"+id+'\n')

infores = ecs.GetEcsInfo(RegionId=HKinfo["RegionId"],InstanceIds=id)
pprint(infores)
log.write(str(str(time.strftime('%Y-%m-%d %H-%M-%S')))+":"+str(infores)+"\n")
newlog.write("info:"+str(infores)+'\n')

ip = ecs.GetEcsIp(InstanceId=id)
log.write(str(time.strftime('%Y-%m-%d %H-%M-%S'))+":"+str(ip)+"\n")

ip = ip["IpAddress"]
newlog.write("ip:"+ip+'\n')
print("id:",id)
print("ip:",ip)

print("更改dns")
dnsres = dns.change_dns_recoder(RRKeyWord="hk.vpn",DomainName="casxt.com",ip=ip)
log.write(str(time.strftime('%Y-%m-%d %H-%M-%S'))+":"+str(dnsres)+"\n")

print("等待20s")
time.sleep(20)

print("启动实例")
startres = ecs.StartEcs(InstanceId=id)
log.write(str(time.strftime('%Y-%m-%d %H-%M-%S'))+":"+str(startres)+"\n")

log.write("==========================================="+"\n")
log.close()
newlog.close()

py = '''
import time
import sys
sys.path.append("D:\\\\python\\\\aliyun api\\\\")
import ecs
log = open(r"{0}", 'a+', encoding='utf-8')
InstanceId = "{1}"
RegionId = "{2}"
state = ecs.GetEcsState(RegionId=RegionId,InstanceIds=InstanceId)
log.write(str(time.strftime('%Y-%m-%d %H-%M-%S'))+":"+str(state)+'\\n')
stopres = ecs.StopEcs(InstanceId,ForceStop=True)
log.write(str(time.strftime('%Y-%m-%d %H-%M-%S'))+":"+str(stopres)+'\\n')
while state != "Stopped":
    print(state)
    time.sleep(1)
    state = ecs.GetEcsState(RegionId=RegionId,InstanceIds=InstanceId)
delres = ecs.DeleteEcs(InstanceId)
log.write(str(time.strftime('%Y-%m-%d %H-%M-%S'))+":"+str(delres)+'\\n')
print(InstanceId,"Delete")
log.close()
input("回车退出:")
'''.format(logurl,id,HKinfo["RegionId"])
print("创建删除脚本")
newdelete.write(py)
newdelete.close()

print("轮询实例状态")
a=0
state = ecs.GetEcsState(RegionId=HKinfo["RegionId"],InstanceIds=id)
while state != "Running":
    print(state)
    time.sleep(1)
    a=a+1
    state = ecs.GetEcsState(RegionId=HKinfo["RegionId"],InstanceIds=id)

if a < 50:
    print("实例可能启动有误")
    select = input("删除实例选1,不删除直接回车:")
    if select=="1":
        AutoDeleteEcs(InstanceId=id,RegionId=HKinfo["RegionId"])
        
print("id:",id)
print("ip:",ip)
print("清空dns")
os.system("ipconfig /flushdns")
sel = input("回车退出，输入1再次刷新:")
while sel == "1":
    print("ipconfig /flushdns")
    os.system("ipconfig /flushdns")
    print("ping hk.vpn.casxt.com -w 100")
    os.system("ping hk.vpn.casxt.com -w 100")
    sel = input("回车退出，输入1再次刷新:")