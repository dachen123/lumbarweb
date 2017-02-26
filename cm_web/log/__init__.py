#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:   waterpku
# company:  duoc
# date:     May, 15, 2015

__all__ = [ "log_server", "dclogging", "add_log_handler", "log" ]
import os
from .dclogging import add_log_handler
import json

class DuocLog(object):
    """
    duoc log 对象
    """

    def __init__(self):
        pass

    def init_app(self, app):
        self.app = app
        add_log_handler(app, app.logger_name)
        self.method = {
                'INFO'      : self.app.logger.info,
                'DEBUG'     : self.app.logger.debug,
                'WARNING'   : self.app.logger.warning,
                'ERROR'     : self.app.logger.error,
                'CRITICAL'  : self.app.logger.critical,
                'EXCEPTION' : self.app.logger.exception,
        }

        # 这里启动log_server，这里使用restart是因为对于多进程的情况下，后起的进程需要
        # 重新启动log_server连接nano socket
        server_dir = self.app.config.get('SRC_DIRECTORY', '..')

        if self.app.config.get('MODE') == 'UNITTEST':
            os.system(server_dir+'/duoc/script/duoclogging.sh start_utest')
        elif self.app.config.get('MODE') == 'TESTING':
            os.system(server_dir+'/duoc/script/duoclogging.sh start_testing')
        #else:
        #    os.system(server_dir+'/duoc/script/duoclogging.sh start')

    def __call__(self, msg='', level='INFO', *args, **kwargs):
        try:
            message = (msg % args)
        except:
            message = msg
            for a in args:
                message = message + repr(a)
        if args or kwargs:
            data = dict(message=message, args=args, kwargs=kwargs)
            message = json.dumps(data, encoding='utf-8', ensure_ascii=False)
        if not self.method.has_key(level):
            level = 'INFO'
        self.method[level](message)

log = DuocLog()
