# AliyunAPI
基于Python3的AliyunAPI<br>
包含了常用的dns操作接口（dns.py）和常用ecs接口（ecs.py）<br>
包含了一个自动创建ecs的脚本，可以快速用指定镜像构建服务器，并上传ip至阿里云DNS<br>
请注意autovpn.py中的绝对路径，使用前请更改,详情见文件中注释
=====
目前所有接口用函数实现，正常人看起来简单易懂，以后如果完善起来可能会封装成类<br>
ps.ecs的官方文档可能存在问题，我写的时候被狠狠坑了一把<br>
