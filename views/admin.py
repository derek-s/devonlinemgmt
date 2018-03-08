# !/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, request, url_for, flash, session, redirect
from flask_login import login_required, current_user
from decorators import admin_required
from models import Dev_Loging, Setting, Dev_Note
from log import eventlog
from base64 import b64decode
from urllib import unquote
from sysmanger import optionsupdate
import arrow
from ext import db
from notice import noticeindexlist

adminbg = Blueprint('adminbg', __name__)


@adminbg.route("/admin")
@login_required
@admin_required
def admin():
    """
    管理后台视图
    :return: 返回管理页面
    """
    notice = noticeindexlist()
    return render_template('/admin/admin.html', data=notice)


@adminbg.route("/admin/query")
@login_required
@admin_required
def query():
    """
    数据查询视图
    :return: 返回数据查询结果并构建相应页面
    """
    return render_template('/admin/dbquery.html')


@adminbg.route("/admin/lvrmanage")
@login_required
@admin_required
def lvrmanager():
    """
    弱电间管理视图
    :return: 返回数据查询结果并构建相应页面
    """
    return render_template('/admin/lvrmanager.html')


@adminbg.route("/admin/dvrmanage")
@login_required
@admin_required
def dvrmanage():
    """
    :return: 返回数据查询结果并构建相应页面
    """
    return render_template('/admin/dvrmanage.html')


@adminbg.route("/admin/dvrstatus")
@login_required
@admin_required
def dvrstatus():
    """
    :return: 返回数据查询结果并构建相应页面
    """
    return render_template('/admin/dvrstatus.html')


@adminbg.route("/admin/basicinfo")
@login_required
@admin_required
def basicinfo():
    """
    :return: 返回数据查询结果并构建相应页面
    """
    return render_template('/admin/basicinfo.html')


@adminbg.route("/admin/usrmanage")
@login_required
@admin_required
def usrmanage():
    """
    :return: 返回数据查询结果并构建相应页面
    """
    return render_template('/admin/usrmanage.html')


@adminbg.route("/admin/sysmanage", methods=['GET', 'POST'])
@login_required
@admin_required
def sysmanage():
    """
    :return: 返回数据查询结果并构建相应页面
    """
    eventlog("[访问系统设置]")
    default_value = ""
    if request.method == 'POST':
        pagesize = request.form.get('syspagen', 1)
        if pagesize.isdigit():
            optionsupdate('pagination', int(pagesize))
            flash(u"修改完成。", 'success')
            eventlog("[修改系统设置]")
        else:
            session.pop('_flashes', None)
            flash(u"分页条数输入有误，请检查输入。", 'danger')
    syspagn = Setting().pagination
    return render_template('/admin/sysmanage.html', syspagn=syspagn)


@adminbg.route("/admin/log", methods=['GET', 'POST'])
@login_required
@admin_required
def logviews():
    """
    操作日志界面
    :return: 返回数据查询结果并构建相应页面
    """
    page = request.values.get('page', 1, type=int)
    uname = request.values.get('username', "", type=str)
    username = b64decode(unquote(uname))
    catsname = request.values.get('cats', "", type=str)
    cats = b64decode(unquote(catsname))
    date = request.values.get('date', "", type=str)
    logdata = Dev_Loging.query.filter(
        (Dev_Loging.UserName.like("%" + username + "%"), "")[username is None],
        (Dev_Loging.Date.like("%" + date + "%"), "")[date is None],
        (Dev_Loging.Log.like("%" + cats + "%"), "")[cats is None]
    )
    paginateion = logdata.paginate(
        page, per_page=Setting().pagination
    )
    posts = paginateion.items
    count = logdata.count()
    eventlog("[查看日志]" + " 第" + str(page) +"页")
    return render_template(
        '/admin/log.html', posts=posts, count=count, pagination=paginateion,
        page=page, username=uname, cats=catsname, date=date,
        thuname=username.decode('utf-8'), thcats=cats.decode('utf-8')
    )


@adminbg.route("/admin/notecreate", methods=['GET', 'POST'])
@login_required
@admin_required
def notecreate():
    """
    通知公告创建页面
    :return:
    """
    eventlog("[访问创建公告页面]")
    notename = ""
    notecontent = ""
    if request.method == 'POST':
        notename = request.form.get('notename', "默认标题")
        notecontent = request.form.get('note', None)
        createdate = arrow.now().format("YYYY-MM-DD HH:mm")
        createname = current_user.username
        note = Dev_Note(notename, notecontent, createdate, createname)
        db.session.add(note)
        db.session.commit()
        flash(u"发布成功", 'success')
        return redirect(url_for('adminbg.notecreate_id', id=note.id))
    return render_template(
        '/admin/notecreate.html', name=notename, editorcontent=notecontent, operation=u"创建公告")


@adminbg.route("/admin/notecreate/<id>", methods=['GET', 'POST'])
@login_required
@admin_required
def notecreate_id(id):
    """
    通知公告创建页面
    :return:
    """
    eventlog("[访问修改公告页面 公告id: " + str(id) + "]")
    notename = ""
    notecontent = ""
    if request.method == 'GET':
        note = Dev_Note.query.filter(Dev_Note.id == id).one()
        notename = note.articlename
        notecontent = note.article
        return render_template(
            '/admin/notecreate.html', name=notename, editorcontent=notecontent, operation=u"编辑公告")
    if request.method == 'POST':
        notename = request.form.get('notename', "默认标题")
        notecontent = request.form.get('note', None)
        createdate = arrow.now().format("YYYY-MM-DD HH:mm")
        createname = current_user.username
        note = Dev_Note.query.filter(Dev_Note.id == id).one()
        note.articlename = notename
        note.article = notecontent
        note.createdate = createdate
        note.createuser = createname
        db.session.commit()
        flash(u"修改成功", 'success')
        return redirect(url_for('adminbg.notecreate_id', id=note.id))


@adminbg.route("/admin/notelist", methods=['GET', 'POST'])
@login_required
@admin_required
def notelist():
    """
    通知公告列表页
    :return:
    """
    page = request.values.get('page', 1, type=int)
    aname = request.values.get('aname', "", type=str)
    cuser = request.values.get('cuser', "", type=str)
    cdata = request.values.get('cdata', "", type=str)
    notices = Dev_Note.query.filter(
        (Dev_Note.articlename.like("%" + aname + "%"), "")[aname is None],
        (Dev_Note.createuser.like("%" + cuser + "%"), "")[cuser is None],
        (Dev_Note.createdate.like("%" + cdata + "%"), "")[cdata is None]
    )
    paginateion = notices.paginate(
        page, per_page=Setting().pagination
    )
    posts = paginateion.items
    count = notices.count()
    eventlog("[查看通知公告列表页] " + "第" + str(page) + "页")
    return render_template(
        "/admin/noticelist.html", posts=posts, count=count, pagination=paginateion,
        page=page
    )

