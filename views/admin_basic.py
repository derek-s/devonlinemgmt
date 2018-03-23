#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/21 21:47
# @Author  : Derek.S
# @Site    : 
# @File    : admin_basic.py

from flask import Blueprint, jsonify, render_template, request, url_for, flash, session, redirect, abort
from flask_login import login_required, current_user
from decorators import admin_required
from models import Dev_Loging, Setting, Dev_Note, Dev_DeviceStatus, Dev_Campus, Dev_LVRInfo, Dev_DeviceInfo, DevDevType
from models import DevBuild
from log import eventlog
from base64 import b64decode
from urllib import unquote
from sysmanger import optionsupdate
import arrow
from ext import db
from notice import noticeindexlist
from pevent import peventsindexlist
import json


def basic_campus():
    page = request.args.get('page', 1, type=int)
    request.script_root = url_for('indexview.index', _external=True)
    count = Dev_Campus.query.count()
    pagination = Dev_Campus.query.order_by(Dev_Campus.ID.asc()).paginate(
        page, per_page=Setting().pagination
    )
    datas = pagination.items
    result = {
        'datas': datas,
        'count': count,
        'pagination': pagination
    }
    return result


def basic_campus_search():
    request.script_root = url_for('indexview.index', _external=True)
    page = request.values.get('pagenum', 1, type=int)
    word = request.values.get('keyword', "", type=str)
    search = b64decode(unquote(word)).decode('utf-8')
    select_result = Dev_Campus.query.filter(
        Dev_Campus.Campus.like("%" + search + "%")
    )
    pagination = select_result.paginate(
        page, per_page=Setting().pagination
    )
    count = select_result.count()
    posts = pagination.items
    result = {
        'posts': posts,
        'count': count,
        'pagination': pagination,
        'keyword': search
    }
    return result


def basic_campus_add():
    campusname = request.values.get("campusname")
    campus_query_count = Dev_Campus.query.filter(Dev_Campus.Campus == campusname).count()
    if campus_query_count != 0:
        campus_table_query = Dev_Campus.query.filter(Dev_Campus.Campus == campusname).one()
        campus_table_name = campus_table_query.Campus
    else:
        campus_table_name = ''
    if campus_table_name == campusname:
        campus_add_status = {
            'status': 0,
            'message': '被添加项已存在'
        }
        return json.dumps(campus_add_status)
    else:
        new_campus = Dev_Campus(campusname)
        db.session.add(new_campus)
        db.session.commit()
        campus_add_status = {
            'status': 1,
            'message': 'success'
        }
        return json.dumps(campus_add_status)


def basic_campus_modfiy():
    """
    修改校区名称
    :param id: 校区id
    :return:  修改结果
    """
    try:
        campus_id = request.values.get("id")
        campus_new = request.values.get("cname")
        campus_info = Dev_Campus.query.filter(Dev_Campus.ID == campus_id).one()
        campus_old = campus_info.Campus
        DevBuild.query.filter(DevBuild.Campus == campus_old).update({DevBuild.Campus:campus_new})
        Dev_LVRInfo.query.filter(Dev_LVRInfo.Campus == campus_old).update({Dev_LVRInfo.Campus:campus_new})
        Dev_DeviceStatus.query.filter(Dev_DeviceStatus.Campus == campus_old).update({Dev_DeviceStatus.Campus:campus_new})
        Dev_Campus.query.filter(Dev_Campus.Campus == campus_old).update({Dev_Campus.Campus:campus_new})
        db.session.commit()
        campus_modfiy_status = {
            'status': 1,
            'message': 'success'
        }
        return json.dumps(campus_modfiy_status)
    except Exception as e:
        campus_modfiy_status = {
            'status': 5,
            'message': 'Server Error'
        }
        return json.dumps(campus_modfiy_status)


def basic_campus_delete():
    delstatus = {
        'status': '',
        'message': ''
    }
    try:
        campus_id = request.values.get("array_id")
        for one in json.loads(campus_id.encode("utf-8")):
            campus_info = Dev_Campus.query.filter(
                Dev_Campus.ID == one
            )
            if campus_info:
                campus_info.delete()
        db.session.commit()
        delstatus['status'] = 1
        delstatus['message'] = "success"
        return json.dumps(delstatus)
    except Exception:
        delstatus['status'] = 500
        delstatus['message'] = "Server Error"
        return json.dumps(delstatus)


def basic_campus_layer():
    campus_list = []
    campus_info = {
        "campus_info": campus_list,
        "status": 404
    }
    try:
        campus = Dev_Campus.query.all()
        for campus_one in campus:
            campus_info_one = {
                "id": campus_one.ID,
                "campus_name": campus_one.Campus.encode("utf-8")
            }
            campus_list.append(campus_info_one)
        campus_info['status'] = 1
        return json.dumps(campus_info)
    except Exception as e:
        campus_info['status'] = 404
        return json.dumps(campus_info)