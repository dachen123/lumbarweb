# -*- coding: utf-8 -*-
#################################################################
#
#           author:jianwen
#           2016-1-09
#
#################################################################



from flask import Blueprint, g, session, request, current_app, redirect
bp = Blueprint('user', __name__)
from .business import web_login,web_logout
from .form import LoginForm
from cm_web.helper import view_exception_wrapper, allow_cross_domain
from cm_web.form import validate_form
from flask.ext.login import login_required, current_user
from datetime import datetime




@bp.route("/login", methods=["POST"])
@view_exception_wrapper
@validate_form(LoginForm)
def api_web_login():
    """
    """
    web_login(account=g.form.account.data,
            password=g.form.password.data)
    return current_app.helper.ret_ok()

    

@bp.route("/logout", methods=["POST"])
@view_exception_wrapper
def api_logout():
    """
        用户登出
        in: Nothing
    """
    web_logout()
    return current_app.helper.ret_ok()

