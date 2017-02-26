#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:jianwen

from flask import current_app
from flask.ext.login import current_user
from cm_web.app import create_app



def init_test_data():
    from cm_web.storage import db
    from cm_web.storage.data import *
    user = Admin('admin','chengmeiadmin')
    user.add_to_db()
    db.commit()

if __name__ == '__main__':
    app = create_app( test=True )
    with app.test_request_context():
        init_test_data()


