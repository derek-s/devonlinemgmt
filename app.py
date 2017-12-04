# !/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import (Flask, render_template, redirect, url_for, request, flash)
from flask_login import login_required
from flask_bootstrap import Bootstrap

from ext import login_manager
from models import *

from views.admin import adminbg
from views.ajaxquery import ajaxquery
from views.login import loginview
from base64 import b64decode, b64encode
from urllib import unquote

SECRET_KEY = '12efc6ca97aefb8e1f6a589c6f334a405bca977bc9cec023f193ee975379e153'

app = Flask(__name__)
app.register_blueprint(adminbg)
app.register_blueprint(ajaxquery)
app.register_blueprint(loginview)

app.secret_key = SECRET_KEY
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "mysql://root:123a+-@192.168.10.105/devonlie"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    """首页函数"""
    page = request.args.get('page', 1, type=int)
    request.script_root = url_for('index', _external=True)
    count = Dev_DeviceStatus.query.count()
    pagination = Dev_DeviceStatus.query.order_by(Dev_DeviceStatus.Campus.desc()).paginate(
        page, per_page=Setting.pagination
    )
    posts = pagination.items
    campus = Dev_Campus.query.all()
    return render_template('index.html', posts=posts, count=count, pagination=pagination, campus=campus)


@app.route("/list", methods=['GET', 'POST'])
@login_required
def indexlist():
    """根据校区/楼宇进行查询"""
    page = request.args.get('page', 1, type=int)
    campusname = b64decode(request.args.get('campusname', "", type=str))
    buildname = b64decode(request.args.get('buildname', "", type=str))
    devinfo = Dev_DeviceStatus.query.filter(
        (Dev_DeviceStatus.Campus.like("%" + campusname + "%"), "")[campusname is None],
        (Dev_DeviceStatus.Location.like("%" + buildname + "%"), "")[buildname is None]
    ).order_by(Dev_DeviceStatus.Campus.desc())
    paginateion = devinfo.paginate(
        page, per_page=Setting.pagination
    )
    count = devinfo.count()
    posts = paginateion.items
    campus = Dev_Campus.query.all()
    return render_template("list.html", posts=posts, count=count, pagination=paginateion, campus=campus)


if __name__ == '__main__':
    app.run(host='127.0.0.100', port=5000, debug=True)
