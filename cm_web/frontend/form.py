#!/usr/bin/env python
# -*- coding:utf-8 -*-

from wtforms import validators, ValidationError

from cm_web.form import CMForm, ListForm, ValidID, ValidImage, ValidVideo
from cm_web.form import (IntegerField, StringField, FormField, FieldList, 
                    BooleanField, FloatField)

class GetImListByType(ListForm):
    type_id = StringField(u'type_id',validators=[
        validators.data_required(message=u'缺少类型id')
        ])

class GetNewsListByType(ListForm):
    type_id = StringField(u'type_id',validators=[
        validators.data_required(message=u'缺少类型id')
        ])


class GetInvestmentList(ListForm):
    pass
