# !/usr/bin/python
# -*- coding:UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username  = StringField('username', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField('password', validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField('login')