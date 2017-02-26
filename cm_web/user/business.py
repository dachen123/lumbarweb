# -*- coding: utf-8 -*-
"""
    编写服务器内部接口
    author : jianwen
    company: duoc
    date   : 2015.05
"""
from flask import g, current_app, session, jsonify,redirect,url_for
from flask.ext.login import UserMixin, current_user, logout_user
from flask.ext.login import login_user as flask_login_user
from flask.ext.login import LoginManager, login_required
from cm_web.storage import db
import requests
import datetime
import gevent


login_manager = LoginManager()



@login_manager.unauthorized_handler
def unauthorized():
    # return current_app.helper.ret_fail(u"请先登录再操作", 'E_NOT_LOGIN')
    return redirect(url_for('backend.web_ad_no_login'))

@login_manager.user_loader
def load_user(user_id):
    from cm_web.storage.data import Admin
    return Admin.query_valid_entry().filter_by(id=user_id).first()


def web_login(account, password):
    """
        用户登录
        输入phone, password进行登录
        返回user_info
    """
    # 获取用户uid
    from cm_web.storage.data import Admin
    user = Admin.query_valid_entry()\
            .filter(Admin.account_name==account).first()
    if not user:
        raise CMException(info=u'用户不存在',
                log_msg=u'用户不存在')
    if user.password != password:
        raise CMException(info=u'密码错误',
                log_msg=u'密码错误')
    session.permanent = True
    flask_login_user(user)

    #     return redirect(url_for('backend.web_ad_index'))
    # else:
    #     return redirect(url_for('backend.web_ad_no_login'))





def web_logout():
    """
        user logout
    """
    logout_user()

