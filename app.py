# !/usr/bin/python
# -*- coding: utf-8 -*-

from flask import (Flask, render_template, url_for, request, )
from flask_login import login_required, current_user
from flask_bootstrap import Bootstrap

from ext import login_manager
from models import *
from log import eventlog
from views.admin import adminbg
from views.ajaxquery import ajaxquery
from views.login import loginview
from base64 import b64decode, b64encode
from urllib import unquote

SECRET_KEY = '12efc6ca97aefb8e1f6a589c6f334a405bca977bc9cec023f193ee975379e153'

app = Flask(__name__, template_folder="templates")
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
login_manager.login_view = "loginview.login"
login_manager.login_message = u"需要登录才可以查看页面"


@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    """首页函数"""
    eventlog(
        "[访问首页]"
    )
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
    campusname = b64decode(unquote(request.args.get('campusname', "", type=str)))
    buildname = b64decode(unquote(request.args.get('buildname', "", type=str)))
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
    eventlog(
        "[查询校区/楼宇]" + campusname + buildname + " 第" + str(page) + "页"
    )
    return render_template(
        "list.html", posts=posts, count=count, pagination=paginateion, campus=campus,
        ctitle=campusname.decode('utf-8'), btitle=buildname.decode('utf-8')
    )


@app.route("/serach", methods=['GET', 'POST'])
@login_required
def serach():
    """
    搜索页面
    :return: serach.html模板搜索页面
    """
    page = request.args.get('page', 1, type=int)
    word = request.args.get('keyword', "", type=str)
    serach = unquote(b64decode(word)).decode('utf-8')
    serp = Dev_DeviceStatus.query.filter(
        (Dev_DeviceStatus.Campus.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.Location.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.RoomNo.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HostName.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.LAA.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HigherlinkIP.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HigherlinkPort.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.DeviceModel.like("%" + serach + "%"), "")[serach is None]
    ).order_by(Dev_DeviceStatus.Campus.desc())
    paginateion = serp.paginate(
        page, per_page=Setting.pagination
    )
    count = serp.count()
    posts = paginateion.items
    eventlog(
        "[搜索]" + serach.encode('utf-8') + " 第" + str(page) + "页"
    )
    return render_template(
        'serach.html', posts=posts, count=count, pagination=paginateion, keyword=serach
    )


@app.route("/profile/<username>")
@login_required
def userinfo(username):
    return render_template("/user/userinfo.html")


if __name__ == '__main__':
    app.run(host='127.0.0.100', port=5000, debug=True)
