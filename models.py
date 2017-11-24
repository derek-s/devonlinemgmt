# !/usr/bin/python
# -*- coding:UTF-8 -*-

from ext import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "dev_User"
    id = db.Column('ID', db.Integer, primary_key=True)
    username = db.Column('UserName', db.String(24))
    password = db.Column('PassWord', db.String(24))
    userlevel = db.Column('UserLevel', db.String(24))

    def __init__(self, username, password, userlevel):
        self.username = username
        self.password = password
        self.userlevel = userlevel