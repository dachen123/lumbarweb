# -*- coding: utf-8 -*-
#################################################################
#
#           author:zhengwei
#           2015-6-1
#
#################################################################

from wtforms import IntegerField, StringField, PasswordField, FieldList,DateField 
from wtforms import validators

from cm_web.form import CMForm

class LoginForm(CMForm):
    account = StringField(u'account',validators=[ 
        validators.data_required(message=u'缺少用户名')])
    password = PasswordField(u'password',validators=[ 
        validators.data_required(message=u'缺少密码') ])
    
