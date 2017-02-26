# -*- coding: utf-8 -*-

import json
import os

from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
from cm_web.config.test_config import Config
from flask import current_app
import re

import oss2


# 以下代码展示了STS的用法，包括角色扮演获取临时用户的密钥、使用临时用户的密钥访问OSS。

# STS入门教程请参看  https://yq.aliyun.com/articles/57895
# STS的官方文档请参看  https://help.aliyun.com/document_detail/28627.html

# 首先初始化AccessKeyId、AccessKeySecret、Endpoint等信息。
# 通过环境变量获取，或者把诸如“<你的AccessKeyId>”替换成真实的AccessKeyId等。
# 注意：AccessKeyId、AccessKeySecret为子用户的密钥。
# RoleArn可以在控制台的“访问控制  > 角色管理  > 管理  > 基本信息  > Arn”上查看。
#
# 以杭州区域为例，Endpoint可以是：
#   http://oss-cn-hangzhou.aliyuncs.com
#   https://oss-cn-hangzhou.aliyuncs.com
# 分别以HTTP、HTTPS协议访问。
# access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', '<你的AccessKeyId>')
# access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', '<你的AccessKeySecret>')
# bucket_name = os.getenv('OSS_TEST_BUCKET', '<你的Bucket>')
# endpoint = os.getenv('OSS_TEST_ENDPOINT', '<你的访问域名>')
# sts_role_arn = os.getenv('OSS_STS_ARN', '<你的Role Arn>')




class StsToken(object):
    """AssumeRole返回的临时用户密钥
    :param str access_key_id: 临时用户的access key id
    :param str access_key_secret: 临时用户的access key secret
    :param int expiration: 过期时间，UNIX时间，自1970年1月1日UTC零点的秒数
    :param str security_token: 临时用户Token
    :param str request_id: 请求ID
    """
    def __init__(self):
        self.access_key_id = ''
        self.access_key_secret = ''
        self.expiration = 0
        self.security_token = ''
        self.request_id = ''



class OSS2(object):

    def __init__(self,app=None):
        if app is not None:
            self.init_app(app)


    def init_app(self,app):
        self.token = None
        self.access_key_id = app.config.get('OSS_ACCESS_KEY_ID', '<你的AccessKeyId>')
        self.access_key_secret = app.config.get('OSS_ACCESS_KEY_SECRET', '<你的AccessKeySecret>')
        self.bucket_name = app.config.get('OSS_BUCKET', '<你的Bucket>')
        self.endpoint = app.config.get('OSS_ENDPOINT', '<你的访问域名>')
        self.sts_role_arn = app.config.get('OSS_STS_ARN', '<你的Role Arn>')
        self.addr_prefix = u'http://'+self.bucket_name+'.'+self.endpoint

    def assert_param(self):
        # 确认上面的参数都填写正确了
        for param in (
                self.access_key_id, 
                self.access_key_secret, 
                self.bucket_name, 
                self.endpoint, 
                self.sts_role_arn):
            assert '<' not in param, '请设置参数：' + param

    def fetch_sts_token(self):
        """子用户角色扮演获取临时用户的密钥
        :param access_key_id: 子用户的 access key id
        :param access_key_secret: 子用户的 access key secret
        :param role_arn: STS角色的Arn
        :return StsToken: 临时用户密钥
        """
        self.assert_param()
        clt = client.AcsClient(self.access_key_id, self.access_key_secret, 'cn-beijing')
        req = AssumeRoleRequest.AssumeRoleRequest()
    
        req.set_accept_format('json')
        req.set_RoleArn(self.sts_role_arn)
        req.set_RoleSessionName('cm-web-upload')
        req.set_DurationSeconds(900)
    
        body = clt.do_action(req)
    
        j = json.loads(body)
    
        self.token = StsToken()
    
        self.token.access_key_id = j['Credentials']['AccessKeyId']
        self.token.access_key_secret = j['Credentials']['AccessKeySecret']
        self.token.security_token = j['Credentials']['SecurityToken']
        self.token.request_id = j['RequestId']
        self.token.expiration = oss2.utils.to_unixtime(j['Credentials']['Expiration'], '%Y-%m-%dT%H:%M:%SZ')
        return self.token.access_key_id,self.token.access_key_secret,self.token.security_token

    def strip_url_suffix(self, url):
        '如果是阿里云上的图片，去除规格参数'
        regex = '^(http://' + self.bucket_name + '.oss-\w{2}-\w{4,}\D*\d*.aliyuncs.com)?/[^!\s]+'
        m = re.match(regex, url)
        return m and m.group() or url

    def strip_url_prefix(self, url):
        '如果是阿里云上的图片，去除前缀http://bucket.region.aliyuncs.com'
        regex = '^http://' + self.bucket_name + '.oss-\w{2}-\w{4,}\D*\d*.aliyuncs.com/.*'
        m = re.match(regex, url)
        if m is None:
            return url
        index = url.find('aliyuncs.com')
        return url[index+12:]
    
    def original(self, image_url):
        '原图, 传进来的阿里云云的url都是预处理后的不带前后缀的url'
        if not image_url:
            return ''
        if re.match('^http://.+', image_url):
            return image_url
        return self.addr_prefix + self.strip_url_suffix(image_url)

    
    def oss_upload_image(self,file):
        self.fetch_sts_token()

        auth = oss2.StsAuth(self.token.access_key_id, self.token.access_key_secret, self.token.security_token)
        bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
        key = u'image/news/'+str(current_app.helper.dcid())+'.png'
        ret = bucket.put_object(key, file)
        if ret.status == 200:
            return current_app.oss.original('/'+key)

# oss = OSS2()
    

# # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
# token = fetch_sts_token(access_key_id, access_key_secret, sts_role_arn)
# auth = oss2.StsAuth(token.access_key_id, token.access_key_secret, token.security_token)
# bucket = oss2.Bucket(auth, endpoint, bucket_name)
#
#
# # 上传一段字符串。Object名是motto.txt，内容是一段名言。
# bucket.put_object('motto.txt', 'Never give up. - Jack Ma')
#
#
# # 下载到本地文件
# bucket.get_object_to_file('motto.txt', '本地座右铭.txt')
#
#
# # 删除名为motto.txt的Object
# bucket.delete_object('motto.txt')
#
#
# # 清除本地文件
# os.remove(u'本地座右铭.txt')
#
