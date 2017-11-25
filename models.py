# !/usr/bin/python
# -*- coding:UTF-8 -*-

from ext import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """用户信息模型 登录用"""
    __tablename__ = "dev_User"
    id = db.Column("ID", db.Integer, primary_key=True)
    username = db.Column("UserName", db.String(24))
    password = db.Column("PassWord", db.String(24))
    userlevel = db.Column("UserLevel", db.String(24))

    def __init__(self, username, password, userlevel):
        self.username = username
        self.password = password
        self.userlevel = userlevel


class Dev_DeviceStatus(db.Model):
    """总表（设备情况表）数据模型"""
    __tablename__ = "dev_DeviceStatus"
    id = db.Column('ID', db.Integer, primary_key=True)
    Location = db.Column("Location", db.String(190), db.ForeignKey("dev_LVRInfo.LVRNo"))
    HostName = db.Column("HostName", db.String(255))
    LAA = db.Column("LAA", db.String(255))
    HigherlinkIP = db.Column("HigherlinkIP", db.String(255))
    HigherlinkPort = db.Column("higherlinkPort", db.String(255))
    DeviceModel = db.Column("DeviceModel", db.String(190), db.ForeignKey("dev_DeviceInfo.DeviceID"))


class Dev_DeviceInfo(db.Model):
    """设备信息表数据模型"""
    __tablename__ = "dev_DeviceInfo"
    id = db.Column("ID", db.Integer, primary_key=True)
    DeviceName = db.Column("DeviceName", db.String(255))
    DeviceCategory = db.Column("DeviceCategory", db.String(255))
    DeviceSN = db.Column("DeviceSN", db.String(255))
    DeviceCondition = db.Column("DeviceCondition", db.String(255))
    DeviceID = db.Column("DeviceID", db.String(190))
    DeviceIDs = db.relationship("Dev_DeviceStatus", backref="DeviceID", lazy="dynamic")


class Dev_LVRInfo(db.Model):
    """弱电间信息表数据模型"""
    __tablename__ = "dev_LVRInfo"
    id = db.Column("ID", db.Integer, primary_key=True)
    BulidName = db.Column("BulidName", db.String(255))
    BulidNo = db.Column("BulidNo", db.String(255))
    FloorNo = db.Column("FloorNo", db.String(255))
    RoomNo = db.Column("RoomNo", db.String(255))
    Cabinet = db.Column("Cabinet", db.String(255))
    LVRNo = db.Column("LVRNo", db.String(190))
    LVRNos = db.relationship("Dev_DevicesStatus", backref="LVRNo", lazy="dynamic")
