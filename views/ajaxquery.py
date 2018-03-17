# !/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Blueprint, jsonify, request
from flask_login import login_required
from models import Dev_DeviceStatus, Dev_LVRInfo, Dev_Campus, Dev_DeviceInfo, Setting
from urllib import unquote
from base64 import b64decode, b64encode
from log import eventlog

ajaxquery = Blueprint("ajaxquery", __name__)


@ajaxquery.route("/_queryipage", methods=['POST'])
@login_required
def _queryipage():
    """
    ajax下一页加载
    :return: json
    """
    count = request.values.get('count', None, type=int)
    pagenum = request.values.get('pagenum', None, type=int)
    page_num = ((count/Setting().pagination+pagenum), 0)[count/Setting().pagination == 0]
    devinfo = Dev_DeviceStatus.query.order_by(Dev_DeviceStatus.Campus.desc()).paginate(
        (
            page_num
        ), per_page=Setting().pagination
    )
    devinfotemp = []
    hasnext = {
        'next': devinfo.has_next
    }

    for devx in devinfo.items:
        jsonlist = devx.to_json()
        jsonlist.update(hasnext)
        devinfotemp.append(jsonlist)
    eventlog(
        "[ajax首页加载下一页]" + " 第" + str(page_num) + "页"
    )
    return jsonify(devinfotemp)


@ajaxquery.route("/_querybuild", methods=['POST'])
@login_required
def _querybuild():
    """
    ajax加载前台查询下拉列表数据
    :return: json
    """
    campusurl = request.values.get('campusname', None, type=str)
    campusname = unquote(campusurl).decode('utf-8')
    bntemp = []
    settemp = []
    for bnlist in Dev_DeviceStatus.query.filter(
            (Dev_DeviceStatus.Campus.like("%" + campusname + "%"), "")[campusname is None]
    ).with_entities(Dev_DeviceStatus.Location):
        for bname in bnlist:
            settemp.append(bname)
    setlist = set(settemp)
    for bsname in setlist:
        name = {
            'BuildName': bsname
        }
        bntemp.append(name)
    return jsonify(bntemp)


@ajaxquery.route("/_querylvr", methods=['POST'])
@login_required
def querylvr():
    """
    弱电间信息表查询
    :return: json
    """
    recampus = request.values.get('campus', None, type=str)
    campus = unquote(recampus).decode('utf-8')
    relocation = request.values.get('location', None, type=str)
    location = unquote(relocation).decode('utf-8')
    reroomno = request.values.get('roomno',None,type=str)
    roomno = unquote(reroomno).decode('utf-8')
    serptemp = []
    serp = Dev_LVRInfo.query.filter_by(
        Campus=campus, BuildName=location, LVRNo=roomno
    ).all()
    for serpx in serp:
        serptemp.append(serpx.to_json())
    eventlog(
        "[查看弱电间信息]" + campus.encode('utf-8') + location.encode('utf-8') + str(roomno)
    )
    return jsonify(serptemp)


@ajaxquery.route("/_querydev", methods=['POST'])
@login_required
def querydev():
    """
    设备信息表查询
    :return: json
    """
    word = request.values.get('keyword', None, type=str)
    serach = unquote(word).decode('utf-8')
    serptemp = []
    serp = Dev_DeviceInfo.query.filter(
        (Dev_DeviceInfo.DeviceName.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceInfo.DeviceCategory.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceInfo.DeviceSN.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceInfo.DeviceCondition.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceInfo.DeviceID.like("%" + serach + "%"), "")[serach is None]
    ).all()
    for serpx in serp:
        serptemp.append(serpx.to_json())
    eventlog(
        "[查看设备信息]" + serach.encode('utf-8')
    )
    return jsonify(serptemp)


@ajaxquery.route("/_qindexlist", methods=['POST'])
@login_required
def queryilist():
    """
    按校区查询页面ajax加载
    :return:
    """
    pagenum = request.values.get('pagenum', None, type=int)
    count = request.values.get('count', None, type=int)
    campusname = unquote(request.values.get('campusname', "", type=str))
    buildname = unquote(request.values.get('buildname', "", type=str))
    devinfo = Dev_DeviceStatus.query.filter(
        (Dev_DeviceStatus.Campus.like("%" + campusname + "%"), "")[campusname is None],
        (Dev_DeviceStatus.Location.like("%" + buildname + "%"), "")[buildname is None]
    ).order_by(Dev_DeviceStatus.Campus.desc())
    page_num = ((count / Setting().pagination + pagenum), 0)[count / Setting().pagination == 0]
    paginateion = devinfo.paginate(
        page_num, per_page=Setting().pagination
    )
    devinfotest = []
    hasnext = {
        'next': paginateion.has_next
    }

    for devx in paginateion.items:
        jsonlist = devx.to_json()
        jsonlist.update(hasnext)
        devinfotest.append(jsonlist)
    eventlog(
        "[ajax加载校区查询页面下一页]" + campusname + buildname + " 第" + str(page_num) + "页"
    )
    return jsonify(devinfotest)


@ajaxquery.route("/_qserach", methods=['POST'])
@login_required
def queryserach():
    """
    搜索页面ajax加载
    :return: json
    """
    pagenum = request.values.get('pagenum', None, type=int)
    count = request.values.get('count', None, type=int)
    word = request.values.get('keyword', '123', type=str)
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
    page_num = ((count / Setting().pagination + pagenum), 0)[count / Setting().pagination == 0]
    paginateion = serp.paginate(
        page_num , per_page=Setting().pagination
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
        "[ajax加载搜索页面下一页]" + serach.encode('utf-8') + " 第" + str(page_num) + "页"
    )
    return jsonify(serachresult)
