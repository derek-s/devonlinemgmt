# !/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import flash
from models import Dev_Options
from ext import db


def optionsupdate(name, value):
    """
    更新设置值
    :param name: 设置名称
    :param value:  设置值
    :return:
    """
    options = Dev_Options.query.filter_by(
        optinoname=name
    ).one()
    print options.optionvalue
    options.optionvalue = value
    try:
        db.session.commit()
        flash(u"更新完成", 'success')
    except Exception as e:
        print e
