#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import uuid
import cPickle
import base64
import datetime
import time
import smtplib
from email.mime.text import MIMEText
from tld import get_tld


def datetime_now_ms() :
    return int( round(time.time()*1000) )


def datetime_now_str() :
    date=datetime.datetime.now()
    return date.strftime("%Y-%m-%d %H:%M:%S")


def encode( real_data ) :
    pickled = cPickle.dumps( real_data )
    return base64.encodestring( pickled )


def decode( raw_data ) :
    pickled = base64.decodestring( raw_data )
    return cPickle.loads( pickled )


def make_a_secret() :
    res = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
    print res
    return res


def send_mail(to, sub,content) :
    me="石头人"+"<hello@rongoman.com>"
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = to
    try:
        server = smtplib.SMTP()
        server.connect("smtp.exmail.qq.com")
        server.login("hello@rongoman.com","hotumatua001")
        server.sendmail(me, to, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


def get_domain_from_host( host ) :
    return get_tld('http://'+host,fail_silently=True)


if __name__ == "__main__":
    print 'start'

