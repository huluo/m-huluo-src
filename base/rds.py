#!/usr/bin/env python
# -*- coding: utf-8 -*-
 

import sys
import redis
import etc
import util
import log


pool = redis.ConnectionPool( host=etc.redis_host, port=etc.redis_port )


#key must be long type
def set_item( pfx, key, item ) :
    try:
        raw_data = util.encode( item )
        r = redis.Redis( connection_pool=pool )
        if r.set( pfx+'_item_'+str(key), raw_data ) :
            return True
        return False
    except Exception as e :
        log.exp( e )
        return False


#key must be long type
def get_item( pfx, key ) :
    try:
        r = redis.Redis( connection_pool=pool )
        raw_data = r.get( pfx+'_item_'+str(key) )
        item = None
        if raw_data :
            item = util.decode( raw_data )
        return item
    except Exception as e :
        log.exp( e )
        return None


#keys of item_dict must be long type
def set_item_dict( pfx, item_dict ) :
    r = redis.Redis( connection_pool=pool )
    pipe = r.pipeline() #原子pipe
    #pipe = r.pipeline(transaction=False) #非原子pipe
    for (k,v) in item_dict.items() :
        try:
            raw_data = util.encode( v )
            pipe.set( pfx+'_item_'+str(k), raw_data )
        except Exception as e :
            log.exp( e )
    try:
        pipe.execute()
    except Exception as e :
        log.exp( e )


#keys in key_arr must be long type
def get_item_dict( pfx, key_arr ) :
    item_dict = {}
    if len(key_arr) <= 0 :
        return item_dict
    r = redis.Redis( connection_pool=pool )
    for key in key_arr :
        try:
            raw_data = r.get( pfx+'_item_'+str(key) )
            item = None
            if raw_data :
                item = util.decode( raw_data )
                item_dict[key] = item
        except Exception as e :
            log.exp( e )
    return item_dict


def del_item( pfx, key ) :
    try:
        r = redis.Redis( connection_pool=pool )
        if r.delete( pfx+'_item_'+str(key) ) :
            return True
        return False
    except Exception as e :
        log.exp( e )
        return False


#keys of item_dict must be long type
def del_item_dict( pfx, key_arr ) :
    r = redis.Redis( connection_pool=pool )
    pipe = r.pipeline() #原子pipe
    #pipe = r.pipeline(transaction=False) #非原子pipe
    for key in key_arr :
        try:
            r.delete( pfx+'_item_'+str(key) )
        except Exception as e :
            log.exp( e )
    try:
        pipe.execute()
    except Exception as e :
        log.exp( e )
        return False
    return True


def clear_all() :
    r = redis.Redis( connection_pool=pool )
    r.flushdb()


if __name__ == "__main__":
    print( 'start' )
    key='None'
    try:
        key = str(sys.argv[1])
    except Exception as e :
        print e
        exit(1)

    #不管是否连接成功，这里都不会异常
    rds = redis.StrictRedis( host=etc.redis_host, port=etc.redis_port, db=0 )

    #如果异常，抛出redis.exceptions.ConnectionError; 如果正常,op=True;
    #op = rds.set(key,"xiangye")
    #print op

    #如果异常，抛出redis.exceptions.ConnectionError
    res = rds.get(key)
    print key
    print res


