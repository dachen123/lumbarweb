#!/usr/bin/env python
# -*- coding:utf-8 -*-

import multiprocessing, os
#bind = "unix:/tmp/gunicorn_duoc.sock"
bind = "0.0.0.0:7777"
workers = multiprocessing.cpu_count() * 2 + 1
#workers = 4

#worker_class = 'egg:gunicorn#gevent'
worker_class = 'gevent'
#worker_class = 'gevent'
#worker_class = 'sync'

worker_connections = 40960
backlog = 2048

max_request = 100000

timeout = 30
graceful_timeout = 30
keepalive = 65

limit_request_line = 4090
limit_request_fields = 100
limit_request_file_size = 8190

daemon = True

debug=False

pidfile = '/var/run/lumbarv2_web/gunicorn/gunicorn_lumbarv2_web.pid'
user = 'lumbarv2'
group = 'lumbarv2'

x_forwarded_for_header = 'X-FORWARDED-FOR'

accesslog = '/var/log/lumbarv2_web/gunicorn/access'
errorlog = '/var/log/lumbarv2_web/gunicorn/error'
loglevel = 'debug'

proc_name = 'gunicorn_lumbarv2_web'

pythonpath = os.getenv('PYTHONPATH')
import sys
sys.path.insert(0, pythonpath)

os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs'

