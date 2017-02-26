#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import current_app, g, jsonify, request, render_template,Response 
bp = Blueprint('oss', __name__, template_folder='templates')

from cm_web.oss.business import get_oss_sts_token
from cm_web.helper import view_exception_wrapper
from cm_web.form import validate_form
from cm_web.oss.form import GetOssStsToken

@bp.route("/get_oss_token",methods = ["GET"])
@view_exception_wrapper
@validate_form(GetOssStsToken)
def api_get_oss_token():
    ret = get_oss_sts_token(
            pic_type=g.form.pic_type.data)
    return current_app.helper.ret_ok(
            access_key_id=ret['access_key_id'],
            access_key_secret=ret['access_key_secret'],
            security_token=ret['security_token'],
            upload_key=ret['upload_key'])

@bp.route("/image_upload",methods = ["POST"])
@view_exception_wrapper
def api_image_upload():
    file = request.files['wangEditorH5File']
    if file == None:
        result = r"error|未成功获取文件，上传失败"
        res =  Response(result)
        res.headers["ContentType"] = "text/html"
        res.headers["Charset"] = "utf-8"
        return res
    else:
        # if file and allowed_file(file.filename):
        if file :
            # filename = file.filename
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # imgUrl = "http://chengmeitest.oss-cn-beijing.aliyuncs.com/testtest.png"
            # oss_upload_image(file)
            imgUrl = current_app.oss.oss_upload_image(file)
            res =  Response(imgUrl)
            res.headers["ContentType"] = "text/html"
            res.headers["Charset"] = "utf-8"
            return res
