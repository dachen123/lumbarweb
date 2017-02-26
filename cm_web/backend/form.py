#!/usr/bin/env python
# -*- coding:utf-8 -*-

from wtforms import validators, ValidationError

from cm_web.form import CMForm, ListForm, ValidID, ValidImage, ValidVideo
from cm_web.form import (IntegerField, StringField, FormField, FieldList, 
                    BooleanField, FloatField)


class AddTeamMember(CMForm):
    light_avatar=StringField(u'light_avatar',validators=[
        validators.data_required(message=u'缺少头像亮图'),
        ValidImage()
        ])
    dark_avatar=StringField(u'dark_avatar',validators=[
        validators.optional()
        ])
    name=StringField(u'name',validators=[
        validators.data_required(message=u'u缺少名字')])
    description=StringField(u'description',validators=[
        validators.data_required(message=u'缺少描述')])

class UpdateTeamMember(AddTeamMember):
    tm_id=IntegerField(u'tm_id',validators=[
        validators.data_required(message=u'缺少成员id'),
        ValidID()])

class DeleteTeamMember(CMForm):
    tm_id=IntegerField(u'tm_id',validators=[
        validators.data_required(message=u'缺少成员id'),
        ValidID()])

class SetTeamTop(CMForm):
    tm_id=IntegerField(u'tm_id',validators=[
        validators.data_required(message=u'缺少成员id'),
        ValidID()])
    top = BooleanField(u'top',default=False)

class GetTeamMemberList(ListForm):
    pass

class GetTeamMemberMeta(CMForm):
    tm_id=IntegerField(u'tm_id',validators=[
        validators.data_required(message=u'缺少成员id'),
        ValidID()])

class AddInvestment(CMForm):
    company_name=StringField(u'company_name',validators=[
        validators.data_required(message=u'缺少公司名字')])
    cover_image=StringField(u'cover_image',validators=[
        validators.data_required(message=u'缺少封面图片'),
        ValidImage()])
    company_url=StringField(u'company_url',validators=[
        validators.data_required(message=u'缺少公司网址')])
    company_addr=StringField(u'company_addr',validators=[
        validators.data_required(message=u'缺少公司地址描述')
        ])
    pm_manager = StringField(u'pm_manager',validators=[
        validators.data_required(message=u'缺少项目负责人')
        ])
    company_introduce = StringField(u'company_introduce',validators=[
        validators.data_required(message=u'缺少公司描述')
        ])
    type_id = IntegerField(u'type_id',validators=[
        validators.data_required(message=u'缺少类型id')
        ])

class UpdateInvestment(AddInvestment):
    im_id = IntegerField(u'im_id',validators=[
        validators.data_required(message=u'缺少项目id')
        ])

class SetImTop(CMForm):
    im_id = IntegerField(u'im_id',validators=[
        validators.data_required(message=u'缺少项目id')
        ])
    top = BooleanField(u'top',default=False)


class DeleteInvestment(CMForm):
    im_id = IntegerField(u'im_id',validators=[
        validators.data_required(message=u'缺少项目id')
        ])

class GetInvestmentList(ListForm):
    pass

class GetInvestmentInfo(CMForm):
    im_id = IntegerField(u'im_id',validators=[
        validators.data_required(message=u'缺少项目id')
        ])

class AddNews(CMForm):
    title = StringField(u'title',validators=[
        validators.data_required(message=u'缺少标题')
        ])
    cover_image = StringField(u'cover_image',validators=[
        validators.data_required(message=u'缺少封面图片'),
        ValidImage()
        ])
    content = StringField(u'content',validators=[
        validators.data_required(message=u'缺少新闻内容')])
    type_id = IntegerField(u'type_id',validators=[
        validators.data_required(message=u'缺少类型id')
        ])

class UpdateNews(AddNews):
    news_id = IntegerField(u'news_id',validators=[
        validators.data_required(message=u'缺少新闻id')
        ])

class DeleteNews(CMForm):
    news_id = IntegerField(u'news_id',validators=[
        validators.data_required(message=u'缺少新闻id')
        ])

class SetNewsTop(CMForm):
    news_id = IntegerField(u'news_id',validators=[
        validators.data_required(message=u'缺少新闻id')
        ])
    top = BooleanField(u'top',default=False)

class GetNewsList(ListForm):
    pass

class GetNewsMeta(CMForm):
    news_id = IntegerField(u'news_id',validators=[
        validators.data_required(message=u'缺少新闻id')
        ])

class AddAddr(CMForm):
    city = StringField(u'city',validators=[
        validators.data_required(message=u'缺少城市名称')])
    cover_image = StringField(u'cover_image',validators=[
        validators.data_required(message=u'缺少封面图片'),
        ValidImage()
        ])
    detail_addr = StringField(u'detail_addr',validators=[
        validators.data_required(message=u'缺少详细地址')])
    phone = StringField(u'phone',validators=[
        validators.data_required(message=u'缺少手机号码')
        ])
    mail = StringField(u'mail',validators=[
        validators.data_required(message=u'缺少邮箱')])
    fax_no = StringField(u'fax_no',validators=[
        validators.data_required(message=u'缺少传真号码')
        ])
    baidu_share = StringField(u'baidu_share',validators=[
        validators.data_required(message=u'缺少百度分享链接')
        ])

class UpdateAddr(AddAddr):
    addr_id = IntegerField(u'addr_id',validators=[
        validators.data_required(message=u'缺少地址记录id')
        ])

class DeleteAddr(CMForm):
    addr_id = IntegerField(u'addr_id',validators=[
        validators.data_required(message=u'缺少地址记录id')
        ])

class GetAddrList(ListForm):
    pass

class GetAddrMeta(CMForm):
    addr_id = IntegerField(u'addr_id',validators=[
        validators.data_required(message=u'缺少地址记录id')
        ])

class AddNewsType(CMForm):
    type_name = StringField(u'type_name',validators=[
        validators.data_required(message=u'缺少类型名称')])
    description = StringField(u'description',validators=[
        validators.optional()])

class UpdateNewsType(AddNewsType):
    type_id = IntegerField(u'type_id',validators=[
        validators.data_required(message=u'缺少类型id')])

class DeleteNewsType(CMForm):
    type_id = IntegerField(u'type_id',validators=[
        validators.data_required(message=u'缺少类型id')])

class AddInvestmentType(CMForm):
    type_name = StringField(u'type_name',validators=[
        validators.data_required(message=u'缺少类型名称')])
    description = StringField(u'description',validators=[
        validators.optional()])

class UpdateInvestmentType(AddInvestmentType):
    type_id = IntegerField(u'type_id',validators=[
        validators.data_required(message=u'缺少类型id')])

class DeleteInvestmentType(CMForm):
    type_id = IntegerField(u'type_id',validators=[
        validators.data_required(message=u'缺少类型id')])


class AddImage(CMForm):
    image = StringField(u'image',validators=[
        validators.data_required(message=u'缺少图片')
        ])
    title = StringField(u'title',validators=[
        validators.data_required(message=u'缺少标题')
        ])
    content = StringField(u'content',validators=[
        validators.data_required(message=u'缺少标题')
        ])

class UpdateImage(AddImage):
    image_id = IntegerField(u'image_id',validators=[
        validators.data_required(message=u'缺少图片id')])

class DeleteImage(CMForm):
    image_id = IntegerField(u'image_id',validators=[
        validators.data_required(message=u'缺少图片id')])

class AddTab(CMForm):
    bg_image = StringField(u'bg_image',validators=[
        validators.data_required(message=u'缺少背景图片')
        ])
    title= StringField(u'title',validators=[
        validators.data_required(message=u'缺少标题') 
        ])
    slogan = StringField(u'slogan',validators=[
        validators.data_required(message=u'缺少标语')
        ])

class UpdateTab(AddTab):
    tab_id = IntegerField(u'tab_id',validators=[
        validators.data_required(message='缺少tab栏id')
        ])

class DeleteTab(CMForm):
    tab_id = IntegerField(u'tab_id',validators=[
        validators.data_required(message='缺少tab栏id')
        ])

class SetTabTop(CMForm):
    tab_id=IntegerField(u'tab_id',validators=[
        validators.data_required(message=u'缺少tab id'),
        ValidID()])
    top = BooleanField(u'top',default=False)
