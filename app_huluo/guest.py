#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import urllib
import json
import etc
import conf
import util
import log
from session_mc import BaseHandler


class MainHandler( BaseHandler ) :

    def get( self ) :
        next = self.get_argument( 'next', default=conf.url['guest_main'] )

        self.render( "guest_main.html",
                p_msg = conf.msg,
                p_url = conf.url,
                p_next = urllib.quote(next),
                p_host_name = conf.host_name,
            )


class PageNotFoundHandler( BaseHandler ) :

    def get( self ) :
        raise tornado.web.HTTPError( 503 )



