# !/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Blueprint, jsonify, request
from flask_login import login_required
from models import Dev_DeviceStatus, Dev_LVRInfo, Dev_Campus, Dev_DeviceInfo, Setting
from urllib import unquote
from base64 import b64decode, b64encode

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
    devinfo = Dev_DeviceStatus.query.order_by(Dev_DeviceStatus.Campus.desc()).paginate(
        (
            ((count/Setting.pagination+pagenum), 0)[count/Setting.pagination == 0]
        ), per_page=Setting.pagination
    )
    devinfotemp = []
    hasnext = {
        'next': devinfo.has_next
    }

    for devx in devinfo.items:
        jsonlist = devx.to_json()
        jsonlist.update(hasnext)
        devinfotemp.append(jsonlist)
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


@ajaxquery.route("/_querydevinfo", methods=['POST'])
@login_required
def qudevinfo():
    """
    设备情况信息表查询
    :return: json
    """
    word = request.values.get('keyword', None, type=str)
    serach = unquote(word).decode('utf-8')
    serptemp = []
    serp = Dev_DeviceStatus.query.filter(
        (Dev_DeviceStatus.Location.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HostName.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.LAA.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HigherlinkIP.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HigherlinkPort.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.DeviceModel.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.DeviceModel.like("%" + serach + "%"), "")[serach is None]
    ).all()
    for serpx in serp:
        serptemp.append(serpx.to_json())
    return jsonify(serptemp)


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
        Campus=campus, BuildName=location, RoomNo=roomno
    ).all()
    for serpx in serp:
        serptemp.append(serpx.to_json())
    return jsonify(serptemp)


@ajaxquery.route("/_querydev", methods=['POST'])
@login_required
def querydev():
    """
    弱电间信息表查询
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
    paginateion = devinfo.paginate(
        ((count / Setting.pagination + pagenum), 0)[count / Setting.pagination == 0], per_page=Setting.pagination
    )
    devinfotest = []
    hasnext = {
        'next': paginateion.has_next
    }

    for devx in paginateion.items:
        jsonlist = devx.to_json()
        jsonlist.update(hasnext)
        devinfotest.append(jsonlist)

    return jsonify(devinfotest)
