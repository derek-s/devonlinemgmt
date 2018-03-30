# !/usr/bin/python
# -*- coding:UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo
from ext import passwdcreate


class LoginForm(FlaskForm):
    username = StringField(
        '', validators=[
            DataRequired(
                message=u'用户名不能为空'), Length(4, 24)], render_kw={"placeholder": u"用户名", "required": False})
    password = PasswordField(
        '', validators=[
            DataRequired(
                message=u'密码不能为空'), Length(1, 24)], render_kw={"placeholder": u"密码"})
    submit = SubmitField(u'登录', render_kw={"style": "width:100%"})


class ChangePwd(FlaskForm):
    oldpwd = PasswordField('', validators=[
        DataRequired(message=u'旧密码不能为空'), Length(6, 24)
    ], render_kw={"placeholder": u"旧密码", "id": "oldpw"}
                           )
    newpwd = PasswordField('', validators=[
        DataRequired(message=u"新密码不能为空"),
        EqualTo('confirm', message=u"两次密码不相同"),
        Length(1, 24)], render_kw={"placeholder": u"新密码", "id": "newpw"})
    confirm = PasswordField('', None, render_kw={"placeholder": u"重复密码", "id": "confirmpw"})
    submit = SubmitField(u'修改密码', None ,render_kw={"class": "btn btn-danger changpwdb"})


class CreateUser(FlaskForm):

    username = StringField(
        u'用户名', validators=[
            DataRequired(
                message=u'用户名不能为空'
            ),Length(4,24)
        ]
    )
    password = StringField(
        u'密码',None, render_kw={
            "value": passwdcreate(),
            "readonly": "readonly"
        })
    permission = SelectField(
        u'用户权限', choices=[
            ('ptman', u'普通用户'),
            ('admin', u'管理员'),
            ('suadmin', u'超级管理员')
        ]
    )
    submit = SubmitField(u'创建新用户', None, render_kw={"class": "btn btn-danger"})