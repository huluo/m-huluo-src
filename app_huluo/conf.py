#!/usr/bin/env python
# -*- coding: utf-8 -*-

import etc

host_name = 'huluo'
domain_name = host_name+'.com'
pfx = host_name

path_template = etc.path_template_pfx+'/'+pfx
path_static = etc.path_static_pfx+'/'+pfx

url = {
    'guest_main'               : r"/" ,
    'guest_index'              : r"/index" ,
    'host_home'                : r"/home" ,
    'user_login'               : r"/user/login" ,
}
url.update( etc.url )

msg = {
    'err_500'           : etc.err_500,
    'err_timeout'       : etc.err_timeout,
    'err_op_fail'       : etc.err_op_fail,
    'err_no_api'        : etc.err_no_api,
}

