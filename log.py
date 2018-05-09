#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import request
from flask_login import current_user
import arrow
from models import Dev_Loging
from ext import db
import json

def eventlog(log):
    """
    操作日志写入数据库
    :param log: 操作内容
    :return: 无
    """
    date = arrow.now().format("YYYY-MM-DD HH:mm")
    try:
        username = current_user.username
        ip = request.remote_addr
        loginfo = Dev_Loging(date, username, ip, log)
        db.session.add(loginfo)
        db.session.commit()
    except Exception as e:
        pass


def logonlog(username, log):
    """
    登录日志
    :param username: 用户名
    :param log: 日志内容
    :return: 无
    """
    date = arrow.now().format("YYYY-MM-DD HH:mm")
    username = username
    ip = request.remote_addr
    loginfo = Dev_Loging(date, username, ip, log)
    db.session.add(loginfo)
    db.session.commit()

def emptylog():
    """
    清空日志
    :return: 返回操作状态
    """
    try:
        Dev_Loging.query.delete()
        emptylog_status = {
            'status': 200,
            'message': 'Operation Complete'
        }
        db.session.commit()
        eventlog("[清空日志表]")
    except:
        emptylog_status = {
            'status': 500,
            'message': 'Server Error'
        }
    return json.dumps(emptylog_status)