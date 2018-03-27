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

def admin_userindex():
    page = request.args.get('page', 1 ,type=int)
    request.script_root = url_for('indexview.index', _external=True)
    count = User.query.count()
    pagination = User.query.order_by(User.id.asc()).paginate(
        page, per_page=Setting().pagination
    )
    posts = pagination.items
    result = {
        'posts': posts,
        'count': count,
        'pagination': pagination
    }
    return result