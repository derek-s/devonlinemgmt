#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/20 17:27
# @Author  : Derek.S
# @Site    : 
# @File    : admin_lvr.py

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


def lvr_manager_index():
    request.script_root = url_for('indexview.index', _external=True)
    page = request.args.get('page', 1, type=int)
    count = Dev_LVRInfo.query.count()
    pagination = Dev_LVRInfo.query.order_by(Dev_LVRInfo.Campus.desc()).paginate(
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



def lvr_manager_ajaxquery():
    count = request.values.get('count', None, type=int)
    pagenum = request.values.get('pagenum', None, type=int)
    page_num = ((count / Setting().pagination + pagenum), 0)[count / Setting().pagination == 0]
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


def lvr_list_get():
    page = request.args.get('page', 1, type=int)
    request.script_root = url_for('indexview.index', _external=True)
    campusname = b64decode(unquote(request.args.get('campusname', "", type=str)))
    buildname = b64decode(unquote(request.args.get('buildname', "", type=str)))
    lvrinfo = lvrlistsql(campusname, buildname)
    paginateion = lvrinfo.paginate(
        page, per_page=Setting().pagination
    )
    count = lvrinfo.count()
    posts = paginateion.items
    campus = Dev_Campus.query.all()
    eventlog(
        "[后台弱电间信息 查询校区/楼宇]" + campusname + buildname + " 第" + str(page) + "页"
    )
    result = {
        'posts': posts,
        'count': count,
        'pagination': paginateion,
        'campus': campus,
        'ctitle': campusname.decode('utf-8'),
        'btitle': buildname.decode('utf-8')
    }
    return result


def lvr_list_post():
    pagenum = request.values.get('pagenum', None, type=int)
    count = request.values.get('count', None, type=int)
    campusname = unquote(request.values.get('campusname', "", type=str))
    buildname = unquote(request.values.get('buildname', "", type=str))
    lvrinfo = lvrlistsql(campusname, buildname)
    page_num = ((count / Setting().pagination + pagenum), 0)[count / Setting().pagination == 0]
    paginateion = lvrinfo.paginate(
        page_num, per_page=Setting().pagination
    )
    lvrinfolist = []
    hasnext = {
        'next': paginateion.has_next
    }

    for lvrline in paginateion.items:
        jsonlist = lvrline.to_json()
        jsonlist.update(hasnext)
        lvrinfolist.append(jsonlist)
    eventlog(
        "[ajax加载弱电间查询页面下一页]" + campusname + buildname + " 第" + str(page_num) + "页"
    )
    return jsonify(lvrinfolist)


def lvrlistsql(campusname, buildname):
    """
    校区查询SQL
    :param campusname: 校区名称
    :param buildname: 楼宇名称
    :return:
    """
    lvrinfo = Dev_LVRInfo.query.filter(
        (Dev_LVRInfo.Campus.like("%" + campusname + "%"), "")[campusname is None],
        (Dev_LVRInfo.BuildName.like("%" + buildname + "%"), "")[buildname is None]
    ).order_by(Dev_LVRInfo.Campus.desc())
    return lvrinfo


def lvr_search_get():
    request.script_root = url_for('indexview.index', _external=True)
    page = request.args.get('page', 1, type=int)
    word = request.args.get('keyword', "", type=str)
    serach = unquote(b64decode(word)).decode('utf-8')
    serp = lvrsearchsql(serach)
    pagination = serp.paginate(
        page, per_page=Setting().pagination
    )
    count = serp.count()
    posts = pagination.items
    eventlog(
        "[管理后台弱电间 搜索]" + serach.encode('utf-8') + " 第" + str(page) + "页"
    )
    result = {
        'posts': posts,
        'count': count,
        'pagination': pagination,
        'keyword': serach
    }
    return result


def lvr_search_post():
    pagenum = request.values.get('pagenum', None, type=int)
    count = request.values.get('count', None, type=int)
    word = request.values.get('keyword', None, type=str)
    search = b64decode(unquote(word)).decode('utf-8')
    serp = lvrsearchsql(search)
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


def lvrsearchsql(search):
    """
    弱电间搜索SQL
    :return:
    """
    serp = Dev_LVRInfo.query.filter(
        (Dev_LVRInfo.Campus.like("%" + search + "%"), "")[search is None] |
        (Dev_LVRInfo.BuildName.like("%" + search + "%"), "")[search is None] |
        (Dev_LVRInfo.BuildNo.like("%" + search + "%"), "")[search is None] |
        (Dev_LVRInfo.RoomNo.like("%" + search + "%"), "")[search is None] |
        (Dev_LVRInfo.LVRNo.like("%" + search + "%"), "")[search is None]
    ).order_by(Dev_LVRInfo.Campus.desc())
    return serp
