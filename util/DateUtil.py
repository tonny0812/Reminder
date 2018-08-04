#encoding:utf-8
'''
Created on 2018年8月1日

@author: guodongqing
'''
import time
import json
from urllib import urlencode
import urllib2

url = 'http://api.k780.com'
params = {
  'app' : 'life.workday',
  'date' : '',
  'appkey' : '35576',
  'sign' : '76b98bb4baf22df5b362efeccf739c49',
  'format' : 'json'
}

def isWorkDay(checkDate):
    result = False;
    if checkDate is not None:
        params['date'] = checkDate;
        urlparams = urlencode(params)
        req = urllib2.Request(url)
        result = urllib2.urlopen(req, urlparams)
        nowapi_call = result.readlines()
        nowapi_call = ','.join(nowapi_call)
        print nowapi_call
        a_result = json.loads(nowapi_call)
        if a_result:
            if a_result['success'] != '0':
                workmk = a_result['result']['workmk'];
                if workmk == '1':
                    result = True;
                else:
                    result = False;
            else:
                print a_result['msgid']+' '+a_result['msg']
        else:
            print '获取  nowapi 失败！';
    return result;

def getCurrentDate():
    #获得当前时间时间戳 
    now = int(time.time()) 
    #转换为其他日期格式,如:"%Y%m%d",20180801 
    timeStruct = time.localtime(now) 
    strTime = time.strftime("%Y%m%d", timeStruct) 
    return strTime;
