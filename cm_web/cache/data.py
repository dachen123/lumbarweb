#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#  
#    Author: waterpku
#    Date:   2015-4-18
#    弃用
# 
############################################################################

from functools import wraps

from flask.ext.cache import Cache
from flask.ext.cache import function_namespace


class CMCache(Cache):
    """
    Cache策略：
    1. cache.cached:适用纯静态的（没有参数和环境）的函数或view函数
    2. cache.memoize:适用需要将参数包含在key中的cache
    """
    def __init__(self, app=None, with_jinja2=True, config=None):
        super(DuocCache, self).__init__(app, with_jinja2_ext, config)

    def init_app(self, app):
        super(DuocCache, self).init_app(app)

    def _log(self, *args, **kwargs):
        if self.app is not None:
            self.app.log(*args, **kwargs)

    def cached(self, timeout=None, key_prefix='view/%s', unless=None):
        return super(DuocCache, self).cached(timeout, key_prefix, unless)


    
