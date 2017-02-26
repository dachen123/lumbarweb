#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:   jianwen
# company:  duoc
# date:     2016-01-09
#

from flask.ext.sqlalchemy import SQLAlchemy
from flask import current_app, g
__all__ = [ 'db' ]

class DuocSQLAlchemy(SQLAlchemy):
    """
    Flask-SQLAlchemy 有一个BUG，单独执行 init_app 不会把 self.app = app 设置
    所以封装一下，修正这个BUG
    """
    def __init__(self, app=None, user_native_unicode=True, session_options=None):
        super(DuocSQLAlchemy, self).__init__(app, user_native_unicode, session_options)

    def init_app(self, app):
        self.app = app
        super(DuocSQLAlchemy, self).init_app(app)
        self.create_all()

    def commit(self):
        """
            为避免直接使用SQLAlchemy在操作数据库中容易抛出异常，
            封装一下db.session截断异常，防止程序中止
        """
        try:
            self.session.commit()
        except Exception as e:
            self.app.logger.exception("db.commit exception")
            print e.message
            # self.session.rollback()
            raise CMException(info=u'数据库检测到非法数据', log_msg=e.message)
            return False
        return True

    def rollback(self):
        db.session.rollback()

db = DuocSQLAlchemy()

class DuocDataBase(object):

    def update(self):
        '提交数据库更改''不需要手动提交，所以以下各函数没有调用update'
        pass

    def delete(self,commit=False):

        self.strict_rm(commit)

    def add_to_db(self, commit=False):
        "提交到数据库"
        db.session.add(self)
        return not commit or db.commit()

    def strict_rm(self, commit=False):
        '从数据库彻底删除'
        db.session.delete(self)
        return not commit or db.commit()

    @classmethod
    def get(cls, query_id):
        "通过 id 获取对象"
        if not query_id:
            return None
        query_id = int(query_id)
        ret = cls.query.filter_by(id=query_id).first()
        return ret

    def is_deleted(self):
        return False

class DuocData(DuocDataBase):

    """
    DUOC 数据库表的基类，所有表使用一个域status进行有效性管理
    status = db.Column( db.SmallInteger, default=3 )
    status 是一个bitmap，标记位说明：
            从右到左        1       |       0
                    0位： 存在      |       删除
                    1位： 审核通过  |   审核未通过
                    2位： 被冻结    |   正常状态
                    3位:  已审核    |   未审核
    本类定义了有效性的统一操作

    先审后发: 初始为0001(表示存在，未审核)
    先发后审: 初始为0011(表示存在，未审核，假定审核通过)

    """
    _valid_status = 3
    _personal_valid = 1
    _freeze_status = 7

    def is_valid(self):
        '检查该条目是否有效: bitmap x011'
        try:
            st = getattr(self, 'status')
            st = st & 7
            if st == self._valid_status:
                return True
            else:
                return False
        except Exception, e:
            current_app.logger.exception(e)
            raise DCError

    def get_status(self):
        'WS:未审核;BH:驳回;TG:通过;DJ:冻结;NE:不存在'
        try:
            st = getattr(self, 'status')
            st = st & 15
            if st&15 == 11:     # 1011
                return 'TG'
            if st&13 == 1:      # 00x1
                return 'WS'
            if st&15 == 9:      # 1001
                return 'BH'
            if st&5  == 5:      # x1x1
                return 'DJ'
            if st&1  == 0:      # xxx0
                return 'NE'
        except Exception, e:
            current_app.logger.exception(e)
            raise DCError

    def delete(self):
        '将该条目置为已删除'
        try:
            st = getattr(self, 'status')
            st = st & (~1)
            setattr(self, 'status', st)
        except Exception, e:
            current_app.logger.exception(e)
            raise DCError

    def restore(self):
        '恢复误删除的条目'
        try:
            st = getattr(self, 'status')
            st = st | 1
            setattr(self, 'status', st)
        except Exception, e:
            current_app.logger.exception(e)
            raise DCError

    def is_deleted(self):
        try:
            st = getattr(self, 'status')
            st = st & 1
            return True if st == 0 else False
        except Exception, e:
            current_app.logger.exception(e)
            raise DCError

    def exist(self):
        '检查是否存在，未被删除'
        try:
            st = getattr(self, 'status')
            return True if st & 1 else False
        except Exception, e:
            current_app.logger.exception(e)
            raise DCError

    def verify(self, is_pass=True):
        """
        '设置审核通过与否(同时标记已审核)'
        is_pass:
                True:   审核通过
                False:  审核不通过
        """
        try:
            st = getattr(self, 'status')
            if is_pass is True:
                st = st | 2
            else:
                st = st & (~2)
            setattr(self, 'status', st)

            st = st | 8
            setattr(self, 'status', st)

        except Exception, e:
            current_app.logger.exception(e)
            raise DCError

    def set_status(self,exist=True,verify_pass=True,freeze=False,
            has_verify=False):

        try:
            st = getattr(self, 'status')
            if exist:
                st = st | 1
            else:
                st = st & (~1)
            if verify_pass:
                st = st | 2
            else:
                st = st & (~2)
            if freeze:
                st = st | 4
            else:
                st = st & (~4)
            if has_verify:
                st = st | 8
            else:
                st = st & (~8)
            setattr(self, 'status', st)
            db.commit()

        except Exception, e:
            current_app.logger.exception(e)
            raise DCError

    @classmethod     
    def query_entry(cls,exist=True,verify_pass=True,freeze=False,
            has_verify=False):

        q = cls.query         
        tablename = "public.%s" % cls.__tablename__           #
        #条件:存在&&审核通过&&未被冻结
        fc = []
        if exist:
            fc.append('( %s.status & %d )::int = %d' % ( tablename, 1, 1 ))
        else:
            fc.append('( %s.status & %d )::int != %d' % ( tablename, 1, 1 ))
        if verify_pass:
            fc.append('( %s.status & %d )::int = %d' % ( tablename, 2, 2 ))
        else:
            fc.append('( %s.status & %d )::int != %d' % ( tablename, 2, 2 ))
        if freeze:
            fc.append('( %s.status & %d )::int = %d' % ( tablename, 4, 4 ))
        else:
            fc.append('( %s.status & %d )::int != %d' % ( tablename, 4, 4 ))
        if has_verify:
            fc.append('( %s.status & %d )::int = %d' % ( tablename, 8, 8 ))
        else:
            fc.append('( %s.status & %d )::int != %d' % ( tablename, 8, 8 ))

        q = q.filter( db.text(cls._and(fc)) )         
        return q

    def freeze(self, is_freeze=True):
        """
        is_freeze:
                True:   冻结
                False:  解除冻结
        """
        try:
            st = getattr(self, 'status')
            if is_freeze is True:
                st = st | 4
            else:
                st = st & (~4)
            setattr(self, 'status', st)
        except Exception, e:
            current_app.logger.exception(e)
            raise DCError

    @classmethod
    def real_get(cls, query_id):
        "通过 id 获取对象, 不检查状态"
        if not query_id:
            return None
        query_id = int(query_id)
        ret = cls.query.filter_by(id=query_id).first()
        if ret: 
            return ret
        else:
            return None


    @classmethod
    def get(cls, query_id):
        "通过 id 获取对象, 检查状态"
        if not query_id:
            return None
        query_id = int(query_id)
        ret = cls.query.filter_by(id=query_id).first()
        if ret and not ret.is_deleted():
            return ret
        else:
            return None

    #获取可用的条目，去除状态标志位不在可显示状态的条目     
    @classmethod     
    def query_valid_entry(cls):         
        q = cls.query         
        tablename = "public.%s" % cls.__tablename__           #
        fc = '( %s.status & %d )::int = %d' % ( tablename, 1, cls._personal_valid )
        q = q.filter( db.text(fc) )         
        return q

    #获取存在的条目，包括审核过未审核过     
    @classmethod     
    def query_exist_entry(cls):         
        q = cls.query         
        tablename = "public.%s" % cls.__tablename__           #
        fc = '( %s.status & %d )::int = %d' % ( tablename, 1, cls._personal_valid )
        q = q.filter( db.text(fc) )         
        return q

    @classmethod     
    def _and(cls,filter_clause=[]):

        return ' ( ' + ' and '.join(filter_clause) + ' ) '

    @classmethod     
    def _or(cls,filter_clause=[]):

        return ' ( ' + ' or '.join(filter_clause) + ' ) '

    #获取存在而未被冻结的条目，包括审核过未审核过     
    @classmethod     
    def query_normal_entry(cls):         
        q = cls.query         
        tablename = "public.%s" % cls.__tablename__           #
        #条件:存在&&审核通过&&未被冻结
        fc=['( %s.status & %d )::int = %d' % ( tablename, 1, 1 ),
            '( %s.status & %d )::int = %d' % ( tablename, 2, 2 ),
            '( %s.status & %d )::int != %d' % ( tablename, 4, 4)
            ]
        q = q.filter( db.text(cls._and(fc)) )         
        return q

    def __getstate__(self):
        ' used by pickle '
        state = {'id':self.id}
        return state

    def __setstate__(self, state):
        ' used by pickle '
        style = type(self).get(state['id'])
        self.__dict__.update(style.__dict__.copy())
