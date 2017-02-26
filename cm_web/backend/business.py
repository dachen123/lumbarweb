#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask.ext.login import current_user
from cm_web.storage import db
from cm_web.storage.data import *
from cm_web.helper import update_field

class TeamManager(object):
    def __init__(self):
        pass

    def add_team_member(self,form):
        try:
            tm = TeamMember(
                light_avatar = form.light_avatar.data,
                dark_avatar = form.dark_avatar.data,
                name = form.name.data,
                description = form.description.data
                    )
            tm.add_to_db(commit=True)
        except Exception,e:
            db.session.rollback()
            raise CMException(info=e,log_msg=e)
        return tm.id

    
    def update_team_member(self,form):
        try:
            tm = TeamMember.get(form.tm_id.data)
            if not tm:
                raise CMException(info=u'找不到成员记录',
                        log_msg=(u'找不到id=%s的成员记录,无法进行编辑操作'))

            update_field(
                    tm,
                    light_avatar = form.light_avatar.data,
                    dark_avatar = form.dark_avatar.data,
                    name= form.name.data,
                    description = form.description.data)
            tm.add_to_db(commit=True)
        except Exception,e:
            db.session.rollback()

    def delete_team_member(self,form):
        try:
            tm = TeamMember.get(form.tm_id.data)
            if not tm:
                raise CMException(info=u'找不到成员记录',
                        log_msg=(u'找不到id=%s的成员记录,无法进行删除操作'))
            tm.delete()
            db.commit()
        except Exception,e:
            db.session.rollback()

    def get_team_member_list(self,form):
        start = form.start_index.data - 1
        if form.count.data < 0:
            count = 100
        else:
            count = form.count.data
        stop = start + count

        team_list = TeamMember.query_valid_entry()\
                .order_by(TeamMember.update_time.desc())[start:stop]
        # team_list = TeamMember.query_valid_entry()\
        #         .order_by(TeamMember.update_time.desc()).all()
        tm_meta_list = []
        for t in team_list:
            tm_meta_list.append(t.tm_meta)

        return tm_meta_list

    def get_team_member_meta(self,form):
        tm = TeamMember.get(form.tm_id.data)
        if not tm:
            raise CMException(info=u'找不到指定的成员记录',
                    log_msg=(u'找不到id=%s的成员记录'% form.tm_id.data))
        return tm.tm_meta

    def set_team_top(self,form):
        tm = TeamMember.get(form.tm_id.data)
        if not tm:
            raise CMException(info=u'找不到指定的成员记录',
                    log_msg=(u'找不到id=%s的成员记录'% form.tm_id.data))
        tm.top=form.top.data
        tm.add_to_db(commit=True)

    def get_top_team(self):
        tm_list = TeamMember.query_valid_entry().filter(
                TeamMember.top==True).all()
        tm_meta_list=[]
        for t in tm_list:
            tm_meta_list.append(t.tm_meta)
        return tm_meta_list


class ImManager(object):
    def __init__(self):
        pass
    
    def add_investment(self,form):
        try:
            im = Investment(
                    company_name=form.company_name.data,
                    cover_image=form.cover_image.data,
                    company_url=form.company_url.data,
                    company_addr=form.company_addr.data,
                    pm_manager=form.pm_manager.data,
                    company_introduce=form.company_introduce.data)
            im.add_to_db(commit=True)

            db.session.execute("insert into investment_investment_type(im_id, type_id) \
                        values (:im_id, :type_id)", {'im_id':im.id, 'type_id':form.type_id.data}  )
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            raise CMException(info=e,log_msg=e)
        return im.id

    def update_investment(self,form):
        try:
            im = Investment.get(form.im_id.data)
            if not im:
                raise CMException(info=u'找不到指定id的项目',
                        log_msg=(u'找不到指定id的项目,无法进行编辑操作'))
            update_field(im,
                    company_name=form.company_name.data,
                    cover_image=form.cover_image.data,
                    company_url=form.company_url.data,
                    company_addr=form.company_addr.data,
                    pm_manager=form.pm_manager.data,
                    company_introduce=form.company_introduce.data)
            db.session.execute("delete from investment_investment_type where im_id=:im_id", {'im_id':im.id})
            db.session.execute("insert into investment_investment_type(im_id, type_id) \
                        values (:im_id, :type_id)", {'im_id':im.id, 'type_id':form.type_id.data}  )
            im.add_to_db(commit=True)
        except Exception,e:
            print e
            db.session.rollback()
            raise CMException(info=e,log_msg=e)

    def delete_investment(self,form):
        try:
            im = Investment.get(form.im_id.data)
            if not im:
                raise CMException(info=u'找不到指定id的项目',
                        log_msg=(u'找不到指定id的项目,无法进行删除操作'))
            im.delete()
            db.commit()
        except Exception,e:
            db.session.rollback()
            raise CMException(info=e,log_msg=e)

    def get_investment_list(self,form):
        try:
            start = form.start_index.data - 1
            count = 0
            if form.count.data < 0:
                count = 100
            else:
                count = form.count.data
            stop = start + count
            im_list = Investment.query_valid_entry()\
                    .order_by(Investment.update_time.desc())[start:stop]
            # im_list = Investment.query_valid_entry()\
            #         .order_by(Investment.update_time.desc()).all()
            im_info_list=[]
            for i in im_list:
                im_info_list.append(i.im_info)
        except Exception,e:
            raise CMException(log=e,log_msg=e)
        return im_info_list

    def get_investment_info(self,form):
        im = Investment.get(form.im_id.data)
        if not im:
            raise CMException(info=u'未找到指定id的项目',
                    log_msg=u'未找到指定id%s的项目'%form.im_id.data)
        return im.im_info

    def set_im_top(self,form):
        im = Investment.get(form.im_id.data)
        if not im:
            raise CMException(info=u'未找到指定id的项目',
                    log_msg=u'未找到指定id%s的项目'%form.im_id.data)
        im.top=form.top.data
        im.add_to_db(commit=True)

    def get_top_im(self):
        im_list = Investment.query_valid_entry().filter(
                Investment.top==True).all()
        im_info_list = []
        for i in im_list:
            im_info_list.append(i.im_info)
        return im_info_list

class NewsManager(object):
    def __init__(self):
        pass

    def add_news(self,form):
        n = News(
                title = form.title.data,
                cover_image=form.cover_image.data,
                content = form.content.data)
        n.add_to_db(commit=True)
        db.session.execute("insert into news_news_type(news_id, type_id) \
                    values (:news_id, :type_id)", {'news_id':n.id, 'type_id':form.type_id.data}  )
        db.session.commit()
        return n.id

    def update_news(self,form):
        n = News.get(form.news_id.data)
        if not n:
            raise CMException( info=u'未找到指定id的新闻',
                    log_msg=u'未找到指定id%s的新闻' % form.news_id.data)
        update_field(n,
                title=form.title.data,
                cover_image=form.cover_image.data,
                content=form.content.data)
        db.session.execute("delete from news_news_type where news_id=:news_id", {'news_id':n.id})
        db.session.execute("insert into news_news_type(news_id, type_id) \
                    values (:news_id, :type_id)", {'news_id':n.id, 'type_id':form.type_id.data}  )
        n.add_to_db(commit=True)

    def delete_news(self,form):
        n = News.get(form.news_id.data)
        if not n:
            raise CMException( info=u'未找到指定id的新闻',
                    log_msg=u'未找到指定id%s的新闻' % form.news_id.data)
        n.delete()
        db.commit()

    def get_news_list(self,form):
        start = form.start_index.data - 1
        count = 0
        if form.count.data < 0:
            count = 100
        else:
            count = form.count.data
        stop = start + count
        news_list = News.query_valid_entry()\
                .order_by(News.update_time.desc())[start:stop]
        # news_list = News.query_valid_entry()\
        #         .order_by(News.update_time.desc()).all()
        news_meta_list = []
        for n in news_list:
            news_meta_list.append(n.news_meta)
        return news_meta_list

    def get_news_meta(self,form):
        n = News.get(form.news_id.data)
        if not n:
            raise CMException( info=u'未找到指定id的新闻',
                    log_msg=u'未找到指定id%s的新闻' % form.news_id.data)

        return n.news_meta

    def set_news_top(self,form):

        n = News.get(form.news_id.data)
        if not n:
            raise CMException( info=u'未找到指定id的新闻',
                    log_msg=u'未找到指定id%s的新闻' % form.news_id.data)
        n.top=form.top.data
        n.add_to_db(commit=True)

    def get_top_news(self):
        news_list = News.query_valid_entry().filter(
                News.top==True).all()
        news_meta_list = []
        for n in news_list:
            news_meta_list.append(n.news_meta)
        return news_meta_list



class ContactAddrManager(object):
    def __init__(self):
        pass

    def add_addr(self,form):
        addr = ContactAddr(
                city=form.city.data,
                cover_image=form.cover_image.data,
                detail_addr=form.detail_addr.data,
                phone=form.phone.data,
                mail=form.mail.data,
                fax_no=form.fax_no.data,
                baidu_share=form.baidu_share.data)
        addr.add_to_db(commit=True)
        return addr.id

    def update_addr(self,form):
        addr = ContactAddr.get(form.addr_id.data)

        if not addr:
            raise CMException( info=u'找不到指定id的地址记录',
                    log_msg=u'找不到指定id的地址记录')
        update_field(addr,
                city=form.city.data,
                cover_image=form.cover_image.data,
                detail_addr=form.detail_addr.data,
                phone=form.phone.data,
                mail=form.mail.data,
                fax_no=form.fax_no.data,
                baidu_share=form.baidu_share.data)
        addr.add_to_db(commit=True)

    def delete_addr(self,form):
        addr = ContactAddr.get(form.addr_id.data)

        if not addr:
            raise CMException( info=u'找不到指定id的地址记录',
                    log_msg=u'找不到指定id的地址记录')
        addr.delete()
        db.commit()

    def get_addr_list(self,form):
        start = form.start_index.data - 1
        count = 0
        if form.count.data < 0:
            count = 100
        else:
            count = form.count.data
        stop = start + count
        addr_list = ContactAddr.query_valid_entry()\
                .order_by(ContactAddr.update_time.desc()).all()
        # addr_list = ContactAddr.query_valid_entry()\
        #         .order_by(ContactAddr.update_time.desc())[start:stop]
        addr_meta_list = []
        for a in addr_list:
            addr_meta_list.append(a.contact_addr)
        return addr_meta_list

    def get_addr_meta(self,form):
        addr = ContactAddr.get(form.addr_id.data)
        if not addr:
            raise CMException(info=u'找不到指定id的地址记录',
                    log_msg=u'找不到指定id地址的记录')
        return addr.contact_addr


class InvestmentTypeManager(object):
    def __init__(self):
        pass

    def add_investment_type(self,form):
        try:
            it = InvestmentType(
                    type_name = form.type_name.data,
                    description = form.description.data)
            it.add_to_db(commit=True)
        except Exception,e:
            raise CMException(info=e,
                    log_msg=e)
        return it.id

    def update_investment_type(self,form):
        it = InvestmentType.get(form.type_id.data)
        if not it:
            raise CMException( info=u'找不到指定id的项目类型',
                    log_msg=u'找不到指定id的项目类型')
        update_field(it,
                type_name=form.type_name.data,
                description=form.description.data)

    def delete_investment_type(self,form):
        it = InvestmentType.get(form.type_id.data)
        if not it:
            raise CMException( info=u'找不到指定id的项目类型',
                    log_msg=u'找不到指定id的项目类型')
        it.delete()

    def get_im_type_list(self):
        type_list = InvestmentType.query\
                .order_by(InvestmentType.create_time.asc()).all()
        type_meta_list = []
        for t in type_list:
            type_meta_list.append(t.im_type_meta)
        return type_meta_list


class NewsTypeManager(object):
    def __init__(self):
        pass

    def add_news_type(self,form):
        try:
            nt = NewsType(
                    type_name = form.type_name.data,
                    description = form.description.data)
            nt.add_to_db(commit=True)
        except Exception,e:
            raise CMException(info=e,
                    log_msg=e)
        return nt.id

    def update_news_type(self,form):
        nt = NewsType.get(form.type_id.data)
        if not nt:
            raise CMException( info=u'找不到指定id的新闻类型',
                    log_msg=u'找不到指定id的新闻类型')
        update_field(nt,
                type_name=form.type_name.data,
                description=form.description.data)
    def delete_news_type(self,form):
        nt = NewsType.get(form.type_id.data)
        if not nt:
            raise CMException( info=u'找不到指定id的新闻类型',
                    log_msg=u'找不到指定id的新闻类型')
 
        nt.delete()

    def get_news_type_list(self):
        type_list = NewsType.query\
                .order_by(NewsType.create_time.asc()).all()
        type_meta_list = []
        for t in type_list:
            type_meta_list.append(t.news_type_meta)
        return type_meta_list


class Carousel( object ):
    def __init__(self):
        pass

    def add_carousel(self,form):
        image = Indexcarousel(
                image=form.image.data,
                title=form.title.data,
                content=form.content.data)
        image.add_to_db(commit=True)
        return image.id

    
    def update_image(self,form):
        image = Indexcarousel.get( form.image_id.data)

        if not image:
            raise CMException( info=u'找不到指定Id的轮播图',
                    log_msg=(u'找不到指定id的轮播图'))
        # image.image = form.image.data
        image.image = form.image.data
        update_field(image,
                image=form.image.data,
                title=form.title.data,
                content=form.content.data)
        image.add_to_db( commit=True)

    def delete_image(self,form):
        image = Indexcarousel.get( form.image_id.data)

        if not image:
            raise CMException( info=u'找不到指定Id的轮播图',
                    log_msg=(u'找不到指定id的轮播图'))
        image.delete(commit=True)

    def get_image_list(self):
        image_list = Indexcarousel.query.\
                order_by(Indexcarousel.create_time.asc()).all()

        image_meta_list = []
        for i  in image_list:
            image_meta_list.append(i.carousel)
        return image_meta_list


class AbManager(object):
    def __init__(self):
        pass

    def add_tab(self,bg_image,title,slogan):
        t = AboutUs(
                bg_image=bg_image,
                title=title,
                slogan=slogan)
        t.add_to_db(commit=True)
        return t.id

    def update_tab(self,tab_id,bg_image,title,slogan):
        t = AboutUs.get(tab_id)
        if not t:
            raise CMException(info=u'找不到指定id的tab',
                    log_msg=(u'找不到指定id的tab'))
        update_field(t,
                bg_image=bg_image,
                title=title,
                slogan=slogan)

    def get_tab_list(self):
        tab_list = AboutUs.query_valid_entry()\
                .filter(AboutUs.top==False)\
                .all()

        tab_meta_list = []
        for t in tab_list:
            tab_meta_list.append(t.about_us)
        return tab_meta_list

    def delete_tab(self,tab_id):
        t = AboutUs.get(tab_id)
        if not t:
            raise CMException(info=u'找不到指定id的tab',
                    log_msg=(u'找不到指定id的tab'))

        t.delete()
        db.commit()

    def set_tab_top(self,form):
        t = AboutUs.get(form.tab_id.data)
        if not t:
            raise CMException(info=u'找不到指定的tab记录',
                    log_msg=(u'找不到id=%s的tab记录'% form.tab_id.data))
        t.top=form.top.data
        t.add_to_db(commit=True)

    def get_top_tab(self):
        t_list = AboutUs.query_valid_entry()\
                .filter(AboutUs.top==True)\
                .order_by(AboutUs.create_time.asc()).all()

        t_meta_list = []
        for t in t_list:
            t_meta_list.append(t.about_us)
        return t_meta_list

