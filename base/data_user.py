#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import util
import etc

"""user collection has 
   uid:        用户id (int)
   email:      注册邮箱 (str)
   pw:         密码，密文 (str)
   ss:         当前已经登录的用户ssid和sshmac (dict)
   ltime:      最后一次登录 (datetime)
"""
"""reset collection has
   vid:         唯一标识串 (str)
   email:       email命名 (str)
   rtime:       reset时间 (datatime)
"""

def create_user( col_user, uid, email, pwd ) :
    res = col_user.insert({
            'uid': uid,
            'email': email,
            'pw': pwd,
            'ss': {
                    'ssid': None,
                    'sstime': datetime.datetime.now()
                },
        })
    return res


def update_user_by_email( col_user, email, pwd ) :
    return col_user.update(
            {
                'email': email,
            },
            {'$set': {
                    'pw': pwd,
                }
            }
        )

def update_user_by_id( col_user, uid, email, pwd ):
    return col_user.update(
        {
            'uid': uid,
        },
        {'$set': {
                'email': email,
                'pw': pwd,
            }
        }
    )


def find_user_by_email( col_user, email ) :
    return col_user.find_one({'email': email})


def get_user_by_email( col_user, email, pw ) :
    return col_user.find_one({'email': email})


def get_user_by_id( col_user, uid ) :
    return col_user.find_one({'uid': uid})


def set_login( col_user, uid, ssid ) :
    return col_user.update(
            {
                'uid': long(uid)
            },
            {'$set': {
                'ss': {
                        'ssid': ssid,
                        'sstime': datetime.datetime.now()
                    }
                }
            }
        )


def set_logout( col_user, uid ) :
    user = get_user_by_id( col_user, uid )
    if not user:
        return None
    return col_user.update(
            {'uid': long(uid)},
            {'$set': {
                'ss': {
                        'ssid': None,
                        'sstime': user['ss']['sstime'],
                    }
                }
            }
        )


def create_reset( col_reset, email, vid ) :
    return col_reset.update(
            {
                'email': email,
            },
            {
                'vid': vid,
                'atime': datetime.datetime.now()
            },
            True,
        )


def get_reset( col_reset, vid ) :
    return col_reset.find_one({'vid': vid})


def del_reset( col_reset, email ) :
    return col_reset.remove({
            'email': email,
        })

def create_seq_userid( col_counter, start_num ) :
    if not col_counter.find_one( {'_id':etc.key_userseq} ) :
        col_counter.save(
            {
                '_id' : etc.key_userseq,
                'seq' : start_num,
            }
        )


def count_userid( col_counter ) :
    ret = col_counter.find_and_modify(
            query = { '_id' : etc.key_userseq },
            update = { '$inc' : { 'seq' : 1 } },
        )
    return ret['seq']


def create_seq_resetid( col_counter, start_num ) :
    if not col_counter.find_one( {'_id':etc.key_resetseq} ) :
        col_counter.save(
            {
                '_id' : etc.key_resetseq,
                'seq' : start_num,
            }
        )


def count_resetid( col_counter ) :
    ret = col_counter.find_and_modify(
            query = { '_id' : etc.key_resetseq },
            update = { '$inc' : { 'seq' : 1 } },
        )
    return ret['seq']


