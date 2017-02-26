#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import current_app, g, jsonify, request, render_template
from flask import Blueprint,request
from flask.ext.login import login_required, current_user
from cm_web.backend.form import *
from cm_web.helper import view_exception_wrapper
from cm_web.form import validate_form
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

bp = Blueprint('backend', __name__, template_folder='templates',
        static_folder='static',static_url_path='/static/be')

@bp.route("/ad_addr",methods = ["GET"])
@login_required
def web_ad_addr():
    return render_template('ad_addr.html')


@bp.route("/ad_index",methods = ["GET"])
@login_required
def web_ad_index():
    return render_template('ad_index.html')

@bp.route("/ad_investment_pm",methods = ["GET"])
@login_required
def web_ad_investment_pm():
    im_type_list = itm.get_im_type_list()
    return render_template('ad_investment_pm.html',im_type_list=im_type_list)

@bp.route("/ad_investment_type",methods = ["GET"])
@login_required
def web_ad_investment_typ():
    return render_template('ad_investment_type.html')

@bp.route("/ad_news",methods = ["GET"])
@login_required
def web_ad_news():
    return render_template('ad_news.html')

@bp.route("/ad_team",methods = ["GET"])
@login_required
@login_required
def web_ad_team():
    return render_template('ad_team.html')

@bp.route("/ad_redirct",methods = ["GET"])
def web_ad_no_login():
    return render_template('redirect_login.html')

@bp.route("/ad_about",methods = ["GET"])
@login_required
@login_required
def web_ad_about():
    return render_template('ad_about.html')

@bp.route("/editor",methods = ["GET"])
@login_required
def web_editor():
    news_type_list = ntm.get_news_type_list()
    return render_template('editor.html',news_type_list=news_type_list)


@bp.route("/update_news",methods = ["GET"])
@login_required
def web_update_news():
    news_type_list = ntm.get_news_type_list()
    return render_template('update_news.html',news_type_list=news_type_list)


@bp.route("/admin",methods = ["GET"])
def web_admin_login():
    return render_template('login.html')

@bp.route("/add_team_member",methods=["POST"])
@view_exception_wrapper
@validate_form(AddTeamMember)
@login_required
def api_add_team_member():
    tm_id = tm.add_team_member(g.form)
    return current_app.helper.ret_ok(tm_id=tm_id)

@bp.route("/update_team_member",methods=["POST"])
@view_exception_wrapper
@validate_form(UpdateTeamMember)
@login_required
def api_update_team_member():
    tm.update_team_member(g.form)
    return current_app.helper.ret_ok()

@bp.route("/delete_team_member",methods=["POST"])
@view_exception_wrapper
@validate_form(DeleteTeamMember)
@login_required
def api_delete_team_member():
    tm.delete_team_member(g.form)
    return current_app.helper.ret_ok()

@bp.route("/get_team_member_list",methods=["GET"])
@view_exception_wrapper
@validate_form(GetTeamMemberList)
@login_required
def api_get_team_member_list():
    tm_meta_list = tm.get_team_member_list(g.form)
    return current_app.helper.ret_ok(tm_meta_list=tm_meta_list)

@bp.route("/get_team_member_meta",methods=["GET"])
@view_exception_wrapper
@validate_form(GetTeamMemberMeta)
@login_required
def api_get_team_member_meta():
    tm_meta = tm.get_team_member_meta(g.form)
    return current_app.helper.ret_ok(tm_meta=tm_meta)

@bp.route("/add_investment",methods=["POST"])
@view_exception_wrapper
@validate_form(AddInvestment)
@login_required
def api_add_investment():
    im_id = im.add_investment(g.form)
    return current_app.helper.ret_ok(im_id=im_id)

@bp.route("/update_investment",methods=["POST"])
@view_exception_wrapper
@validate_form(UpdateInvestment)
@login_required
def api_update_investment():
    im.update_investment(g.form)
    return current_app.helper.ret_ok()

@bp.route("/delete_investment",methods=["POST"])
@view_exception_wrapper
@validate_form(DeleteInvestment)
@login_required
def api_delete_investment():
    im.delete_investment(g.form)
    return current_app.helper.ret_ok()

@bp.route("/get_investment_list",methods=["GET"])
@view_exception_wrapper
@validate_form(GetInvestmentList)
@login_required
def api_get_investment_list():
    im_info_list = im.get_investment_list(g.form)
    return current_app.helper.ret_ok(im_info_list=im_info_list)

@bp.route("/get_investment_info",methods=["GET"])
@view_exception_wrapper
@validate_form(GetInvestmentInfo)
@login_required
def api_get_investment_info():
    im_info = im.get_investment_info(g.form)
    return current_app.helper.ret_ok(im_info=im_info)

@bp.route("/add_news",methods=["POST"])
@view_exception_wrapper
@validate_form(AddNews)
@login_required
def api_add_news():
    news_id = nm.add_news(g.form)
    return current_app.helper.ret_ok(news_id=news_id)

@bp.route("/update_news",methods=["POST"])
@view_exception_wrapper
@validate_form(UpdateNews)
@login_required
def api_update_news():
    nm.update_news(g.form)
    return current_app.helper.ret_ok()

@bp.route("/delete_news",methods=["POST"])
@view_exception_wrapper
@validate_form(DeleteNews)
@login_required
def api_delete_news():
    nm.delete_news(g.form)
    return current_app.helper.ret_ok()

@bp.route("/get_news_list",methods=["GET"])
@view_exception_wrapper
@validate_form(GetNewsList)
@login_required
def api_get_news_list():
    news_meta_list = nm.get_news_list(g.form)
    return current_app.helper.ret_ok(news_meta_list=news_meta_list)

@bp.route("/get_news_meta",methods=["GET"])
@view_exception_wrapper
@validate_form(GetNewsMeta)
def api_get_news_meta():
    news_meta = nm.get_news_meta(g.form)
    return current_app.helper.ret_ok(news_meta=news_meta)

@bp.route("/add_addr",methods=["POST"])
@view_exception_wrapper
@validate_form(AddAddr)
@login_required
def api_add_addr():
    addr_id = am.add_addr(g.form)
    return current_app.helper.ret_ok(addr_id=addr_id)

@bp.route("/delete_addr",methods=["POST"])
@view_exception_wrapper
@validate_form(DeleteAddr)
@login_required
def api_delete_addr():
    am.delete_addr(g.form)
    return current_app.helper.ret_ok()

@bp.route("/update_addr",methods=["POST"])
@view_exception_wrapper
@validate_form(UpdateAddr)
@login_required
def api_update_addr():
    am.update_addr(g.form)
    return current_app.helper.ret_ok()

@bp.route("/get_addr_list",methods=["GET"])
@view_exception_wrapper
@validate_form(GetAddrList)
@login_required
def api_get_addr_list():
    addr_meta_list = am.get_addr_list(g.form)
    return current_app.helper.ret_ok(addr_meta_list=addr_meta_list)

@bp.route("/get_addr_meta",methods=["GET"])
@view_exception_wrapper
@validate_form(GetAddrMeta)
@login_required
def api_get_addr_meta():
    contact_addr = am.get_addr_meta(g.form)
    return current_app.helper.ret_ok(contact_addr=contact_addr)

@bp.route("/add_news_type",methods=["POST"])
@view_exception_wrapper
@validate_form(AddNewsType)
@login_required
def api_add_news_type():
    news_type_id = ntm.add_news_type(g.form)
    return current_app.helper.ret_ok(news_type_id=news_type_id)

@bp.route("/update_news_type",methods=["POST"])
@view_exception_wrapper
@validate_form(UpdateNewsType)
@login_required
def api_update_news_type():
    ntm.update_news_type(g.form)
    return current_app.helper.ret_ok()

@bp.route("/delete_news_type",methods=["POST"])
@view_exception_wrapper
@validate_form(DeleteNewsType)
@login_required
def api_delete_news_type():
    ntm.delete_news_type(g.form)
    return current_app.helper.ret_ok()

@bp.route("/get_news_type_list",methods=["GET"])
@view_exception_wrapper
@login_required
def api_get_news_type_list():
    type_meta_list = ntm.get_news_type_list()
    return current_app.helper.ret_ok(type_meta_list=type_meta_list)

@bp.route("/add_investment_type",methods=["POST"])
@view_exception_wrapper
@validate_form(AddInvestmentType)
@login_required
def api_add_investment_type():
    im_type_id = itm.add_investment_type(g.form)
    return current_app.helper.ret_ok(im_type_id=im_type_id)

@bp.route("/update_investment_type",methods=["POST"])
@view_exception_wrapper
@validate_form(UpdateInvestmentType)
@login_required
def api_update_investment_type():
    itm.update_investment_type(g.form)
    return current_app.helper.ret_ok()

@bp.route("/delete_investment_type",methods=["POST"])
@view_exception_wrapper
@validate_form(DeleteInvestmentType)
@login_required
def api_delete_investment_type():
    itm.delete_investment_type(g.form)
    return current_app.helper.ret_ok()

@bp.route("/get_im_type_list",methods=["GET"])
@view_exception_wrapper
@login_required
def api_get_im_type_list():
    type_meta_list = itm.get_im_type_list()
    return current_app.helper.ret_ok(type_meta_list=type_meta_list)


@bp.route("/add_image",methods=["POST"])
@view_exception_wrapper
@validate_form(AddImage)
@login_required
def api_add_image():
    image = cl.add_carousel(g.form)
    return current_app.helper.ret_ok(image_id=image)

@bp.route("/update_image",methods=["POST"])
@view_exception_wrapper
@validate_form(UpdateImage)
@login_required
def api_update_image():
    cl.update_image(g.form)
    return current_app.helper.ret_ok()

@bp.route("/delete_image",methods=["POST"])
@view_exception_wrapper
@validate_form(DeleteImage)
@login_required
def api_delete_image():
    cl.delete_image(g.form)
    return current_app.helper.ret_ok()

@bp.route("/get_image_list",methods=["GET"])
@view_exception_wrapper
@login_required
def api_get_image_list():
    image_list = cl.get_image_list()
    return current_app.helper.ret_ok(image_list=image_list)

@bp.route("/set_team_top",methods=["POST"])
@view_exception_wrapper
@validate_form(SetTeamTop)
@login_required
def api_set_team_top():
    tm.set_team_top(g.form)
    return current_app.helper.ret_ok()

@bp.route("/set_im_top",methods=["POST"])
@view_exception_wrapper
@validate_form(SetImTop)
@login_required
def api_set_im_top():
    im.set_im_top(g.form)
    return current_app.helper.ret_ok()

@bp.route("/set_news_top",methods=["POST"])
@view_exception_wrapper
@validate_form(SetNewsTop)
@login_required
def api_set_news_top():
    nm.set_news_top(g.form)
    return current_app.helper.ret_ok()

@bp.route("/get_top_news",methods=["GET"])
@view_exception_wrapper
@login_required
def api_get_top_news():
    news_meta_list = nm.get_top_news()
    return current_app.helper.ret_ok(news_meta_list=news_meta_list)


@bp.route("/get_top_im",methods=["GET"])
@view_exception_wrapper
@login_required
def api_get_top_im():
    im_info_list = im.get_top_im()
    return current_app.helper.ret_ok(im_info_list=im_info_list)

@bp.route("/get_top_team",methods=["GET"])
@view_exception_wrapper
@login_required
def api_get_top_team():
    tm_meta_list = tm.get_top_team()
    return current_app.helper.ret_ok(tm_meta_list=tm_meta_list)


@bp.route("/add_tab",methods=["POST"])
@view_exception_wrapper
@validate_form(AddTab)
@login_required
def api_add_tab():
    tab_id = abm.add_tab(
            bg_image=g.form.bg_image.data,
            title=g.form.title.data,
            slogan=g.form.slogan.data)
    return current_app.helper.ret_ok(tab_id=tab_id)

@bp.route("/update_tab",methods=["POST"])
@view_exception_wrapper
@validate_form(UpdateTab)
@login_required
def api_update_tab():
    abm.update_tab(
            tab_id=g.form.tab_id.data,
            bg_image=g.form.bg_image.data,
            title=g.form.title.data,
            slogan=g.form.slogan.data)
    return current_app.helper.ret_ok()

@bp.route("/get_tab_list",methods=["GET"])
@view_exception_wrapper
@login_required
def api_get_tab_list():
    tab_list = abm.get_tab_list()
    return current_app.helper.ret_ok(tab_list=tab_list)


@bp.route("/delete_tab",methods=["POST"])
@view_exception_wrapper
@validate_form(DeleteTab)
@login_required
def api_delete_tab():
    abm.delete_tab(
            tab_id=g.form.tab_id.data)
    return current_app.helper.ret_ok()

@bp.route("/set_tab_top",methods=["POST"])
@view_exception_wrapper
@validate_form(SetTabTop)
@login_required
def api_set_tab_top():
    abm.set_tab_top(g.form)
    return current_app.helper.ret_ok()

@bp.route("/get_top_tab",methods=["GET"])
@view_exception_wrapper
@login_required
def api_get_top_tab():
    tab_list = abm.get_top_tab()
    return current_app.helper.ret_ok(tab_list=tab_list)
