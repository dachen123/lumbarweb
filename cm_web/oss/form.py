#!/usr/bin/env python
# -*- coding:utf-8 -*-

from wtforms import validators, ValidationError

from cm_web.form import CMForm, ListForm, ValidID, ValidImage, ValidVideo
from cm_web.form import (IntegerField, StringField, FormField, FieldList, 
                    BooleanField, FloatField)

class GetOssStsToken(CMForm):
    pic_type = StringField(u'pic_type',validators=[
        validators.data_required(message=u'u缺少图片分类'),
        validators.any_of(['index','team','investment','news','addr','about'])
        ])
