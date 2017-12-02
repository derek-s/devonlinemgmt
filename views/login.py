# !/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import request, flash, redirect, url_for, render_template, Blueprint
from flask_login import login_required, login_user, logout_user
from ext import login_manager
from forms import LoginForm
from models import User

loginview = Blueprint("loginview", __name__)


@loginview.route("/login", methods=['GET', 'POST'])
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


@loginview.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have logout!')
    return redirect(url_for('loginview.login'))


@login_manager.user_loader
def load_user(id):
    """登录user_loader回调"""
    return User.query.filter_by(id=int(id)).first()