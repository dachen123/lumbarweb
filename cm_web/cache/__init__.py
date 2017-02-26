#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:   waterpku
# company:  duoc
# date:     April, 2015

"""
    使用Flask-Cache提供的cache功能，已配置到redis://duoc:bingo@localhost/1
    使用方法如下：
    app = Flask(__name__)
    config = load_config()
    app.config.from_config(config) #一定要先设置config
    cache = Cache(app)

    使用的时候注意：
        对于flask的view，使用@cache.cached()
        对于其他函数，一律使用@cache.memoize()，如要使用cached，则须指定key名，
            人工保证不重名，如下所示：
                @cache.cached(key_prefix='uniq_cache_key_name')
            否则，所有未指定key_prefix的cached key都会使用同一个名字'flask_cache_view//'


    所有被cache的函数，在第一次被cache的时候设置了expire time，以后再命中不会自动延长
    expire time, 即使一直使用的函数，每5分钟都会被清掉cache重新计算。如果要每次访问自
    动延长超时时间，需在werkzeug/contrib/cache中（而不是Flask-Cache模块）作相应的修改，
    亦即在cache.get时加入延时操作
"""

from flask.ext.cache import Cache

cache = Cache()

__all__ = [ "cache" ]
