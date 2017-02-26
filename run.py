#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent.pywsgi import WSGIServer
from cm_web.app import create_app
from cm_web.storage import db

app = create_app(name='LUMBARV2_WEB')



if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0',port=7777,debug=True)

