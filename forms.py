# !/usr/bin/python
# -*- coding:UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username  = StringField(u'用户名', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField(u'密码', validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField(u'登录')