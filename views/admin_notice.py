#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/21 17:30
# @Author  : Derek.S
# @Site    : 
# @File    : admin_notice.py
from flask import request, flash
from models import Setting, Dev_Note
from log import eventlog
from base64 import b64decode
from urllib import unquote
import arrow
from ext import db
import json
from flask_login import current_user

def notice_create_post():
    """
    创建公告
    :return:
    """
    notename = request.form.get('notename', "默认标题")
    notecontent = request.form.get('note', None)
    createdate = arrow.now().format("YYYY-MM-DD HH:mm")
    createname = current_user.username
    note = Dev_Note(notename, notecontent, createdate, createname)
    db.session.add(note)
    db.session.commit()
    flash(u"发布成功", 'success')
    return note.id


def notice_modfiy_get(id):
    """
    修改公告
    :param id: 公告id
    :return:
    """
    eventlog("[访问修改公告页面 公告id: " + str(id) + "]")
    note = Dev_Note.query.filter(Dev_Note.id == id).one()
    notename = note.articlename
    notecontent = note.article
    result = {
        'notename': notename,
        'notecontent': notecontent
    }
    return result


def notice_modfiy_post(id):
    """
    修改公告
    :param id: 公告id
    :return:
    """
    notename = request.form.get('notename', "默认标题")
    notecontent = request.form.get('note', None)
    createdate = arrow.now().format("YYYY-MM-DD HH:mm")
    createname = current_user.username
    note = Dev_Note.query.filter(Dev_Note.id == id).one()
    note.articlename = notename
    note.article = notecontent
    note.createdate = createdate
    note.createuser = createname
    db.session.commit()
    flash(u"修改成功", 'success')
    return note.id


def notice_list():
    """
    通知公告列表
    :return:
    """
    page = request.values.get('page', 1, type=int)
    aname = request.values.get('aname', "", type=str)
    b64aname = b64decode(unquote(aname))
    cuser = request.values.get('cuser', "", type=str)
    b64cuser = b64decode(unquote(cuser))
    cdata = request.values.get('cdata', "", type=str)
    notices = Dev_Note.query.filter(
        (Dev_Note.articlename.like("%" + b64aname + "%"), "")[aname is None],
        (Dev_Note.createuser.like("%" + b64cuser + "%"), "")[cuser is None],
        (Dev_Note.createdate.like("%" + cdata + "%"), "")[cdata is None]
    )
    paginateion = notices.paginate(
        page, per_page=Setting().pagination
    )
    posts = paginateion.items
    count = notices.count()
    eventlog("[查看通知公告列表页] " + "第" + str(page) + "页")
    result = {
        'posts': posts,
        'count': count,
        'pagination': paginateion,
        'page': page
    }
    return result


def notice_delete(id):
    """
    删除公告
    :param id:
    :return:
    """
    delstatus = {
        "status": 1,
        "message": "success"
    }
    notice = Dev_Note.query.filter(
        Dev_Note.id == id
    )
    if not notice:
        delstatus['status'] = 404
        delstatus['message'] = "Not Found"
        return json.dumps(delstatus)
    notice.delete()
    db.session.commit()
    eventlog("[删除公告 公告id: " + str(id) + "]")
    return json.dumps(delstatus)

