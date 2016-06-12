#!/usr/bin/env python
#coding=utf8
 
import http.client    #修改引用的模块
import urllib
import json


import urllib.request


def checkJSON(  content , name ):
    _jsonObj = json.loads(content);
    status = _jsonObj['status'];
    if status != '1':
        print(name  + ', ' + status + ', ' + _jsonObj['data']);
        return False;

    busData = _jsonObj['busData'];
    if (busData == None or len(busData) == 0):
        print(name  + ', ' + status + ', empty ');
        return False;
    return True;


city = '320500';
key  = '19';
url = "http://ditu.amap.com/service/poiInfo?query_type=TQUERY&city="+ city +"&keywords=" + key

print(url);
fp = urllib.request.urlopen(url)

mybytes = fp.read()
# note that Python3 does not read the html code as string
# but as html code bytearray, convert to string with
mystr = mybytes.decode("utf8")

fp.close()

print(mystr)

result = checkJSON(mystr, key);
print( result);

