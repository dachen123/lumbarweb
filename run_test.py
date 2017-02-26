#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cm_web.app import create_app


if __name__ == '__main__':
    app = create_app(test=True)
    app.run(host='0.0.0.0',port=7777,debug=True)

