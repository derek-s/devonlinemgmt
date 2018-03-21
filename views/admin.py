# !/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Blueprint, jsonify, render_template, request, url_for, flash, session, redirect, abort
from flask_login import login_required, current_user
from decorators import admin_required
from models import Dev_Loging, Setting, Dev_Note, Dev_DeviceStatus, Dev_Campus, Dev_LVRInfo, Dev_DeviceInfo, DevDevType
from log import eventlog
from base64 import b64decode
from urllib import unquote
from sysmanger import optionsupdate
import arrow
from ext import db
from notice import noticeindexlist
from pevent import peventsindexlist
import json

from .admin_dbquery import admin_query, admin_query_list, admin_query_serach
from .admin_lvr import  lvr_manager_index, lvr_manager_ajaxquery
from .admin_lvr import lvr_list_get, lvr_list_post, lvr_search_get, lvr_search_post


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
    event = peventsindexlist(current_user.username)
    return render_template('/admin/admin.html',
                           data=notice,
                           events=event
                           )


@adminbg.route("/admin/query")
@login_required
@admin_required
def query():
    """
    数据查询视图
    :return: 返回数据查询结果并构建相应页面
    """
    result = admin_query()
    return render_template(
        '/admin/dbquery.html',
        posts=result['posts'],
        count=result['count'],
        pagination=result['pagination'],
        campus=result['campus']
    )


@adminbg.route("/admin/query/list")
@login_required
@admin_required
def query_list():
    """
    后台查询视图 根据校区/楼宇进行查询
    :return: json
    """
    result = admin_query_list()
    return render_template(
        "/admin/dbquery_list.html",
        posts=result['posts'],
        count=result['count'],
        pagination=result['pagination'],
        campus=result['campus'],
        ctitle=result['campusname'],
        btitle=result['buildname']
    )


@adminbg.route("/admin/query/serach", methods=['GET', 'POST'])
@login_required
@admin_required
def query_serach():
    """
    数据查询搜索页
    :return:
    """
    result = admin_query_serach()
    return render_template(
        '/admin/dbquery_serach.html',
        posts=result['posts'],
        count=result['count'],
        pagination=result['pagiation'],
        keyword=result['keyword']
    )


@adminbg.route("/admin/lvrmanage")
@login_required
@admin_required
def lvrmanager():
    """
    弱电间管理视图
    :return: 返回数据查询结果并构建相应页面
    """
    result = lvr_manager_index()
    return render_template(
        '/admin/lvrmanager.html',
        posts=result['posts'],
        count=result['count'],
        pagination=result['pagination'],
        campus=result['campus'])


@adminbg.route("/admin/lvrmanage/_queryipage", methods=['POST'])
@login_required
@admin_required
def querylvrpage():
    """
    后台弱电间信息ajax查询
    :return:
    """
    return lvr_manager_ajaxquery()


@adminbg.route("/admin/lvrmanage/list", methods=['GET', 'POST'])
@login_required
@admin_required
def querylvrlist():
    """
    后台弱电间信息校区查询
    :return:
    """
    if request.method == 'GET':
        result = lvr_list_get()
        return render_template(
            "/admin/lvrmanage_list.html",
            posts=result['posts'],
            count=result['count'],
            pagination=result['pagination'],
            campus=result['campus'],
            ctitle=result['ctitle'],
            btitle=result['btitle']
        )
    elif request.method == 'POST':
        return lvr_list_post()
    else:
        abort(404)



@adminbg.route("/admin/lvrmanage/search", methods=['GET', 'POST'])
@login_required
@admin_required
def querylvrserach():
    """
    后台弱电间信息搜索
    :return:
    """
    if request.method == 'GET':
        result = lvr_search_get()
        return render_template(
            "/admin/lvrmanage_serach.html",
            posts=result['posts'],
            count=result['count'],
            pagination=result['pagination'],
            keyword=result['keyword']
        )
    elif request.method == 'POST':
        return lvr_search_post()
    else:
        abort(500)


@adminbg.route("/admin/dvrmanage", methods=['GET', 'POST'])
@login_required
@admin_required
def dvrmanage():
    """
    :return: 返回数据查询结果并构建相应页面
    """
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        request.script_root = url_for('indexview.index', _external=True)
        count = Dev_DeviceInfo.query.count()
        pagination = Dev_DeviceInfo.query.order_by(Dev_DeviceInfo.ID.asc()).paginate(
            page, per_page=Setting().pagination
        )
        datas = pagination.items
        devtype = DevDevType.query.all()
        return render_template('/admin/dvrmanage.html', datas=datas, count=count, pagination=pagination, devtype=devtype)
    elif request.method == 'POST':
        count = request.values.get('count', None, type=int)
        pagenum = request.values.get('pagenum', None, type=int)
        page_num = ((count / Setting().pagination + pagenum), 0)[count / Setting().pagination == 0]
        dvrinfo = Dev_DeviceInfo.query.order_by(Dev_DeviceInfo.ID.asc()).paginate(
            (page_num), per_page=Setting().pagination
        )
        dvrinfotemp = []
        hasnext = {
            'next': dvrinfo.has_next
        }
        for devx in dvrinfo.items:
            jsonlist = devx.to_json()
            jsonlist.update(hasnext)
            dvrinfotemp.append(jsonlist)
        return jsonify(dvrinfotemp)


@adminbg.route("/admin/dvrmanage/list", methods=['GET', 'POST'])
@login_required
@admin_required
def dvrmanagelist():
    """
    设备信息页分类查询
    :return:
    """
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        request.script_root = url_for('indexview.index', _external=True)
        devtype = b64decode(unquote(request.args.get('devtype', "", type=str)))
        devonline = unquote(request.args.get('devonline', "", type=str))
        if devonline == "5piv":
            devonline = "Y"
        elif devonline == "5ZCm":
            devonline = "N"
        devinfo = dvrselectsql(devtype, devonline)
        pagination = devinfo.paginate(
            page, per_page=Setting().pagination
        )
        count = devinfo.count()
        datas = pagination.items
        dev_types = DevDevType.query.all()
        return render_template(
            '/admin/devmanage_list.html', datas=datas, count=count, pagination=pagination, devtype=dev_types,
            devtypebname=devtype.decode('utf-8'), devostatus=devonline)
    elif request.method == 'POST':
        devtype = b64decode(unquote(request.values.get('devtype', "", type=str)))
        devonline = unquote(request.values.get('devonline', "", type=str))
        if devonline == "5piv":
            devonline = "Y"
        elif devonline == "5ZCm":
            devonline = "N"
        count = request.values.get('count', None, type=int)
        pagenum = request.values.get('pagenum', None, type=int)
        page_num = ((count / Setting().pagination + pagenum), 0)[count / Setting().pagination == 0]
        devinfo = dvrselectsql(devtype, devonline)
        dvrinfo = devinfo.paginate(
            page_num, per_page=Setting().pagination
        )
        dvrinfotemp = []
        hasnext = {
            'next': dvrinfo.has_next
        }
        for devx in dvrinfo.items:
            jsonlist = devx.to_json()
            jsonlist.update(hasnext)
            dvrinfotemp.append(jsonlist)
        return jsonify(dvrinfotemp)

def dvrselectsql(devtype, devonline):
    """
    设备信息查询sql
    :return:
    """
    devinfo = Dev_DeviceInfo.query.filter(
        (Dev_DeviceInfo.DeviceCategory.like("%" + devtype + "%"), "")[devtype is None],
        (Dev_DeviceInfo.DeviceCondition.like("%" + devonline + "%"), "")[devonline is None]
    ).order_by(Dev_DeviceInfo.ID.asc())
    return devinfo


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
            flash(u"修改完成", 'success')
            eventlog("[修改系统设置]")
        else:
            session.pop('_flashes', None)
            flash(u"分页条数输入有误，请检查输入", 'danger')
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
    通知公告修改页面
    :return:
    """
    eventlog("[访问修改公告页面 公告id: " + str(id) + "]")
    notename = ""
    notecontent = ""
    if request.method == 'GET':
        try:
            note = Dev_Note.query.filter(Dev_Note.id == id).one()
            notename = note.articlename
            notecontent = note.article
            return render_template(
                '/admin/notecreate.html', name=notename, editorcontent=notecontent, operation=u"编辑公告")
        except Exception as e:
            abort(500)
    if request.method == 'POST':
        notename = request.form.get('notename', "默认标题")
        notecontent = request.form.get('note', None)
        createdate = arrow.now().format("YYYY-MM-DD HH:mm")
        createname = current_user.username
        try:
            note = Dev_Note.query.filter(Dev_Note.id == id).one()
            note.articlename = notename
            note.article = notecontent
            note.createdate = createdate
            note.createuser = createname
            db.session.commit()
            flash(u"修改成功", 'success')
            return redirect(url_for('adminbg.notecreate_id', id=note.id))
        except Exception as e:
            abort(500)


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
    b64aname = b64decode(unquote(aname))
    cuser = request.values.get('cuser', "", type=str)
    b64cuser = b64decode(unquote(cuser))
    cdata = request.values.get('cdata', "", type=str)
    notices = Dev_Note.query.filter(
        (Dev_Note.articlename.like("%" + b64aname + "%"), "")[aname is None],
        (Dev_Note.createuser.like("%" + b64cuser + "%"), "")[cuser is None],
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


@adminbg.route("/admin/notelist/<int:id>/delete", methods=['POST'])
@login_required
@admin_required
def notedel(id):
    """
    删除通知公告
    :param id: 公告id
    :return:
    """

    delstatus = {
        "status": 1,
        "message": "success"
    }
    notice = Dev_Note.query.filter(
        Dev_Note.id == id
    )
    if not notice:
        delstatus['status'] = 404
        delstatus['message'] = "Not Found"
        return json.dumps(delstatus)
    notice.delete()
    db.session.commit()
    eventlog("[删除公告 公告id: " + str(id) + "]")
    return json.dumps(delstatus)

