#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/21 14:24
# @Author  : Derek.S
# @Site    : 设备信息管理
# @File    : admin_dvr.py

from flask import jsonify, request, url_for
from models import Setting, Dev_DeviceInfo, DevDevType, Dev_LVRInfo
from log import eventlog
from base64 import b64decode
from urllib import unquote
from models import Dev_Campus

def dvr_manage_get():
    page = request.args.get('page', 1, type=int)
    request.script_root = url_for('indexview.index', _external=True)
    count = Dev_DeviceInfo.query.count()
    pagination = Dev_DeviceInfo.query.order_by(Dev_DeviceInfo.ID.asc()).paginate(
        page, per_page=Setting().pagination
    )
    datas = pagination.items
    devtype = DevDevType.query.all()
    result = {
        'datas': datas,
        'count': count,
        'pagination': pagination,
        'devtype': devtype
    }
    return result


def dvr_manage_post():
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


def dvr_list_get():
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
    result = {
        'datas': datas,
        'count': count,
        'pagination': pagination,
        'devtype': dev_types,
        'devtypebname': devtype.decode('utf-8'),
        'devostatus': devonline
    }
    return result


def dvr_list_post():
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


def dvr_search_get():
    request.script_root = url_for('indexview.index', _external=True)
    page = request.args.get('page', 1, type=int)
    word = request.args.get('keyword', "", type=str)
    serach = unquote(b64decode(word)).decode('utf-8')
    serp = dvrsearchsql(serach)
    pagination = serp.paginate(
        page, per_page=Setting().pagination
    )
    count = serp.count()
    datas = pagination.items
    eventlog(
        "[管理后台设备信息 搜索]" + serach.encode('utf-8') + " 第" + str(page) + "页"
    )
    result = {
        'datas': datas,
        'count': count,
        'pagination': pagination,
        'keyword': serach
    }
    return result


def dvr_search_post():
    pagenum = request.values.get('pagenum', None, type=int)
    count = request.values.get('count', None, type=int)
    word = request.values.get('keyword', None, type=str)
    search = b64decode(unquote(word)).decode('utf-8')
    serp = dvrsearchsql(search)
    page_num = ((count / Setting().pagination + pagenum), 0)[count / Setting().pagination == 0]
    paginateion = serp.paginate(
        page_num, per_page=Setting().pagination
    )
    serachresult = []
    hasnext = {
        'next': paginateion.has_next
    }
    for serachone in paginateion.items:
        jsonlist = serachone.to_json()
        jsonlist.update(hasnext)
        serachresult.append(jsonlist)
    eventlog(
        "[ajax加载搜索页面下一页]" + search.encode('utf-8') + " 第" + str(page_num) + "页"
    )
    return jsonify(serachresult)


def dvrsearchsql(keyword):
    search_result = Dev_DeviceInfo.query.filter(
        (Dev_DeviceInfo.DeviceName.like("%" + keyword + "%"), "")[keyword is None] |
        (Dev_DeviceInfo.DeviceCategory.like("%" + keyword + "%"), "")[keyword is None] |
        (Dev_DeviceInfo.DeviceSN.like("%" + keyword + "%"), "")[keyword is None] |
        (Dev_DeviceInfo.DeviceID.like("%" + keyword + "%"), "")[keyword is None]
    ).order_by(Dev_DeviceInfo.ID.asc())
    return search_result


def dev_getCampus():
    campus = Dev_Campus.query.all()
    return campus

def dev_getBuild(campus):
    campus_decode = b64decode(unquote(campus)).decode('utf-8')
    result = Dev_LVRInfo.query.filter_by(
        Campus=campus_decode
    ).all()
    lvrno = []
    lvrno_result = []
    for each in result:
        lvrno.append(each.LVRNo)
    for each_lvrno in lvrno:
        name = {
            "LVRNo": each_lvrno
        }
        lvrno_result.append(name)
    return jsonify(lvrno_result)