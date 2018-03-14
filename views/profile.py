# !/usr/bin/python
# -*- coding: utf-8 -*-

from flask import (render_template, url_for, request, flash, redirect, session, Blueprint, abort)
from flask_login import login_required

from ext import md5s
from models import Dev_Note, Dev_Loging, User, db, DevPEvents
from log import eventlog
from forms import ChangePwd
from notice import noticeindexlist
from pevent import peventsindexlist
import json
import arrow

profileview = Blueprint('profileview', __name__)


@profileview.route("/profile/<username>", methods=['GET', 'POST'])
@login_required
def userinfo(username):
    lastlogin = Dev_Loging.query.filter(
        Dev_Loging.UserName == username, Dev_Loging.Log.like("%登录成功%")).order_by(
        Dev_Loging.Date.desc()).first()
    logindate = lastlogin.Date
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
    notice = noticeindexlist()
    pevent = peventsindexlist(username)
    return render_template(
        "/user/userinfo.html", username=username, date=logindate, ip=ip, permission=per, form=form,
        note=notice, pevent=pevent
    )


@profileview.route("/profile/<username>/add", methods=['GET', 'POST'])
@login_required
def addevent(username):
    """
    添加待办事项
    :return:
    """
    if request.method == 'GET':
        return render_template("/user/addevent.html", username=username)
    elif request.method == 'POST':
        try:
            addstatus = {
                "status": 1,
                "message": "success"
            }
            eventdata = json.loads(request.get_data())
            eventdb = DevPEvents(
                eventdata['content'], eventdata['endtime'], arrow.now().format("YYYY-MM-DD"), eventdata['user']
            )
            db.session.add(eventdb)
            db.session.commit()
            return json.dumps(addstatus)
        except Exception as e:
            addstatus = {
                "status": 500,
                "message": e
            }
            return json.dumps(addstatus)


@profileview.route("/event/<id>", methods=['GET'])
@login_required
def dpevent(id):
    """
    显示待办事项
    :param id: 待办事项ID
    :return: json
    """
    try:
        event = DevPEvents.query.filter(
            DevPEvents.id == id
        ).first()
        if not event:
            abort(404)
        return render_template("/user/eventinfo.html", event=event)
    except Exception as e:
        abort(404)


@profileview.route("/event/<int:id>/delete", methods=['POST'])
@login_required
def eventdel(id):
    """
    删除待办事项
    :param id: 待办事项id
    :return:
    """

    delstatus = {
        "status": 1,
        "message": "success"
    }
    event = DevPEvents.query.filter(
        DevPEvents.id == id
    )
    if not event:
        delstatus['status'] = 404
        delstatus['message'] = "Not Found"
        return json.dumps(delstatus)
    event.delete()
    db.session.commit()
    eventlog("[删除待办事项 id: " + str(id) + "]")
    return json.dumps(delstatus)
