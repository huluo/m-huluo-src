#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import etc
import util
import data_user
import log
from session_mc import BaseHandler


class SignOutHandler( BaseHandler ) :

    def get( self ) :
        try:
            self.clear_all_cookies()
            if self.get_current_user() :
                domain = util.get_domain_from_host( self.request.host )
                #data_user.set_logout( mongo.db_pool[domain].user, self.ss_data['uid'] )
                self.ss_store.delete( self.ss_data.ss_id )
        except Exception as e :
            log.exp( e )
        finally:
            self.ss_data = None
        self.redirect(etc.url['user_home'])


class FindPwdHandler( BaseHandler ) :

    def get( self ) :
        return self.render( "user_find_pwd.html",
                p_url = etc.url,
                p_session = self.ss_data,
                p_next = None,
            )


class ResetPwdHandler( BaseHandler ) :

    def get( self ) :
        try:
            vid = self.get_argument( 'vid', default=None )
            log.i('vid=%s' % vid)
            domain = util.get_domain_from_host( self.request.host )
            #reset = data_user.get_reset( mongo.db_pool[domain].reset, vid )
            reset = NOne
            if not reset:
                log.w('no such reset pwd')
                return self.redirect( etc.url['user_main'] )
            else:
                log.i( 'verify success' )
                return self.render( "user_reset_pwd.html",
                        p_url = etc.url,
                        p_session = self.ss_data,
                        p_pwsecret = etc.pw_secret,
                        p_next = None,
                        p_email = reset['email'],
                        p_vid = reset['vid'],
                    )
        except Exception as e :
            log.exp( e )
            self.redirect( etc.url['user_main'] )


class PageNotFoundHandler( BaseHandler ) :

    def get( self ) :
        raise tornado.web.HTTPError( 404 )


