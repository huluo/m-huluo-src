#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import psycopg2
import log
 
def popUID():
    try:
        #如果异常，抛出psycopg2.OperationalError;如果正常，连接将保持，pgsql无法从supervisor关闭;
        pgsql=psycopg2.connect("dbname=rongoman user=postgres port=8004")
        #不管连接是否被关闭，这里都不会异常
        pgcur=pgsql.cursor()
        #op恒等于None; 如果连接被强行关闭，这里抛出psycopg2.OperationalError
        op = pgcur.execute("SELECT nextval ('seq_userid')")
        #不管连接是否被关闭，这里都不会异常，但是会得到res的错误数据
        res=pgcur.fetchone()
        return res[0]
    except Exception as e:
        log.i(e);
        return None

if __name__ == "__main__":
    newuid=popUID()
    print newuid

