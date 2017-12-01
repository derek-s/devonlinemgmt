# !/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import (Flask, render_template, redirect, url_for, request, flash, jsonify)
from flask_login import login_required, login_user, logout_user, current_user
from flask_bootstrap import Bootstrap
from urllib import unquote

from forms import LoginForm
from ext import db, login_manager
from models import *
from decorators import permission_required, admin_required

SECRET_KEY = '12efc6ca97aefb8e1f6a589c6f334a405bca977bc9cec023f193ee975379e153'

app = Flask(__name__)

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
    pagination = Dev_DeviceStatus.query.order_by(Dev_DeviceStatus.ID).paginate(
        page, per_page=Setting.pagination
    )
    posts = pagination.items
    return render_template('index.html', posts=posts, count=count, pagination=pagination)


@app.route("/admin")
@login_required
@admin_required
def admin():
    """管理后台"""
    return render_template('admin.html')


@app.route("/list")
@login_required
def list():
    """设备情况全表函数"""
    count = request.args.get('count', None, type=int)
    devinfo = Dev_DeviceStatus.query.order_by(Dev_DeviceStatus.ID).paginate(
        count, per_page=Setting.pagination
    )
    devinfotemp = []

    for devx in devinfo.items:
        devinfotemp.append(devx.to_json())
    return jsonify(devinfotemp)


@app.route("/_querydevinfo")
@login_required
def qudevinfo():
    """设备情况信息表查询函数"""
    word = request.args.get('keyword', None, type=str)
    serach = unquote(word).decode('utf-8')
    serptemp = []
    serp = Dev_DeviceStatus.query.filter(
        (Dev_DeviceStatus.Location.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HostName.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.LAA.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HigherlinkIP.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HigherlinkPort.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.DeviceModel.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.DeviceModel.like("%" + serach + "%"), "")[serach is None]
    ).all()
    for serpx in serp:
        serptemp.append(serpx.to_json())
    return jsonify(serptemp)


@app.route("/_querylvr")
@login_required
def querylvr():
    """弱电间信息表查询函数"""
    word = request.args.get('keyword', None, type=str)
    serach = unquote(word).decode('utf-8')
    serptemp = []
    serp = Dev_LVRInfo.query.filter(
        (Dev_LVRInfo.BuildName.like("%" + serach + "%"), "")[serach is None] |
        (Dev_LVRInfo.BuildNo.like("%" + serach + "%"), "")[serach is None] |
        (Dev_LVRInfo.FloorNo.like("%" + serach + "%"), "")[serach is None] |
        (Dev_LVRInfo.RoomNo.like("%" + serach + "%"), "")[serach is None]
    ).all()
    for serpx in serp:
        serptemp.append(serpx.to_json())
    return jsonify(serptemp)


@app.route("/_querydev")
@login_required
def querydev():
    """弱电间信息表查询函数"""
    word = request.args.get('keyword', None, type=str)
    serach = unquote(word).decode('utf-8')
    serptemp = []
    serp = Dev_DeviceInfo.query.filter(
        (Dev_DeviceInfo.DeviceName.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceInfo.DeviceCategory.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceInfo.DeviceSN.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceInfo.DeviceCondition.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceInfo.DeviceID.like("%" + serach + "%"), "")[serach is None]
    ).all()
    for serpx in serp:
        serptemp.append(serpx.to_json())
    return jsonify(serptemp)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """登录函数，处理登录页面，使用login.html模板"""
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username'], password=request.form['password']).first()
        if user:
            login_user(user)
            flash("logged in!")
            return redirect(url_for('index'))
        else:
            flash("logged filed")
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have logout!')
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(id):
    """登录user_loader回调"""
    return User.query.filter_by(id=int(id)).first()


if __name__ == '__main__':
    app.run(host='127.0.0.100', port=5000, debug=True)
