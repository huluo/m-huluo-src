#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.escape
import tornado.httpserver
import guest
import host
import user
import log
import conf
import etc


class Application( tornado.web.Application ) :

    def __init__( self ) :
        settings = dict(
            template_path = conf.path_template,
            static_path = conf.path_static,
            cookie_secret = etc.cookie_secret,
            login_url = conf.url['host_home'],
            xsrf_cookies = False,
        )
        handlers = [
            (conf.url['guest_main']               , guest.MainHandler) ,
            (conf.url['guest_index']              , guest.MainHandler) ,
            (conf.url['host_home']                , host.HomeHandler) ,
            (conf.url['user_login']               , user.LoginHandler) ,
            ('.*', guest.PageNotFoundHandler),
        ]
        tornado.web.ErrorHandler = guest.PageNotFoundHandler
        tornado.web.Application.__init__( self, handlers, **settings )
 

def main( p_port ) :
    if p_port == 0 :
        print 'port could not be set as 0'
        log.e( 'port could not be set as 0' )
        exit( 1 )
    log.c( 'www listening on port : %s' % p_port )
    app = Application()
    app.listen( p_port )
    tornado.ioloop.IOLoop.instance().start()


#define("port", default=8888, help="run on the given port", type=int)
port = 0
try :
    port = int( sys.argv[1].split('=')[1] )
except :
    print 'need port params'
    log.e( 'need port params' )
    exit( 1 )


if __name__ == "__main__" :
    main( port )


