#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask.ext.redis import Redis

class CMRedis(Redis):
    def init_app(self, app):
        self.app = app
        super(CMRedis, self).init_app(app)

redis = CMRedis()


