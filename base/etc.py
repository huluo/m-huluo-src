#!/usr/bin/env python
# -*- coding: utf-8 -*-

memcached_addr = ["127.0.0.1:8001"]
redis_host     = '127.0.0.1'
redis_port     = 8002

session_secret = 'uIyh3Kv7TWGHrdksrUdumBjBP57KhUEQi6T8lMHfSgc'
appkey_secret = 'z3uFoxJ7S0OOEAiOmZw1LNTtq5aXzkX7u36KJ6vti54='
pw_secret = 'Sk4Ys7sPTx+gT5ssPHXV4ieKwPMKB0czjb+2rVfICMo='
cookie_secret = "/NHkbgvLTxOnZosYcuMEIiN+NitBXE3CudkFY3nwGk8="

session_timeout = 3600
persist_timeout = 0
item_timeout = 600
node_timeout = 600

cookie_name = 'toki_session_id'
cookie_verify = 'toki_session_verify'
cookie_uuid= 'toki_rongo_uuid'

path_template_pfx   = "/opt/m-huluo-server/static/html"
path_static_pfx     = "/opt/m-huluo-server/static/html"
path_log            = "/opt/m-huluo-server/logs"
path_taobao_lib     = "/opt/m-huluo-server/lib/taobao-sdk-python"

mail_regex = r'^([a-zA-Z0-9_-]|\.)+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$'

err_500         = '服务器正在思考人生，请稍后再试'
err_timeout     = '请求超时，请刷新重试'
err_op_fail     = '无法完成此操作'
err_no_api      = '此接口暂未开放'

url = {
    'user_main'           : r"/" ,
    'user_index'          : r"/index" ,
    'user_home'           : r"/home" ,
    'user_api_signout'    : r"/user/api/signout" ,
    'user_api_signup'     : r"/user/api/signup" ,
    'user_api_findpwd'    : r"/user/api/findpwd" ,
    'user_api_resetpwd'   : r"/user/api/resetpwd" ,
    'user_api_emailedit'  : r"/user/api/emailedit" ,
    'user_api_pwdedit'    : r"/user/api/pwdedit" ,
    'user_guest_signout'  : r"/user/signout" ,
    'user_guest_findpwd'  : r"/user/findpwd" ,
    'user_guest_resetpwd' : r"/user/resetpwd" ,
}

