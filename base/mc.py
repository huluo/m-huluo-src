#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
import memcache
import etc
import util
import log
 

#key must be long type
def set_item( pfx, key, item ) :
    try:
        raw_data = util.encode( item )
        mc = memcache.Client( etc.memcached_addr, debug=0 )
        if mc.set( pfx+'_item_'+str(key), raw_data, etc.item_timeout ) :
            return True
        return False
    except Exception as e :
        log.exp( e )
        return False


#key must be long type
def get_item( pfx, key ) :
    try:
        mc = memcache.Client( etc.memcached_addr, debug=0 )
        raw_data = mc.get( pfx+'_item_'+str(key) )
        item = None
        if raw_data :
            item = util.decode( raw_data )
        return item
    except Exception as e :
        log.exp( e )
        return None


#keys of item_dict must be long type
def set_item_dict( pfx, item_dict ) :
    for (k,v) in item_dict.items() :
        try:
            raw_data = util.encode( v )
            mc = memcache.Client( etc.memcached_addr, debug=0 )
            mc.set( pfx+'_item_'+str(k), raw_data, etc.item_timeout )
        except Exception as e :
            log.exp( e )


#keys in key_arr must be long type
def get_item_dict( pfx, key_arr ) :
    item_dict = {}
    if len(key_arr) <= 0 :
        return item_dict
    try:
        mc = memcache.Client( etc.memcached_addr, debug=0 )
        str_key_arr = [ pfx+'_item_'+str(i) for i in key_arr ]
        raw_datas = mc.get_multi( str_key_arr )
        for (k,v) in raw_datas.items() :
            item = util.decode( v )
            item_dict[long(k.replace(pfx+'_item_',''))] = item
        return item_dict
    except Exception as e :
        log.exp( e )
        return {}


#key must be string type altable
def get_node( pfx, key ) :
    try:
        mc = memcache.Client( etc.memcached_addr, debug=0 )
        raw_data = mc.get( pfx+'_node_'+str(key) )
        node = None
        if raw_data :
            node = util.decode( raw_data )
        return node
    except Exception as e :
        log.exp( e )
        return None


#key must be string type altable
def set_node( pfx, key, node ) :
    try:
        raw_data = util.encode( node )
        mc = memcache.Client( etc.memcached_addr, debug=0 )
        if mc.set( pfx+'_node_'+str(key), raw_data, etc.node_timeout ) :
            return True
        return False
    except Exception as e :
        log.exp( e )
        return False


#key must be string type altable
def get_persist( pfx, key ) :
    try:
        mc = memcache.Client( etc.memcached_addr, debug=0 )
        raw_data = mc.get( pfx+'_persist_'+str(key) )
        persist = None
        if raw_data :
            persist = util.decode( raw_data )
        return persist
    except Exception as e :
        log.exp( e )
        return None


#key must be string type altable
def set_persist( pfx, key, persist ) :
    try:
        raw_data = util.encode( persist )
        mc = memcache.Client( etc.memcached_addr, debug=0 )
        if mc.set( pfx+'_persist_'+str(key), raw_data, etc.persist_timeout ) :
            return True
        return False
    except Exception as e :
        log.exp( e )
        return False


def clear_all() :
    try:
        mc = memcache.Client( etc.memcached_addr, debug=0 )
        if mc.flush_all() :
            return True
        return False
    except Exception as e :
        log.exp( e )
        return False


if __name__ == "__main__":
    key='None'
    try:
        key = str(sys.argv[1])
    except Exception as e :
        print e
        exit(1)

    #不管是否连接成功，这里都不会异常;
    mc = memcache.Client( etc.memcached_addr, debug=0 )

    #如果异常,op=0; 如果正常,op=True;
    #op = mc.set(key,"yexiang")
    #print op

    #如果异常,res=None;
    res = mc.get(key)

    print key
    print res


