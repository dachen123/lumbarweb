#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Config( object ):
    """
    postgres config
    """

    LOGIN_DISABLED     = False
    #TESTING     = True
    DEBUG       = True
    MODE        = 'PRODUCTION'
    ADMINS      = [ 'bingo.liang@duoc.cn']
    """
    postgres config
    """
    SQLALCHEMY_DATABASE_URI = \
            "postgresql+psycopg2://cmweb:chengmei123@localhost:5432/cm_db"
    SQLALCHEMY_BINDS            = None
    SQLALCHEMY_NATIVE_UNICODE   = None
    SQLALCHEMY_ECHO             = False  # for debug
    SQLALCHEMY_RECORD_QUERIES   = None
    SQLALCHEMY_POOL_SIZE        = None
    SQLALCHEMY_POOL_TIMEOUT     = None
    SQLALCHEMY_POOL_RECYCLE     = None
    SQLALCHEMY_MAX_OVERFLOW     = None
    SQLALCHEMY_COMMIT_ON_TEARDOWN   = False
    SQLALCHEMY_TRACK_MODIFICATIONS  = True

    ##########################
    #      cache module      #
    ##########################

    CACHE_TYPE              = 'redis'
    CACHE_DEFAULT_TIMEOUT   = 300           # as default
    CACHE_THRESHOLD         = 500           # as default
    CACHE_REDIS_HOST        = '127.0.0.1'
    CACHE_REDIS_PORT        = 6379          # as default
    CACHE_REDIS_PASSWORD    = 'chengmei123'
    CACHE_REDIS_DB          = 5             # as default
    CACHE_REDIS_URL         = 'redis://:chengmei123@localhost:6379/5'

    ##########################
    #      redis module      #
    ##########################

#    REDIS_DATABASE          = 0             # deprecated
    REDIS_URL               = 'redis://:chengmei123@localhost:6379/6'
    REDIS_PORT        = 6379          # as default
    REDIS_PASSWORD    = 'chengmei123'
    REDIS_DB          = 6             # as default


    ##########################
    #      oss   module      #
    ##########################

    OSS_ACCESS_KEY_ID = 'LTAIL9EC5hL3UxBX'
    OSS_ACCESS_KEY_SECRET = 'hbvaVqODecyRJMCXd3VqxWSn4eoKtd'
    OSS_BUCKET = 'chengmeitest'
    OSS_ENDPOINT = 'oss-cn-beijing.aliyuncs.com'
    OSS_STS_ARN = 'acs:ram::1591554417377702:role/chengmeitestwrite'


    ##########################
    #        log module      #
    ##########################

    #nanomsg devices
    LOGGER_NAME       = 'test'
    NN_DEVICE_DICT = {
            'lumbarv2'     : 'ipc:///var/lib/dc_log/nano.lumbarv2',
            'lumbarv2_test'     : 'ipc:///var/lib/dc_log/nano.lumbarv2_test',
            'test'      : 'ipc:///var/lib/dc_log/nano.test',
            'push'      : 'ipc:///var/lib/dc_log/nano.push',
            'attach'    : 'ipc:///var/lib/dc_log/nano.attach',
            'unittest'  : 'ipc:///var/lib/dc_log/nano.unittest',
            }
    LOG_DIR     = '/var/log/lumbarv2/'
    LOG_BACKUP_DIR = '/var/log/lumbarv2/'
    LOG_PID     = '/var/run/lumbarv2/lumbarv2_log_server.pid'
    PUSH_PID    = '/var/run/lumbarv2/push_worker.pid'



    @classmethod
    def get(cls, key, default=None):
        if hasattr(cls, key):
            return getattr(cls, key)
        else:
            return default

