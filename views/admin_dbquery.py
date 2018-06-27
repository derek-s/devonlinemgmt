# !/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import request, url_for
from models import Setting, Dev_DeviceStatus, Dev_Campus
from log import eventlog
from base64 import b64decode
from urllib import unquote


def admin_query():
    page = request.args.get('page', 1, type=int)
    request.script_root = url_for('indexview.index', _external=True)
    # request.script_root = url_for('adminbg.query', _external=True)
    count = Dev_DeviceStatus.query.count()
    pagination = Dev_DeviceStatus.query.filter(Dev_DeviceStatus.DeviceCondition != "N").order_by(Dev_DeviceStatus.Campus.desc()).paginate(
        page, per_page=Setting().pagination
    )
    posts = pagination.items
    campus = Dev_Campus.query.all()
    result = {
        'posts': posts,
        'count': count,
        'pagination': pagination,
        'campus': campus
    }
    return result


def admin_query_list():
    page = request.args.get('page', 1, type=int)
    request.script_root = url_for('indexview.index', _external=True)
    campusname = b64decode(unquote(request.args.get('campusname', "", type=str)))
    buildname = b64decode(unquote(request.args.get('buildname', "", type=str)))
    devinfo = Dev_DeviceStatus.query.filter(
        Dev_DeviceStatus.DeviceCondition != "N",
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
    result = {
        'posts': posts,
        'count': count,
        'pagination': paginateion,
        'campus': campus,
        'campusname': campusname.decode('utf-8'),
        'buildname': buildname.decode('utf-8')
    }
    return result


def admin_query_serach():
    request.script_root = url_for('indexview.index', _external=True)
    page = request.args.get('page', 1, type=int)
    word = request.args.get('keyword', "", type=str)
    serach = unquote(b64decode(word)).decode('utf-8')
    serp = qserach(serach)
    paginateion = serp.paginate(
        page, per_page=Setting().pagination
    )
    count = serp.count()
    posts = paginateion.items
    eventlog(
        "[搜索]" + serach.encode('utf-8') + " 第" + str(page) + "页"
    )
    result = {
        'posts': posts,
        'count': count,
        'pagiation': paginateion,
        'keyword': serach
    }
    return result


def qserach(serach):
    serp = Dev_DeviceStatus.query.filter(
        Dev_DeviceStatus.DeviceCondition != "N",
        (Dev_DeviceStatus.Campus.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.Location.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.RoomNo.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HostName.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.LAA.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HigherlinkIP.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HigherlinkPort.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.DeviceModel.like("%" + serach + "%"), "")[serach is None]
    ).order_by(Dev_DeviceStatus.Campus.desc())
    return serp