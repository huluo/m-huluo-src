#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado
import datetime
import urllib
import etc
import conf
import log
import conf
from session_base import Session
from session_mc import BaseHandler


class HomeHandler( BaseHandler ) :

    @tornado.web.asynchronous
    def get( self ) :
        next = self.get_argument( 'next', default=conf.url['host_home'] )
        self.get_current_user()
        self.render( "host_home.html",
                p_msg = conf.msg,
                p_url = conf.url,
                p_next = urllib.quote(next),
            )


