#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import current_app, g, jsonify, request, render_template
from cm_web.helper import view_exception_wrapper
from cm_web.form import validate_form
from cm_web.frontend.form import  *
from flask import Blueprint,request

from cm_web.storage.data import TeamMember
from flask.ext.login import login_required, current_user
from cm_web.backend.business import TeamManager,ImManager,\
        NewsManager,ContactAddrManager,NewsTypeManager,\
        InvestmentTypeManager,Carousel,AbManager
tm = TeamManager()
im = ImManager()
nm = NewsManager()
am = ContactAddrManager()
ntm = NewsTypeManager()
itm = InvestmentTypeManager()
cl = Carousel()
abm = AbManager()
from cm_web.frontend.business import (
        get_members_for_page,
        get_investment_list,
        get_news_by_type,
        get_im_list_by_type,
        get_addr_list)


bp = Blueprint('frontend', __name__, template_folder='templates',
        static_folder='static',static_url_path='/static/fe')

@bp.route("/",methods = ["GET"])
@bp.route("/index",methods = ["GET"])
def web_index():
    all_list = cl.get_image_list()
    if len(all_list) >= 5:
        cl_list = all_list[0:3]
        pic1 = all_list[3]
        pic2 = all_list[4]
    elif len(all_list) == 4:
        cl_list = all_list[0:3]
        pic1 = all_list[3]
        pic2 = None
    else:
        cl_list = all_list
        pic1 = None
        pic2 = None


    # member_list = tm.get_top_team()
    im_list = im.get_top_im()
    tab_list = abm.get_top_tab()
    news_list = nm.get_top_news()
    return render_template('index.html',
            cl_list=cl_list,
            im_list=im_list,
            tab_list=tab_list,
            news_list=news_list,
            pic1=pic1,
            pic2=pic2)

@bp.route("/about_us",methods = ["GET"])
def web_about_us():
    tab_list = abm.get_tab_list()
    return render_template('about_us.html',tab_list=tab_list)

@bp.route("/contact_us",methods = ["GET"])
def web_contact_us():
    addr_list = get_addr_list()
    return render_template('cm_contact.html',
            addr_list=addr_list)


@bp.route("/investment",methods = ["GET"])
def web_investment():
    type_list = itm.get_im_type_list()
    im_list = get_im_list_by_type('all',1,20)
    return render_template('investment.html',
            type_list=type_list,
            im_list=im_list)

@bp.route("/news",methods = ["GET"])
def web_news():
    news_type = ntm.get_news_type_list()
    news_list = get_news_by_type('all',1,20)
    return render_template('news.html',
            news_type=news_type,
            news_list=news_list
            )

@bp.route("/team",methods = ["GET"])
def web_team():
    base_page,tm_meta_list = get_members_for_page()
    return render_template('team.html',
            base_page=base_page,
            tm_list=tm_meta_list)

@bp.route("/get_im_list_by_type",methods = ["GET"])
@view_exception_wrapper
@validate_form(GetImListByType)
def api_get_im_list_by_type():
    im_list = get_im_list_by_type(
            type_id=g.form.type_id.data,
            start_index=g.form.start_index.data,
            count=g.form.count.data)
    return current_app.helper.ret_ok(im_list=im_list)

@bp.route("/get_news_list_by_type",methods = ["GET"])
@view_exception_wrapper
@validate_form(GetNewsListByType)
def api_get_news_list_by_type():
    news_list = get_news_by_type(
            type_id=g.form.type_id.data,
            start_index=g.form.start_index.data,
            count=g.form.count.data)
    return current_app.helper.ret_ok(news_list=news_list)
