#!/usr/bin/env python
# -*- coding: utf-8 -*-
 

import sys
import tornado.web
import uuid
import datetime
import memcache
import etc
import util
import session_base
import log
 

def generate_uuid( ) :
    return str(uuid.uuid4())


def set_ss( ss_data ) :
    try:
        raw_data = util.encode( ss_data )
        mc = memcache.Client( etc.memcached_addr, debug=0 )
        if mc.set( 'ss_'+ss_data.ss_id, raw_data, etc.session_timeout ) :
            return True
        return False
    except Exception as e:
        log.exp(e)
        return False


def get_ss( ss_id ) :
    try:
        mc = memcache.Client( etc.memcached_addr, debug=0 )
        raw_data = mc.get( 'ss_'+ss_id )
        ss_data = None
        if raw_data :
            ss_data = util.decode( raw_data )
        return ss_data
    except Exception as e:
        log.exp(e)
        return None


def delete_ss( ss_id ) :
    try:
        mc = memcache.Client( etc.memcached_addr, debug=0 )
        if mc.delete( 'ss_'+ss_id, 0 ) :
            return True
        return False
    except Exception as e:
        log.exp(e)
        return False


def replace_ss( ss_data ) :
    try:
        raw_data = util.encode( ss_data )
        mc = memcache.Client( etc.memcached_addr, debug=0 )
        if mc.replace( 'ss_'+ss_data.ss_id, raw_data, etc.session_timeout ) :
            return True
        return False
    except Exception as e:
        log.exp(e)
        return False


class McSessionStore( session_base.BaseSessionStore ) :

    def contains( self, key ) :
        raise NotImplementedError

    def cleanup( self ) :
        raise NotImplementedError

    def get( self, ss_id ) :
        return get_ss( ss_id )

    def set( self, ss_data ) :
        return set_ss( ss_data )

    def delete( self, ss_id ) :
        return delete_ss( ss_id )

    def replace( self, ss_data ) :
        return replace_ss( ss_data )


class BaseHandler( tornado.web.RequestHandler ) :

    def initialize( self ):
        self.ss_store = McSessionStore()
        self.ss_data = None
        return

    def write_error( self, status_code, **kwargs ) :
        self.render( '503.html' )

    def get_current_user( self ) :
        try:
            uuid = self.get_cookie( etc.cookie_uuid )
            if not uuid :
                log.i( 'no uuid' )
                expires = datetime.datetime.utcnow() + datetime.timedelta(days=365)
                uuid = generate_uuid()
                domain = util.get_domain_from_host( self.request.host )
                self.set_cookie( etc.cookie_uuid, uuid, domain=domain, expires=expires )
            self.uuid = uuid
            usr_ss_id = self.get_secure_cookie( etc.cookie_name )
            usr_ss_id_hmac = self.get_secure_cookie( etc.cookie_verify )
            if not usr_ss_id or not usr_ss_id_hmac :
                log.i( 'no cookie' )
                self.clear_cookie( etc.cookie_name )
                self.clear_cookie( etc.cookie_verify )
                self.ss_data = None
                return None
            check_hmac = session_base.generate_hmac( usr_ss_id )
            if usr_ss_id_hmac != check_hmac :
                log.w("evil session : %s %s"%(usr_ss_id,usr_ss_id_hmac))
                self.clear_cookie( etc.cookie_name )
                self.clear_cookie( etc.cookie_verify )
                self.ss_data = None
                return None
            old_ss_data = self.ss_store.get( usr_ss_id )
            if old_ss_data == None :
                log.i("session expired")
                self.clear_cookie( etc.cookie_name )
                self.clear_cookie( etc.cookie_verify )
                self.ss_data = None
                return None
            self.ss_data = old_ss_data
            return self.ss_data
        except Exception as e :
            log.exp(e)
            self.clear_cookie( etc.cookie_name )
            self.clear_cookie( etc.cookie_verify )
            self.ss_data = None
            return self.ss_data


if __name__ == "__main__":
    key='None'
    try:
        key = str(sys.argv[1])
    except Exception as e:
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


