#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
一个url_item的例子:
5297167533L: {
    u'title': u'\u53cc\u94f6\u65d7\u8230\u5e97 \u590d\u53e4 \u8d85\u5927\u5341\u5b57\u67b6\u6cf0\u94f6\u540a\u5760 \u578b\u7537\u81f3\u7231', 
    u'price': u'468.00', 
    u'num_iid': 5297167533, 
    u'item_imgs': {
        u'item_img': [
            {u'url': u'http://img02.taobaocdn.com/bao/uploaded/i2/T1d0qeXfpkXXcUn8A8_071452.jpg', u'position': 0, u'id': 0}, 
            {u'url': u'http://img04.taobaocdn.com/bao/uploaded/i4/391839930/T2B8tjXXlbXXXXXXXX_!!391839930.jpg', u'position': 1, u'id': 188226914}, 
            {u'url': u'http://img07.taobaocdn.com/bao/uploaded/i7/391839930/T2bQNjXXJXXXXXXXXX_!!391839930.jpg', u'position': 2, u'id': 505218157}, 
            {u'url': u'http://img07.taobaocdn.com/bao/uploaded/i7/391839930/T2cANjXXJXXXXXXXXX_!!391839930.jpg', u'position': 3, u'id': 505218173}, 
            {u'url': u'http://img02.taobaocdn.com/bao/uploaded/i2/391839930/T2ekNjXXBXXXXXXXXX_!!391839930.jpg', u'position': 4, u'id': 505218189}
        ]
    }, 
    u'detail_url': u'http://item.taobao.com/item.htm?id=5297167533&spm=2014.21419355.0.0', 
    u'pic_url': u'http://img02.taobaocdn.com/bao/uploaded/i2/T1d0qeXfpkXXcUn8A8_071452.jpg',
    u'ctime': util.datetime_now_str(),
}

'''

import log
import conf
from sqlalchemy.orm import mapper, sessionmaker
from datetime import datetime
from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, BigInteger, String, Unicode, UnicodeText, DateTime
from sqlalchemy.engine import create_engine

class UrlItem( object ) : #创建一个映射类

    def to_item( self ) :
        res = {}
        res['urlid'] = self.urlid
        res['appid'] = self.appid
        res['title'] = self.title
        res['desc'] = self.tag
        #res['name'] = self.name
        res['price'] = self.price
        res['num_iid'] = self.num_iid
        res['item_imgs'] = self.item_imgs
        res['detail_url'] = self.detail_url
        res['pic_url'] = self.pic_url
        return res

    def __repr__( self ) :
        return "%d"%(self.urlid)


#创建到数据库的连接,echo=True表示用logging输出调试结果
engine = create_engine('mysql://root:@localhost:8004/'+conf.host_name+'?charset=utf8',encoding = "utf-8",echo =True) 
metadata = MetaData()
Session = sessionmaker() #创建了一个自定义了的 Session类
Session.configure(bind=engine)  #将创建的数据库连接关联到这个session
url_itm_table = Table(
    'url_item', metadata,
    Column('id', Integer, primary_key=True),
    Column('urlid', Integer, index=True, unique=True, nullable=False),
    Column('appid', Integer, index=True, nullable=False),
    Column('title', Unicode(65), nullable=False),
    Column('tag', Unicode(65), default=''),
    Column('name', Unicode(65), default=''),
    Column('price', Unicode(65), nullable=False),
    Column('num_iid', BigInteger, nullable=False),
    Column('item_imgs', UnicodeText(), nullable=False),
    Column('detail_url', Unicode(127), nullable=False),
    Column('pic_url', Unicode(127), nullable=False),
    Column('ctime', DateTime, default=datetime.now)
)


def createUrlItemTable() :
    metadata.create_all( engine ) #在数据库中生成表
    mapper( UrlItem, url_itm_table ) #把表映射到类


createUrlItemTable() 


def add_item( pItem ) :
    try :
        session = Session()
        session.add( pItem ) #往session中添加内容
        session.flush() #保存数据
        session.commit() #数据库事务的提交,sisson自动过期而不需要关闭
        return True
    except Exception as e :
        log.exp(e)
        session.rollback()
        return False


def del_item( pUrlid ) :
    try :
        session = Session()
        query = session.query( UrlItem )
        query.filter_by( urlid=pUrlid ).delete()
        session.flush() #保存数据
        session.commit() #数据库事务的提交,sisson自动过期而不需要关闭
        return True
    except Exception as e :
        log.exp(e)
        session.rollback()
        return False


def get_item( pUrlid ) :
    try :
        session = Session()
        query = session.query( UrlItem )
        item = query.filter_by(urlid=pUrlid).first()
        item.item_imgs = eval( item.item_imgs )
        return item
    except Exception as e :
        log.exp(e)
        return None


def get_item_dict( pUrlids ) :
    item_dict = {}
    try :
        session = Session()
        query = session.query( UrlItem )
        items = query.filter( UrlItem.urlid.in_(pUrlids) ).all()
        for item in items :
            item.detail_url = item.detail_url.replace('\\','')
            tmp_imgs = eval( item.item_imgs )
            for item_img in tmp_imgs['item_img'] :
                item_img['url'] = item_img['url'].replace('\\','')
            item.item_imgs = tmp_imgs
            item_dict[item.urlid] = item.to_item()
        return item_dict
    except Exception as e :
        log.exp(e)
        return item_dict


def update_item( pItem ) :
    try :
        session = Session()
        session.merge( pItem )
        session.commit() #提交事务
        return True
    except Exception as e :
        log.exp(e)
        session.rollback()
        return False


def update_desc( pUrlid, pDesc ) :
    try :
        session = Session()
        session.query( UrlItem ).filter( UrlItem.urlid==pUrlid ).update( {UrlItem.tag:pDesc} , synchronize_session=False ) 
        session.commit() #提交事务
        return True
    except Exception as e :
        log.exp(e)
        session.rollback()
        return False


def update_name( pAppid, pName) :
    try :
        session = Session()
        session.query( UrlItem ).filter( UrlItem.appid==pAppid ).update( {UrlItem.name:pName} , synchronize_session=False ) 
        session.commit() #提交事务
        return True
    except Exception as e :
        log.exp(e)
        session.rollback()
        return False


def update_appid( pUrlids, pAppid ) :
    try :
        session = Session()
        session.query( UrlItem ).filter( UrlItem.urlid.in_(pUrlids) ).update( {UrlItem.appid:pAppid} , synchronize_session=False ) 
        session.commit() #提交事务
        return True
    except Exception as e :
        log.exp(e)
        session.rollback()
        return False


if __name__ == "__main__" :
    item3 = UrlItem()
    item3.urlid=10000003
    item3.appid=10000003
    item3.title='广西北海涠洲岛旅游手绘地图【酒店景点吃住游玩攻略】2.0版本'
    item3.tag='哈迪斯2'
    item3.name='石头人'
    item3.price='123.00'
    item3.num_iid=12345688
    item3.item_imgs='哈迪斯2'
    item3.detail_url='哈迪斯3'
    item3.pic_url='哈迪斯4'
    add_item( item3 )
    '''
    pUrlids = [200000715]
    item_dict = get_item_dict( pUrlids )
    print item_dict
    '''

