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