#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/26 16:01
# @Author  : Derek.S
# @Site    : 
# @File    : admin_user.py

from flask import request, url_for
from models import User, Setting
from models import DevBuild
from base64 import b64decode
from urllib import unquote
from ext import db
import json
import hashlib
import string
import random
from ext import md5s

def admin_userindex():
    page = request.args.get('page', 1 ,type=int)
    ulevel = request.args.get('level', "", type=str)
    if ulevel == "all":
        upkey = ""
    elif ulevel == "su":
        upkey = 80
    elif ulevel == "admin":
        upkey = 70
    elif ulevel == "ordman":
        upkey = 10
    else:
        upkey = ""
    request.script_root = url_for('indexview.index', _external=True)
    if upkey == "":
        pagination = User.query.order_by(User.id.asc()).paginate(
            page, per_page=Setting().pagination
        )
        count = User.query.count()
    else:
        pagination = User.query.filter(
            User.permissions == upkey
        ).order_by(User.id.asc()).paginate(
            page, per_page=Setting().pagination
        )
        count = User.query.filter(
            User.permissions == upkey
        ).count()
    posts = pagination.items
    suadmin_count = User.query.filter(User.permissions == 80).count()
    admin_count = User.query.filter(User.permissions == 70).count()
    ord_count = User.query.filter(User.permissions == 10).count()
    result = {
        'posts': posts,
        'count': count,
        'pagination': pagination,
        'all_count': count,
        'suadmin_count': suadmin_count,
        'admin_count': admin_count,
        'user_count': ord_count
    }
    return result


def user_per_modfiy():
    id = request.values.get('id', -1, type=int)
    new_perm = request.values.get('newperm')
    try:
        user_info = User.query.filter(User.id == id).one()
        if user_info:
            if new_perm == "suamdin":
                User.query.filter(User.id == id).update({User.permissions: 80})
            elif new_perm == "admin":
                User.query.filter(User.id == id).update({User.permissions: 70})
            elif new_perm == "ptman":
                User.query.filter(User.id == id).update({User.permissions: 10})
            else:
                per_modfiy_status = {
                    'status': 500,
                    'message': 'Server Error'
                }
                return json.dumps(per_modfiy_status)
            db.session.commit()
            per_modfiy_status = {
                'status': 1,
                'message': 'success'
            }
            return json.dumps(per_modfiy_status)
    except Exception as e:
        per_modfiy_status = {
            'status': 500,
            'message': 'Server Error'
        }
        return json.dumps(per_modfiy_status)


def user_delete():
    id = request.values.get('id', -1, type=int)
    try:
        user_info = User.query.filter(User.id == id)
        if user_info:
            user_info.delete()
            db.session.commit()
            user_del_status = {
                'status': 1,
                'message': 'success'
                }
            return json.dumps(user_del_status)
        else:
            user_del_status = {
                'status': 404,
                'message': '没有这个用户'
            }
            return json.dumps(user_del_status)
    except Exception as e:
        user_del_status = {
            'status': 500,
            'message': 'Server Error'
        }
        return json.dumps(user_del_status)

def user_pwd_modfiy():
    id = request.values.get("id", type=int)
    pwd = request.values.get("pwd", type=str)
    user_info = User.query.filter(User.id == id).first()
    if user_info:
        new_pwd = md5s(None, pwd)
        user_info.password = new_pwd
        db.session.commit()
        su_pwd_status = {
            'status': 1,
            'message': 'success'
        }
        return json.dumps(su_pwd_status)
    else:
        su_pwd_status = {
            'status': 404,
            'message': '用户未找到'
        }
        return json.dumps(su_pwd_status)


def user_create():
    pass