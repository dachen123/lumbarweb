#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#  
#    Author: jianwen
#    Date:   2016-1-09
#
############################################################################
#if 'threading' in sys.modules:
#    raise Exception('threading module loaded before patching!')
from gevent import monkey
monkey.patch_all()

from flask import Flask 
from werkzeug.utils import import_string

from cm_web.config import load_config
from cm_web.user.libs import RedisSessionInterface
from psycogreen.gevent import patch_psycopg; patch_psycopg()

extensions = [
        'cm_web.storage:db',
        'cm_web.redis:redis',
        'cm_web.cache:cache',
        'cm_web.log:log',
        'cm_web.helper:helper',
        'cm_web.oss:oss',
        'cm_web.user:login_manager',
]

blueprints = [
        'cm_web.frontend:frontend_bp',
        'cm_web.backend:backend_bp',
        'cm_web.oss:oss_bp',
        'cm_web.user:user_bp',
]

def create_app(name=None, config=None, test=False, extensions=extensions, 
        blueprints=blueprints):

    import sys
    reload(sys)

    sys.setdefaultencoding('utf-8')
    if name and not isinstance(name, basestring):
        name = None
    name = name or 'CMCT'

    baseconfig = load_config(test)
    app = Flask(name or __name__)
    app.config.from_object(baseconfig)
    #config jinjia
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    # set the session interface to user Redis session
    app.session_interface = RedisSessionInterface()
    if config is not None:
        app.config.update(config)

    for ext_name in extensions:
        print 'ext_name: ' + ext_name 
        ext = import_string(ext_name)
        ext.init_app(app)
        symbol = ext_name.split(':')[-1]
        if hasattr(app, symbol):
            print "app hasattr %s" % symbol
        else:
            setattr(app, symbol, ext)
    for bp_name in blueprints:
        #print bp_name
        bp = import_string(bp_name)
        app.register_blueprint(bp)



    return app

    
