# !/usr/bin/python
# -*- coding:UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField(
        '', validators=[
            DataRequired(
                message=u'用户名不能为空'), Length(1, 24)], render_kw={"placeholder": u"用户名", "required": False})
    password = PasswordField(
        '', validators=[
            DataRequired(
                message=u'密码不能为空'), Length(1, 24)], render_kw={"placeholder": u"密码"})
    submit = SubmitField(u'登录', render_kw={"style": "width:100%"})


class ChangePwd(FlaskForm):
    oldpwd = PasswordField('', validators=[
        DataRequired(message=u'旧密码不能为空'), Length(1, 24)
    ], render_kw={"placeholder": u"旧密码"}
                           )
    newpwd = PasswordField('', validators=[
        DataRequired(message=u"新密码不能为空"),
        EqualTo('confirm', message=u"两次密码不相同"),
        Length(1, 24)], render_kw={"placeholder": u"新密码"})
    confirm = PasswordField('', None, render_kw={"placeholder": u"重复密码"})
    submit = SubmitField(u'修改密码', None ,render_kw={"class": "btn btn-danger changpwdb"})