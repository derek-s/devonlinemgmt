#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/12 11:01
# @Author  : Derek.S
# @Site    : 
# @File    : pevent.py

from ext import db
from models import DevPEvents


def peventsindexlist(username):
    """
    返回前台个人待办事项列表
    :return:
    """
    event = DevPEvents.query.filter(
        DevPEvents.ecreationuser == username
    ).order_by(DevPEvents.id.desc()).paginate(1, 10)
    event_items = event.items
    return event_items

