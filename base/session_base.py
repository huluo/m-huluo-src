#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web
import hmac
import uuid
import datetime
import json
import hashlib
import etc
import util
import data_user
import log

def generate_id() :
    new_id = hashlib.sha256( etc.session_secret + str(uuid.uuid4()) )
    return new_id.hexdigest()


def generate_hmac( ss_id ) :
    return hmac.new( ss_id, etc.session_secret, hashlib.sha256 ).hexdigest()


class SessionData( dict ) :

    def __init__( self, ss_id, data ) :
        self.ss_id = ss_id
        self.update( data )

    def __missing__( self, key ) :  
        return None


def Session( request ) :

    @tornado.web.authenticated
    def Process( handler, *args ) :
        #请求前重建Session数据的过程
        #
        #执行原本请求的方法
        request( handler, *args )
        #请求完成后保存Session数据的过程
        if handler.ss_data != None:
            handler.ss_store.replace( handler.ss_data )
    return Process


def ApiSession( request ) :

    @tornado.web.asynchronous
    def Process( handler, *args ) :
        #请求前检验Session数据的过程
        handler.get_current_user()
        if handler.ss_data == None :
            res = { 'op':False, 'msg':'使用此功能需要登录' }
            handler.write( json.dumps(res) )
            handler.finish()
            return
        #执行原本请求的方法
        try:
            request( handler, *args )
        except Exception as e:
            log.exp(e)
            res = { 'op':False, 'msg':etc.err_500 }
            handler.write( json.dumps(res) )
            handler.finish()
            return
        #请求完成后保存Session数据的过程
        if handler.ss_data != None:
            handler.ss_store.replace( handler.ss_data )
    return Process


def NewSession( request ) :

    @tornado.web.asynchronous
    def Process( handler, *args ) :
        #请求前重建Session数据的过程
        try :
            email = handler.get_argument( 'email',default=None )
            passwd = handler.get_argument( 'passwd',default=None )
            rememberme = handler.get_argument( 'rememberme',default=None )
            log.i( 'email=%s , passwd=%s , rememberme=%s' % (email,passwd,rememberme) )
            expires = None
            if rememberme == "on" :
                expires = datetime.datetime.utcnow() + datetime.timedelta(days=365)
            if not email or not passwd:
                log.w( 'empty email or passwd' )
                res = { 'op':False, 'msg':'邮箱和密码不能为空' }
                handler.write( json.dumps(res) )
                handler.finish()
                return
            email = email.strip().lower()
            domain = util.get_domain_from_host( handler.request.host )
            #user = data_user.get_user_by_email( mongo.db_pool[domain].user, email, passwd )
            user = None
            handler.ss_id = None
            if not user:
                log.w( 'no such user' )
                res = { 'op':False, 'msg':'邮箱或密码错误' }
                handler.write( json.dumps(res) )
                handler.finish()
                return
            if passwd != user['pw'] :
                log.w( 'passwd err'+' '+ user['pw'] )
                res = { 'op':False, 'msg':'邮箱或密码错误' }
                handler.write( json.dumps(res) )
                handler.finish()
                return
            if user['ss']['ssid'] :
                old_ss_id = str( user['ss']['ssid'] )
                old_ss_data = handler.ss_store.get( old_ss_id )
                if old_ss_data :
                    log.i( "old session : uid=%s , ssid=%s" % (user['uid'],old_ss_id) )
                    handler.ss_id = old_ss_id
            if not handler.ss_id :
                handler.ss_id = generate_id()
                log.i( "new session : uid=%s , ssid=%s" % (user['uid'],handler.ss_id) )
            handler.ss_id_hmac = generate_hmac( handler.ss_id )
            handler.set_secure_cookie( etc.cookie_name, handler.ss_id, domain=domain, expires=expires )
            handler.set_secure_cookie( etc.cookie_verify, handler.ss_id_hmac, domain=domain, expires=expires )
            #data_user.set_login( mongo.db_pool[domain].user, user['uid'], handler.ss_id )
            handler.ss_user = user
            #执行原本请求的方法
            request( handler, *args )
        except Exception as e :
            log.exp(e)
            res = { 'op':False, 'msg':etc.err_500 }
            handler.write( json.dumps(res) )
            handler.finish()
            return
        #请求完成后保存Session数据的过程
    return Process


class BaseSessionStore:
    """Base class for session stores"""
    def contains( self, key ) :
        raise NotImplementedError

    def cleanup( self ) :
        raise NotImplementedError

    def get( self, ss_id ) :
        raise NotImplementedError

    def set( self, ss_data ) :
        raise NotImplementedError

    def delete( self, ss_id ) :
        raise NotImplementedError

    def replace( self, ss_data ) :
        raise NotImplementedError


class InvalidSessionException(Exception) :
    pass


