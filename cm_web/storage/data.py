#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#  
#    author :jianwen
#    Date :2016-01-09
#                                        
#
############################################################################

try:
    import cPickle as pickle
except ImportError:
    import pickle
from datetime import datetime, date, timedelta
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import UniqueConstraint
import time
import random
from flask import current_app, jsonify, session,url_for
from flask.ext.login import current_user, logout_user,UserMixin
from cm_web.storage import db, DuocData, DuocDataBase
from cm_web.helper import helper
from dateutil.relativedelta import relativedelta
import hashlib

__all__ = ['TeamMember','Investment','News','ContactAddr','NewsType',
        'InvestmentType','Indexcarousel','AboutUs','Admin']

class Admin(db.Model, DuocData,UserMixin):

    id = db.Column( db.BigInteger,primary_key=True)
    status = db.Column( db.SmallInteger,default=3)
    account_name = db.Column( db.String,index=True)
    password = db.Column( db.String )

    create_time = db.Column( db.DateTime, \
            default=datetime.now)
    update_time = db.Column( db.DateTime, \
            default=datetime.now,onupdate = datetime.now)

    def __init__(self,account_name,password):
        self.id = helper.dcid()
        myMd5 = hashlib.md5()
        myMd5.update(password)
        myMd5_Digest = myMd5.hexdigest()
        self.password = myMd5_Digest
        self.account_name = account_name

    def get_id(self):  # login所需
        return self.id


    @property
    def is_active(self): # login所需
        return True
    
    @property
    def is_anonymous(self):
        return False

    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True




class AboutUs( db.Model,DuocData):
    id = db.Column( db.BigInteger,primary_key=True)
    status = db.Column( db.SmallInteger,default=3)
    bg_image = db.Column( db.String)
    title = db.Column( db.String)
    slogan = db.Column( db.String)
    create_time = db.Column( db.DateTime, \
            default=datetime.now)
    update_time = db.Column( db.DateTime, \
            default=datetime.now,onupdate = datetime.now)
    top = db.Column(db.Boolean,default=False)

    def __init__(self,bg_image,title,slogan):
        self.id = helper.dcid()
        self.bg_image = bg_image
        self.title = title
        self.slogan = slogan


    @property
    def about_us(self):
        return {
            'tab_id'    :str(self.id),
            'title'     :self.title,
            'bg_image'  :self.bg_image,
            'slogan'    :self.slogan,
                }

class Indexcarousel( db.Model,DuocDataBase ):
    id = db.Column( db.BigInteger,primary_key=True)
    image = db.Column( db.String )
    title = db.Column( db.String )
    content = db.Column( db.String )
    create_time = db.Column( db.DateTime, \
            default=datetime.now)
    update_time = db.Column( db.DateTime, \
            default=datetime.now,onupdate = datetime.now)

    def __init__( self,image,title,content):
        self.id = helper.dcid()
        self.image = image
        self.title = title 
        self.content = content 

    def __repr__( self ):
        return "<image %s>" % self.image

    @property
    def carousel( self ):
        return {
                'image_id'  :str(self.id),     
                'image'  :self.image,
                'title'  :self.title,
                'content'   :self.content
            }

class TeamMember( db.Model,DuocData ):
    id = db.Column(db.BigInteger,primary_key=True)
    status = db.Column(db.SmallInteger,default=3,index=True)
    light_avatar = db.Column(db.String)
    dark_avatar = db.Column(db.String)
    name = db.Column(db.String)
    description = db.Column(db.String)
    top = db.Column(db.Boolean,default=False)
    create_time = db.Column( db.DateTime, \
            default=datetime.now)
    update_time = db.Column( db.DateTime, \
            default=datetime.now,onupdate = datetime.now)


    def __init__(self,light_avatar,dark_avatar,
            name,description):
        self.id = current_app.helper.dcid()
        self.light_avatar = light_avatar
        self.dark_avatar = dark_avatar
        self.name = name
        self.description = description

    def __repr__(self):
        return "Member:%s" % self.name

    @property
    def tm_meta(self):
        return{
                'tm_id'        :str(self.id),
                'light_avatar' :current_app.oss.original(self.light_avatar),
                'dark_avatar'  :current_app.oss.original(self.dark_avatar),
                'name'         :self.name,
                'description'  :self.description
                }


class Investment( db.Model,DuocData):
    id = db.Column(db.BigInteger,primary_key=True)
    status = db.Column( db.SmallInteger,default=3,index=True)
    company_name = db.Column( db.String,index=True)
    cover_image = db.Column( db.String)
    company_url = db.Column( db.String)
    company_addr = db.Column(db.String)
    pm_manager = db.Column( db.String) #项目负责人
    company_introduce = db.Column( db.String)
    top = db.Column(db.Boolean,default=False)
    create_time = db.Column( db.DateTime,
            default = datetime.now)
    update_time = db.Column( db.DateTime,
            default=datetime.now,onupdate=datetime.now) 

    im_types = db.relationship('InvestmentType', 
            secondary='investment_investment_type',
            backref=db.backref('investments',order_by=db.desc('create_time')),
            lazy='dynamic')



    def __init__(self,company_name,cover_image,company_url,
            company_addr,pm_manager,company_introduce):
        self.id = helper.dcid()
        self.company_name = company_name
        self.cover_image = cover_image
        self.company_url = company_url
        self.company_addr = company_addr
        self.pm_manager = pm_manager
        self.company_introduce = company_introduce

    def __repr__(self):
        return "<investment %s,%s>" % (self.id,self.company_name)

    @property
    def im_info(self):
        try:
            company_type = InvestmentType.query.from_statement(db.text(
                'select a.* from investment_investment_type as b  '
                'join investment_type as a on a.id=b.type_id '
                'where b.im_id=:tid'
                )).params(tid=self.id).first()
        except Exception,e:
            print e
            raise CMException(info=e,log_msg=e)
        return {
            'im_id'     :str(self.id),
            'company_name'  :self.company_name,
            'cover_image'   :current_app.oss.original(self.cover_image),
            'company_url'   :self.company_url,
            'company_addr'  :self.company_addr,
            'pm_manager'    :self.pm_manager,
            'company_introduce' : self.company_introduce,
            'company_type'      : company_type.type_name if company_type \
                    else None
            }

class InvestmentType(db.Model,DuocDataBase):
    id = db.Column( db.BigInteger,primary_key=True)
    type_name = db.Column( db.String )
    description = db.Column( db.String)
    create_time = db.Column( db.DateTime,default=datetime.now)
    update_time = db.Column( db.DateTime,default= datetime.now,
            onupdate=datetime.now)

    def __init__(self,type_name,description=None):
        self.id = helper.dcid()
        self.type_name = type_name
        self.description = description

    def __repr__(self):
        return "<investment type:id=%s,name=%s>" % (self.type_name,
                self.description)

    @property
    def im_type_meta(self):
        return{
                'im_type_id' :str(self.id),
                'type_name'  :self.type_name
                }

investment_investment_type = db.Table('investment_investment_type', #投资项目关联表
        db.Column('im_id', db.BigInteger, 
            db.ForeignKey('investment.id', ondelete='CASCADE'),
            primary_key=True,index=True),
        db.Column('type_id', db.BigInteger, 
            db.ForeignKey('investment_type.id', ondelete='CASCADE'),
            primary_key=True, index=True)
        )



class News( db.Model,DuocData):
    id = db.Column( db.BigInteger,primary_key=True)
    status = db.Column( db.SmallInteger,default=3,index=True)
    title = db.Column( db.String)
    cover_image = db.Column( db.String)
    content = db.Column( db.String) #此处存储的是h5的内容
    top = db.Column(db.Boolean,default=False)
    create_time = db.Column( db.DateTime,default=datetime.now)
    update_time = db.Column( db.DateTime,default= datetime.now,
            onupdate=datetime.now)

    news_types = db.relationship('NewsType', 
            secondary='news_news_type',
            backref=db.backref('news',order_by=db.desc('create_time')),
            lazy='dynamic')

    def __init__(self,title,cover_image,content):
        self.id = helper.dcid()
        self.title = title
        self.cover_image = cover_image
        self.content = content

    def __repr__(self):
        return "<news %s,%s>" % (self.id,self.title)
    
    @property
    def news_meta(self):
        try:
            news_type = NewsType.query.from_statement(db.text(
                'select a.* from news_news_type as b  '
                'join news_type as a on a.id=b.type_id '
                'where b.news_id=:tid'
                )).params(tid=self.id).first()
        except Exception,e:
            print e
            raise CMException(info=e,log_msg=e)

        return {
                'news_id'   :str(self.id),
                'title'     :self.title,
                'create_time'   :self.create_time.strftime("%Y-%m-%d"),
                'cover_image'   :current_app.oss.original(self.cover_image),
                'content'       :self.content,
                'news_type'     :news_type.type_name if news_type \
                        else None
            }

class NewsType(db.Model,DuocDataBase):
    id = db.Column( db.BigInteger,primary_key=True)
    type_name = db.Column( db.String )
    description = db.Column( db.String)
    create_time = db.Column( db.DateTime,default=datetime.now)
    update_time = db.Column( db.DateTime,default= datetime.now,
            onupdate=datetime.now)

    def __init__(self,type_name,description=None):
        self.id = helper.dcid()
        self.type_name = type_name
        self.description = description

    def __repr__(self):
        return "<news type:id=%s,name=%s>" % (self.type_name,
                self.description)

    @property
    def news_type_meta(self):
        return{
                'news_type_id' :str(self.id),
                'type_name'  :self.type_name
                }


news_news_type = db.Table('news_news_type',          #赞动态
        db.Column('news_id', db.BigInteger, 
            db.ForeignKey('news.id', ondelete='CASCADE'),
            primary_key=True,index=True),
        db.Column('type_id', db.BigInteger, 
            db.ForeignKey('news_type.id', ondelete='CASCADE'),
            primary_key=True, index=True)
        )

class ContactAddr(db.Model,DuocData):
    id = db.Column( db.BigInteger,primary_key=True)
    status = db.Column(db.SmallInteger,default=3,index=True)
    city = db.Column( db.String)
    cover_image = db.Column(db.String)
    detail_addr = db.Column( db.String)
    phone = db.Column( db.String)
    mail = db.Column( db.String)
    fax_no = db.Column( db.String) #传真号码
    baidu_share = db.Column( db.String) #百度分享链接
    create_time = db.Column( db.DateTime,default=datetime.now)
    update_time = db.Column( db.DateTime,default=datetime.now,
            onupdate=datetime.now)

    def __init__( self,city,cover_image,detail_addr,phone,mail,
            fax_no,baidu_share):
        self.id = helper.dcid()
        self.city = city
        self.cover_image = cover_image
        self.detail_addr = detail_addr
        self.phone = phone
        self.mail = mail
        self.fax_no = fax_no
        self.baidu_share

    def __repr__(self):
        return "<contact addr %s,%s>" % (self.id,self.city)

    @property
    def contact_addr(self):
        return {
                'addr_id'   :str(self.id),
                'city'      :self.city,
                'cover_image'   :current_app.oss.original(self.cover_image),
                'detail_addr'   :self.detail_addr,
                'phone'         :self.phone,
                'mail'          :self.mail,
                'fax_no'        :self.fax_no,
                'baidu_share'        :self.baidu_share
            }




db.create_all()
