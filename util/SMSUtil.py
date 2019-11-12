# encoding:utf-8
'''
Created on 2018年8月1日

@author: guodongqing
'''
import os

infoSMSCMD = 'sh /opt/utils/pms-alert/info-sms.sh ';
output = ' >> sms.info';


def sendSMS(receivers, msg):
    try:
        if receivers is not None and len(receivers) > 0 and msg is not None:
            receivers = ','.join(receivers);
            msg = unicode('"' + msg + '"', "utf-8")
            os.system(infoSMSCMD + receivers + ' ' + msg + output);
    except Exception as e:
        print(e)
        raise e
