# !/usr/bin/python
# -*- coding: UTF-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from jinja2 import evalcontextfilter, environment
import hashlib

db = SQLAlchemy()
login_manager = LoginManager()


@evalcontextfilter
def md5s(self, value):
    """
    自定义jinja2 过滤器 实现md5 hash压缩
    :param self: 无
    :param value: 需压缩的值
    :return: hash后的值
    """
    hashm = hashlib.md5()
    hashm.update(value)
    return hashm.hexdigest().upper()
