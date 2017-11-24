# !/usr/bin/python
# -*- coding:UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username  = StringField(
        '', validators=[
            DataRequired(message= u'用户名不能为空'), Length(1, 24)], render_kw={"placeholder": u"用户名","required": False})
    password = PasswordField(
        '', validators=[
            DataRequired(message= u'密码不能为空'), Length(1, 24)], render_kw={"placeholder": u"密码"})
    submit = SubmitField(u'登录', render_kw={"style": "width:100%"})