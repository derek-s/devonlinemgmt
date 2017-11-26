# !/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import (Flask, render_template, redirect, url_for, request, flash)
from flask_login import login_required, login_user, logout_user, current_user
from flask_bootstrap import Bootstrap

from forms import LoginForm
from ext import db, login_manager
from models import *

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
ulevelinfo = ''


@app.route("/", methods=['GET', 'POST'])
@login_required
def hello():
    """测试函数"""
    devstatus = Dev_DeviceStatus.query.all()
    print User.is_admin()
    return render_template('index.html', dev_status = devstatus)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """登录函数，处理登录页面，使用login.html模板"""
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username'], password=request.form['password']).first()
        if user:
            login_user(user)
            flash("logged in!")
            ulevelinfo = str(user.userlevel)
            return redirect(url_for('hello'))
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
