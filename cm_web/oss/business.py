#!/usr/bin/env python
# -*- coding:utf-8 -*-

# from cm_web.oss.oss import oss
from flask import current_app
from cm_web.helper import helper

def get_oss_sts_token(pic_type):

    upload_key = u'image/'+pic_type+u'/'+str(helper.dcid())+u'.png'
    access_key_id,access_key_secret,security_token = current_app.oss.fetch_sts_token() 
    ret_dict = {
        'upload_key': upload_key,
        'access_key_id':access_key_id,
        'access_key_secret':access_key_secret,
        'security_token':security_token
            }
    return ret_dict

def oss_upload_image(file):
    current_app.oss.oss_upload_image(file)

