# !/usr/bin/python
# -*- coding:UTF-8 -*-

from ext import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "dev_User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.string(24), nullable=False)
    password = db.Column(db.string(24), nullable=False)
    userlevel = db.Column(db.string(24), nullabe=False)

    def __init__(self, username, password, userlevel):
        self.username = username
        self.password = password
        self.userlevel = userlevel