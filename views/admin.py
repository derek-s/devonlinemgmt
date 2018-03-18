# !/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Blueprint, jsonify, render_template, request, url_for, flash, session, redirect, abort
from flask_login import login_required, current_user
from decorators import admin_required
from models import Dev_Loging, Setting, Dev_Note, Dev_DeviceStatus, Dev_Campus, Dev_LVRInfo
from log import eventlog
from base64 import b64decode
from urllib import unquote
from sysmanger import optionsupdate
import arrow
from ext import db
from notice import noticeindexlist
from pevent import peventsindexlist
import json

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
    return render_template('/admin/admin.html', data=notice, events=event)


@adminbg.route("/admin/query")
@login_required
@admin_required
def query():
    """
    数据查询视图
    :return: 返回数据查询结果并构建相应页面
    """
    page = request.args.get('page', 1, type=int)
    request.script_root = url_for('indexview.index', _external=True)
    #request.script_root = url_for('adminbg.query', _external=True)
    count = Dev_DeviceStatus.query.count()
    pagination = Dev_DeviceStatus.query.order_by(Dev_DeviceStatus.Campus.desc()).paginate(
        page, per_page=Setting().pagination
    )
    posts = pagination.items
    campus = Dev_Campus.query.all()

    return render_template('/admin/dbquery.html', posts=posts, count=count, pagination=pagination, campus=campus)


@adminbg.route("/admin/query/list")
@login_required
@admin_required
def query_list():
    """
    后台查询视图 根据校区/楼宇进行查询
    :return: json
    """
    page = request.args.get('page', 1, type=int)
    request.script_root = url_for('indexview.index', _external=True)
    campusname = b64decode(unquote(request.args.get('campusname', "", type=str)))
    buildname = b64decode(unquote(request.args.get('buildname', "", type=str)))
    devinfo = Dev_DeviceStatus.query.filter(
        (Dev_DeviceStatus.Campus.like("%" + campusname + "%"), "")[campusname is None],
        (Dev_DeviceStatus.Location.like("%" + buildname + "%"), "")[buildname is None]
    ).order_by(Dev_DeviceStatus.Campus.desc())
    paginateion = devinfo.paginate(
        page, per_page=Setting().pagination
    )
    count = devinfo.count()
    posts = paginateion.items
    campus = Dev_Campus.query.all()
    eventlog(
        "[查询校区/楼宇]" + campusname + buildname + " 第" + str(page) + "页"
    )
    return render_template(
        "/admin/dbquery_list.html", posts=posts, count=count, pagination=paginateion, campus=campus,
        ctitle=campusname.decode('utf-8'), btitle=buildname.decode('utf-8')
    )


@adminbg.route("/admin/query/serach")
@login_required
@admin_required
def query_serach():
    """
    数据查询搜索页
    :return:
    """
    request.script_root = url_for('indexview.index', _external=True)
    page = request.args.get('page', 1, type=int)
    word = request.args.get('keyword', "", type=str)
    serach = unquote(b64decode(word)).decode('utf-8')
    serp = Dev_DeviceStatus.query.filter(
        (Dev_DeviceStatus.Campus.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.Location.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.RoomNo.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HostName.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.LAA.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HigherlinkIP.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HigherlinkPort.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.DeviceModel.like("%" + serach + "%"), "")[serach is None]
    ).order_by(Dev_DeviceStatus.Campus.desc())
    paginateion = serp.paginate(
        page, per_page=Setting().pagination
    )
    count = serp.count()
    posts = paginateion.items
    eventlog(
        "[搜索]" + serach.encode('utf-8') + " 第" + str(page) + "页"
    )
    return render_template(
        '/admin/dbquery_serach.html', posts=posts, count=count, pagination=paginateion, keyword=serach
    )



@adminbg.route("/admin/lvrmanage")
@login_required
@admin_required
def lvrmanager():
    """
    弱电间管理视图
    :return: 返回数据查询结果并构建相应页面
    """
    request.script_root = url_for('indexview.index', _external=True)
    page = request.args.get('page', 1, type=int)
    count = Dev_LVRInfo.query.count()
    pagination = Dev_LVRInfo.query.order_by(Dev_LVRInfo.Campus.desc()).paginate(
        page, per_page=Setting().pagination
    )
    posts = pagination.items
    campus = Dev_Campus.query.all()
    return render_template('/admin/lvrmanager.html', posts=posts, count=count, pagination=pagination, campus=campus)


@adminbg.route("/admin/lvrmanage/_queryipage", methods=['POST'])
@login_required
@admin_required
def querylvrpage():
    """
    后台弱电间信息ajax查询
    :return:
    """
    count = request.values.get('count', None, type=int)
    pagenum = request.values.get('pagenum', None, type=int)
    page_num = ((count/Setting().pagination+pagenum), 0)[count/Setting().pagination == 0]
    lvrinfo = Dev_LVRInfo.query.order_by(Dev_LVRInfo.Campus.desc()).paginate(
        (page_num), per_page=Setting().pagination
    )
    lvrinfotemp = []
    hasnext = {
        'next': lvrinfo.has_next
    }
    for lvrx in lvrinfo.items:
        jsonlist = lvrx.to_json()
        jsonlist.update(hasnext)
        lvrinfotemp.append(jsonlist)
    eventlog(
        "弱电间ajax加载下一页" + " 第" + str(page_num) + "页"
    )
    return jsonify(lvrinfotemp)


@adminbg.route("/admin/lvrmanage/list")
@login_required
@admin_required
def querylvrlist():
    """
    后台弱电间信息校区查询
    :return:
    """
    page = request.args.get('page', 1, type=int)
    request.script_root = url_for('indexview.index', _external=True)
    campusname = b64decode(unquote(request.args.get('campusname', "", type=str)))
    buildname = b64decode(unquote(request.args.get('buildname', "", type=str)))
    lvrinfo = Dev_LVRInfo.query.filter(
        (Dev_LVRInfo.Campus.like("%" + campusname + "%"), "")[campusname is None],
        (Dev_LVRInfo.BuildName.like("%") + buildname + "%", "")[buildname is None]
    ).order_by(Dev_LVRInfo.Campus.desc())
    paginateion = lvrinfo.paginate(
        page, per_page=Setting().pagination
    )
    count = lvrinfo.count()
    posts = paginateion.items
    campus = Dev_Campus.query.all()
    eventlog(
        "[后台弱电间信息 查询校区/楼宇]" + campusname + buildname + " 第" + str(page) + "页"
    )
    return render_template(
        "/admin/lvrmanage_list.html", posts=posts, count=count, pagination=paginateion, campus=campus,
        ctitle=campusname.decode('utf-8'), btitle=buildname.decode('utf-8')
    )


@adminbg.route("/admin/lvrmanage/search")
@login_required
@admin_required
def querylvrserach():
    """
    后台弱电间信息搜索在
    :return:
    """
    page = request.args.get('page', 1, type=int)
    request.script_root = url_for('indexview.index', _external=True)
    page = request.args.get('page', 1, type=int)
    word = request.args.get('keyword', "", type=str)
    serach = unquote(b64decode(word)).decode('utf-8')
    serp = Dev_LVRInfo.query.filter(
        (Dev_LVRInfo.Campus.like("%" + serach + "%"), "")[serach is None] |
        (Dev_LVRInfo.BuildName.like("%" + serach + "%"), "")[serach is None] |
        (Dev_LVRInfo.BuildNo.like("%" + serach + "%"), "")[serach is None] |
        (Dev_LVRInfo.RoomNo.like("%" + serach + "%"), "")[serach is None] |
        (Dev_LVRInfo.LVRNo.like("%" + serach + "%"), "")[serach is None]
    ).order_by(Dev_LVRInfo.Campus.desc())
    paginateion = serp.paginate(
        page, per_page=Setting().pagination
    )
    count = serp.count()
    posts = paginateion.items
    eventlog(
        "[管理后台弱电间 搜索]" + serach.encode('utf-8') + " 第" + str(page) + "页"
    )
    return render_template(
        "/admin/lvrmanage_serach.html", posts=posts, count=count, pagination=paginateion, keyword=serach
    )


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

