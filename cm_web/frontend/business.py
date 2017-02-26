#!/usr/bin/env python # -*- coding:utf-8 -*-

from flask.ext.login import current_user
from cm_web.storage import db
from cm_web.storage.data import *


def get_members_for_page():
    team_list = TeamMember.query_valid_entry()\
                .order_by(TeamMember.update_time.desc()).all()
    length = len(team_list)
    base_page = length / 21 #一页21个
    if (length - base_page * 21 ) > 0:
        base_page += 1
    tm_meta_list = []
    for t in team_list:
        tm_meta_list.append(t.tm_meta)
    return base_page,tm_meta_list


def get_im_list_by_type(type_id,start_index,count):
    start = start_index - 1
    if count < 0:
        count = 100
    stop = start + count
    if type_id == 'all':
        im_list = Investment.query_valid_entry()\
                .order_by(Investment.update_time.desc()).all()
    else:
        im_type = InvestmentType.get(type_id)

        # im_list = im_type.investments[start:stop]
        im_list=Investment.query.from_statement(db.text(
            'select a.* from investment as a join investment_investment_type as b on a.id=b.im_id '
            'where (a.status & 1)::int = 1 and b.type_id =:type_id')).params(type_id=im_type.id).all()

    im_info_list = []
    for t in im_list:
        im_info_list.append(t.im_info)
    return im_info_list 


def get_news_by_type(type_id,start_index,count):
    start = start_index - 1
    if count < 0:
        count = 100
    stop = start + count
    if type_id == 'all':
        news_list = News.query_valid_entry()\
                .order_by(News.update_time.desc()).all()
    else:
        news_type = NewsType.get(type_id)
        news_list=News.query.from_statement(db.text(
            'select a.* from news as a join news_news_type as b on a.id=b.news_id '
            'where (a.status & 1)::int = 1 and b.type_id =:type_id')).params(type_id=news_type.id).all()

        # news_list = news_type.news[start:stop]
    news_meta_list = []
    for n in news_list:
        news_meta_list.append(n.news_meta)
    return news_meta_list 
    
def get_investment_list(self,start_index,count):
    
    start = start_index - 1
    count = 0
    if count < 0:
        count = 100
    stop = start + count
    im_list = Investment.query_valid_entry()\
            .order_by(Investment.update_time.desc())[start:stop]
    im_info_list=[]
    for i in im_list:
        im_info_list.append(i.im_info)

    return im_info_list

def get_addr_list():
    addr_list = ContactAddr.query_valid_entry()\
            .order_by(ContactAddr.update_time.desc()).all()
    addr_meta_list = []
    for a in addr_list:
        addr_meta_list.append(a.contact_addr)
    return addr_meta_list

