#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/14 10:33
# @Author  : Derek.S
# @Site    : 
# @File    : errorhandler.py

from flask import Blueprint, render_template, render_template_string, abort
from log import eventlog

errorview = Blueprint('errorview', __name__)


@errorview.app_errorhandler(500)
def internal_server_error(e):
    eventlog("[处理错误] " + str(e))
    return render_template('/exception/500.html'), 500


@errorview.app_errorhandler(404)
def internal_server_error(e):
    eventlog("[处理错误] " + str(e))
    return render_template('/exception/404.html'), 404


@errorview.app_errorhandler(400)
def internal_server_error(e):
    eventlog("[处理错误] " + str(e))
    return render_template('/exception/400.html'), 400
