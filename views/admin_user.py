#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/26 16:01
# @Author  : Derek.S
# @Site    : 
# @File    : admin_user.py

from flask import request, url_for, flash, abort, redirect
from models import User, Setting
from ext import db
import json
from ext import md5s
from forms import CreateUser
from log import eventlog

def admin_userindex():
    """
    用户管理
    :return:
    """
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
    eventlog("[访问用户信息页面]")
    return result


def user_per_modfiy():
    """
    用户信息修改
    :return:
    """
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
            eventlog("[用户信息修改]")
            return json.dumps(per_modfiy_status)
    except Exception as e:
        per_modfiy_status = {
            'status': 500,
            'message': 'Server Error'
        }
        return json.dumps(per_modfiy_status)


def user_delete():
    """
    删除用户
    :return:
    """
    id = request.values.get("array_id")
    try:
        for one in json.loads(id):
            user_info = User.query.filter(User.id == one)
            if user_info:
                user_info.delete()
                eventlog("[尝试删除用户] " + str(one))
        db.session.commit()
        user_del_status = {
            'status': 1,
            'message': 'success'
                    }
        eventlog("[删除用户成功]")
        return json.dumps(user_del_status)
    except Exception as e:
        user_del_status = {
            'status': 500,
            'message': 'Server Error'
        }
        return json.dumps(user_del_status)

def user_pwd_modfiy():
    """
    修改密码
    :return:
    """
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
        eventlog("[修改密码] " + str(id))
        return json.dumps(su_pwd_status)
    else:
        su_pwd_status = {
            'status': 404,
            'message': '用户未找到'
        }
        return json.dumps(su_pwd_status)


def user_create():
    """
    创建用户
    :return:
    """
    form = CreateUser()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(
                username=form.username.data
            ).first()
            pwd = request.values.get("pwd")
            if user:
                flash(u"用户名已存在，请更换用户名", "user_error")
            else:
                permissions = form.permission.data
                if permissions == 'ptman':
                    user_permission = 10
                elif permissions == 'admin':
                    user_permission = 70
                elif permissions == 'suadmin':
                    user_permission = 80
                else:
                    abort(500)
                newuser = User(
                    username=form.username.data,password=md5s(None, pwd),permissions=user_permission
                )
                db.session.add(newuser)
                db.session.commit()
                flash(u"新用户创建成功")
                eventlog("[创建用户]")
                return 0
    return form