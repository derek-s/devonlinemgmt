# !/usr/bin/python
# -*- coding: utf-8 -*-

from flask import (Flask, render_template, url_for, request, Blueprint)
from flask_login import login_required

from models import Dev_DeviceStatus, Dev_DeviceInfo, Dev_Campus, Dev_LVRInfo, Setting, Dev_Note
from log import eventlog
from base64 import b64decode
from urllib import unquote

indexview = Blueprint('indexview', __name__)


@indexview.route("/", methods=['GET', 'POST'])
@login_required
def index():
    """首页函数"""
    eventlog(
        "[访问首页]"
    )
    page = request.args.get('page', 1, type=int)
    request.script_root = url_for('indexview.index', _external=True)
    count = Dev_DeviceStatus.query.count()
    pagination = Dev_DeviceStatus.query.order_by(Dev_DeviceStatus.Campus.desc()).paginate(
        page, per_page=Setting().pagination
    )
    posts = pagination.items
    campus = Dev_Campus.query.all()
    return render_template('index.html', posts=posts, count=count, pagination=pagination, campus=campus)


@indexview.route("/list", methods=['GET', 'POST'])
@login_required
def indexlist():
    """根据校区/楼宇进行查询"""
    page = request.args.get('page', 1, type=int)
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
        "list.html", posts=posts, count=count, pagination=paginateion, campus=campus,
        ctitle=campusname.decode('utf-8'), btitle=buildname.decode('utf-8')
    )


@indexview.route("/notice/<id>")
@login_required
def indexnotice(id):
    """
    前台通知公告显示页
    :param id:
    :return:
    """
    note = Dev_Note.query.filter(Dev_Note.id == id).one()
    print note
    return render_template("notice.html", notice=note)
