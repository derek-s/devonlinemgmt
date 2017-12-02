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
    pagination = Dev_DeviceStatus.query.order_by(Dev_DeviceStatus.Campus).paginate(
        page, per_page=Setting.pagination
    )
    posts = pagination.items
    campus = Dev_Campus.query.all()
    return render_template('index.html', posts=posts, count=count, pagination=pagination, campus=campus)


if __name__ == '__main__':
    app.run(host='127.0.0.100', port=5000, debug=True)
