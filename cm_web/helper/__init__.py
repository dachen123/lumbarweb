#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#  
#    Author: jianwen
#    Date:   2016-9-01
#
############################################################################

import time
import os
from datetime import datetime
import math
import json
import requests
from functools import wraps
from flask.ext.login import current_user
from flask import g, jsonify, current_app, make_response, request, session
from cm_web.config import load_config


#: 全局CMException类，无需导入，直接可用
class CMException(Exception):
    """ 参数列表可以传的默认处理的key有'ret_obj','info', 'dict_info'
        其中ret_obj可以将整个ret_common返回的dict对象放入CMException中，
        info和dict_info也是ret_common返回dict对象中的key，如果写在kwargs中
        处理函数会自动的把kwargs['info']和kwargs['dict_info']中的值merge到
        kwargs['ret_obj']中返回给用户，
        其他信息不返回给用户，只在日志中记录

        'info' : 返回给客户端的信息
        'log_msg' : 记录日志的信息
    """
    def __init__( self, info=None, log_msg=None, error_code='E_FAIL', 
            *args, **kwargs ):
        self.info = info
        self.log_msg = log_msg or info
        self.error_code=error_code
        self.args = args
        self.kwargs = kwargs
        super(CMException,self).__init__(*args)

class CMError(CMException):
    def __init__(self, *args, **kwargs):
        super(CMError, self).__init__(*args, **kwargs)

class CMHelper(object):

    def __init__(self, app=None):
        self.app = app
        self.machid = 0
        self.procid = os.getpid()        # 进程号 或 机器号 < 1024
        import __builtin__
        __builtin__.CMException = CMException
        __builtin__.CMError = CMError

    def init_app(self, app, machid=0):
        self.app = app
        self.machid = machid
        self.procid = os.getpid() & (2 ** 16 -1)

    _serialno = 0;
    _time_base = 2**32
    _proc_base = 2**10
    _proc_mask = 2**10 - 1

    _time_shift = 32
    _mach_shift = 26   # 2 ^^ 6 = 64台机器
    _proc_shift = 10

    _time_before = 1432360312 << 32 #2015-5-23下午的timestamp, 用于valiation
    def dcid(self):
        self._serialno = (self._serialno + 1) & self._proc_mask
        newid = (int(time.time()) << self._time_shift) \
                    | (self.machid << self._mach_shift) \
                    | (self.procid << self._proc_shift) \
                    | self._serialno
        return newid

    def is_valid_id(self, id):
        return id == 0xffffffffffffffff or ((id > self._time_before) and 
                (id < (int(math.ceil(time.time())) << self._time_shift)))

    def ret_common(self,  stat='OK', message=None,error_code='OK',**kwargs):
        ret_c = {   'error_code'      :   error_code, 
                    'timestamp'   :   int(time.time()) * 1000,}
        ret_result = {}
        ret_result.update(kwargs)
        ret_c.update({
            'result':ret_result
            })
        if message:
            ret_c.update({
                'message':message
                })
        return jsonify(ret_c)

    def ret_ok(self, **kwargs):
        # current_app.log(u'OK in request %s' \
        #         % (request.path) + self.log_user_string())
        return self.ret_common(**kwargs)

    def log_user_string(self):
        # if current_user.is_authenticated:
        #     return u' --user(nickname:%s,id:%s) --args:%s --form:%s' % \
        #             ( current_user.nickname,current_user.id,\
        #             json.dumps(request.args),json.dumps(request.form))
        # else:
        #     return u' --AnonymousUser --args:%s --form:%s' % (
        #             json.dumps(request.args),json.dumps(request.form))
        return ''


    def ret_fail(self, message=None, error_code='E_FAIL', **kwargs):
        if message is None:
            try:
                message = g.error_msg   #目前没有 g.error_msg 了
            except:
                message = u'外太空的错误'
                error_code = 'E_ERROR_FROM_OUTSPACE'
        current_app.log(u'FAIL in request %s %s : %s' \
                % (request.path,\
                    error_code, \
                    message) + self.log_user_string())
                
        return self.ret_common(stat='FAIL', 
                               message=message, 
                               error_code=error_code,
                               **kwargs)

    def ret_undo(self, **kwargs):
        return self.ret_common(stat='FAIL', message=u'该功能尚未上线',
                               error_code='E_NOT_SUPPORT')

    def is_android(self):
        '判断当前设备是否是Android'
        device_type = session.get('device_type')
        return 'android' == device_type

    def date_to_ts(self, date):
        if date is None:
            return None
        if isinstance(date, float) or isinstance(date, int):
            return date
        return int(time.mktime(date.timetuple()))

    def date_to_tsi(self, date):
        if date is None:
            return None
        if isinstance(date, float) or isinstance(date, int):
            return int(date)
        return int(time.mktime(date.timetuple()))

    def date_to_tms(self, date):
        if date is None:
            return None
        'datetime to milliseconds'
        if isinstance(date, float) or isinstance(date, int):
            return int(date*1000)
        return str(int(time.mktime(date.timetuple())*1000))

    def ts_to_date(self, timestamp):
        if isinstance(timestamp, datetime):
            return timestamp
        return datetime.fromtimestamp(timestamp)


    def _convert_char(self, ch):
        return rds_hanzi_dict.get(ch) or '~'

    def _convert_str(self, _str):
        try:
            _str = _str.decode('utf-8')
        except:
            pass
        return ''.join([self._convert_char(ch) for ch in _str])

    def weight(self, name):
        _length = 7
        _first_ch = name[0:1]
        if ord(_first_ch) > 0 and ord(_first_ch) < 127:
            _start_hanzi = 0.0
        else:
            _start_hanzi = 0.5
        _str = self._convert_str(name)
        _str = _str[0:_length].ljust(_length)
        _w = 0.0 + ord(_str[0:1]) + _start_hanzi
        for ch in _str[1:]:
            _w = _w * 127 + ord(ch)
        # print (name, _str, _w)
        return _w


def view_exception_wrapper(func):
    '对Flask的view进行包装，捕获异常写入日志，并返回错误信息'
    @wraps(func)
    def decorated_view(*args, **kwargs):
        func_name = func.func_name
        default_err = u'网络繁忙，请稍后重试'
        try:
            ret = func(*args, **kwargs)
            return current_app.db.commit() and ret # or ret_fail(err_msg)
        except CMError, e:
            err_msg = e.info or u'程序运行中出错'
            current_app.logger.error(err_msg)
            current_app.db.rollback()
            return current_app.helper.ret_fail(err_msg)
        except CMException, e:
            err_msg = e.info or e.message or default_err
            current_app.db.rollback()
            return current_app.helper.ret_fail(err_msg, e.error_code)
        except Exception, e:
            print e.message
            current_app.logger.exception(e.message)
            current_app.db.rollback()
            if current_app.config.get('MODE') == 'PRODUCTION':
                return current_app.helper.ret_fail('E_ERROR_FROM_MARS')
            else:
                return current_app.helper.ret_fail(u'来自火星的错误', 
                    'E_ERROR_FROM_MARS')
    return decorated_view

# 后台权限管理系统登录
def admin_required(func):
    @wrap(func)
    def check_authority(*args, **kwargs):
        func_name = func_name
        pass
    return check_authority

config = load_config()
def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin']  = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        rst.headers['Access-Control-Allow-Headers'] = \
                'Referer,Accept,Origin,User-Agent'
        return rst
    return config.get('TESTING', False) and wrapper_fun or fun
helper = CMHelper()


def admin_required(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):

        if current_user.is_authenticated and current_user.is_admin():
            pass
        elif current_user.is_authenticated and current_user.is_expert():
            pass
        else:
            raise CMException(u'只有管理员才可进行操作',
                    error_code = 'E_NOT_ADMIN')
        return fun(*args, **kwargs)
    return wrapper_fun




        
def http_result(r):
    error_log = {
                "method": r.request.method,
                "url": r.request.url,
                "request_header": dict(r.request.headers),
                "response_header": dict(r.headers),
                "response": r.text
            }
    if r.request.body:
        error_log["payload"] = r.request.body
    error_log_string =  json.dumps(error_log)
    print error_log_string
    current_app.logger.debug(error_log_string)

    if r.status_code == requests.codes.ok:
        return True, r.json()
    else:
        return False, r.text

#更新对象的域的函数
def update_field(obj, **kargs):
    if kargs is not None:
        for key,value in kargs.items():
            if getattr(obj, key) != value:
                setattr(obj, key, value)




#获取用户端ip
def get_request_ip():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0]
    else:
        ip = request.remote_addr
    return ip
