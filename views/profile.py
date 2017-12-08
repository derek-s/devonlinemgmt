# !/usr/bin/python
# -*- coding: utf-8 -*-

from flask import (render_template, url_for, request, flash, redirect, session, Blueprint)
from flask_login import login_required

from ext import md5s
from models import *
from log import eventlog
from forms import ChangePwd

profileview = Blueprint('profileview', __name__)


@profileview.route("/profile/<username>", methods=['GET', 'POST'])
@login_required
def userinfo(username):
    lastlogin = Dev_Loging.query.filter(
        Dev_Loging.UserName == username, Dev_Loging.Log.like("%登录成功%")).order_by(
        Dev_Loging.Date.desc()).first()
    date = lastlogin.Date
    ip = lastlogin.IP
    userdb = User.query.filter(User.username == username).first()
    permission = userdb.permissions
    if permission == 80:
        per = u"超级管理员"
    elif permission == 70:
        per = u"管理员"
    elif permission == 10:
        per = u"普通用户"
    else:
        per = u"非法用户"
    form = ChangePwd()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(
                username=username, password=md5s(None, form.oldpwd.data)
            ).first()
            if user:
                newpwd = form.newpwd.data
                user.password = md5s(None, newpwd)
                db.session.commit()
                session.pop('_flashes', None)
                flash(u"密码修改成功，请重新登陆。")
                eventlog(u"[修改密码成功] 跳转到登陆页面")
                return redirect(url_for('loginview.login'))
            else:
                session.pop('_flashes', None)
                flash(u"旧密码错误")
                eventlog(u"[修改密码失败] 旧密码验证失败")
    eventlog(u"[访问个人资料页面]" + username)
    return render_template("/user/userinfo.html", username=username, date=date, ip=ip, permission=per, form=form)