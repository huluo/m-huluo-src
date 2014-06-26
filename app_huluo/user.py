#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado
import tornado.web
import uuid
import datetime
import re
import urllib
import urlparse
import log
import etc
import conf
import json
import session_base
from session_base import ApiSession
from session_base import NewSession
from session_mc import BaseHandler


class LoginHandler( BaseHandler ) :

    def get( self ) :
        log.i( 'hello word' )
        #log.i( 'hello word' % (self.ss_user['uid']) )
        name = self.get_argument( 'name', default='yexiang' )
        msg = 'hello ' + name
        res = { 'op':True, 'msg':msg }
        self.write( json.dumps(res) )
        self.finish()
        return


class ApiNotFoundHandler( BaseHandler ) :

    def get( self ) :
        raise tornado.web.HTTPError( 503 )

    @tornado.web.asynchronous
    def post( self ) :
        log.i( '503' )
        res = { 'op':False, 'msg':'无此功能' }
        self.write( json.dumps(res) )
        self.finish()


