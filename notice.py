#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ext import db
from models import Dev_Note


def noticeindexlist():
    """
    返回前台通知公告列表
    :return:
    """
    note = Dev_Note.query.order_by(Dev_Note.id.desc()).paginate(1, 10)
    notice = note.items
    return notice
