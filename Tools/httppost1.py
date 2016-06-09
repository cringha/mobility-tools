#!/usr/bin/env python
#coding=utf8
 
import http.client    #修改引用的模块
import urllib
 
reqconn = None
 
try:
    reqheaders={
        'MobileType':'Android',
        'DeviceToken':'xxxxxxxxx',
        'OSVersion':'1.0.3',
        'AppVersion':'14',
        'Host':'192.xxx.x.xxxx'} 
    reqconn = http.client.HTTPConnection("www.sina.com.cn")  #修改对应的方法
    reqconn.request("GET", "/Login?username=1416&password=123", None, reqheaders)
    res=reqconn.getresponse()
    print (res.status,  res.reason)
    print (res.msg)
    print (res.read())
except Exception  as e:
    print (e) 
finally:
    if reqconn:
        reqconn.close()