# !/usr/bin/python
# -*- coding: utf-8 -*-

from flask import request, flash, redirect, url_for, render_template, Blueprint, session
from flask_login import login_required, login_user, logout_user, current_user
from ext import login_manager
from forms import LoginForm
from models import User
from ext import md5s

from log import eventlog, logonlog

loginview = Blueprint("loginview", __name__)
login_manager.login_message = u"需要登录才可以查看页面"


@loginview.route("/login", methods=['GET', 'POST'])
def login():
    """登录函数，处理登录页面，使用login.html模板"""
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username'], password=md5s(None, request.form['password'])).first()
        if user:
            login_user(user)
            eventlog("[登录成功]")
            return redirect(url_for('indexview.index'))
        else:
            flash(u"登录失败!")
            logonlog(
                "",
                "[登录失败] " + str(request.form['username']) + " " + str(request.form['password'])
            )
    form = LoginForm()
    return render_template('login.html', form=form)


@loginview.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    flash(u"您已注销")
    logonlog(username, "[用户注销]" )
    return redirect(url_for('loginview.login'))


@login_manager.user_loader
def load_user(id):
    """登录user_loader回调"""
    return User.query.filter_by(id=int(id)).first()
