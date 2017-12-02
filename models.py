# !/usr/bin/python
# -*- coding:UTF-8 -*-

from ext import db
from flask_login import UserMixin


class Setting:
    """设置信息"""
    pagination = 2


class Permission:
    """用户权限常量"""
    domestic = 10
    administer = 80


class User(UserMixin, db.Model):
    """用户信息模型 登录用"""
    __tablename__ = "dev_User"
    id = db.Column("ID", db.Integer, primary_key=True)
    username = db.Column("UserName", db.String(24))
    password = db.Column("PassWord", db.String(24))
    permissions = db.Column("Permissions", db.Integer)

    def can(self, permissions):
        return (self.permissions & Permission.administer) == permissions

    def is_administrator(self):
        return self.can(self.permissions)

    def __init__(self, username, password, permissions):
        self.username = username
        self.password = password
        self.permissions = permissions


class Dev_DeviceStatus(db.Model):
    """设备情况表数据模型"""
    __tablename__ = "dev_DeviceStatus"
    ID = db.Column('ID', db.Integer, primary_key=True)
    Campus = db.Column('Campus', db.String(255))
    Location = db.Column("Location", db.String(190))
    RoomNo = db.Column("RoomNo", db.String(255))
    HostName = db.Column("HostName", db.String(255))
    LAA = db.Column("LAA", db.String(255))
    HigherlinkIP = db.Column("HigherlinkIP", db.String(255))
    HigherlinkPort = db.Column("higherlinkPort", db.String(255))
    DeviceModel = db.Column("DeviceModel", db.String(190))

    def to_json(self):
        """将查询数据转为json"""
        return {
            'ID': self.ID,
            'Campus': self.Campus,
            'Location': self.Location,
            'RoomNo': self.RoomNo,
            'HostName': self.HostName,
            'LAA': self.LAA,
            'HigherlinkIP': self.HigherlinkIP,
            'HigherlinkPort': self.HigherlinkPort,
            'DeviceModel': self.DeviceModel
        }


class Dev_DeviceInfo(db.Model):
    """设备信息表数据模型"""
    __tablename__ = "dev_DeviceInfo"
    ID = db.Column("ID", db.Integer, primary_key=True)
    DeviceName = db.Column("DeviceName", db.String(255))
    DeviceCategory = db.Column("DeviceCategory", db.String(255))
    DeviceSN = db.Column("DeviceSN", db.String(255))
    DeviceCondition = db.Column("DeviceCondition", db.String(255))
    DeviceID = db.Column("DeviceID", db.String(190), index=True)

    def to_json(self):
        """将查询数据转为json"""
        return {
            'ID': self.ID,
            'DeviceName': self.DeviceName,
            'DeviceCategory': self.DeviceCategory,
            'DeviceSN': self.DeviceSN,
            'DeviceCondition': self.DeviceCondition,
            'DeviceID': self.DeviceID
        }


class Dev_LVRInfo(db.Model):
    """弱电间信息表数据模型"""
    __tablename__ = "dev_LVRInfo"
    ID = db.Column("ID", db.Integer, primary_key=True)
    Campus= db.Column("Campus", db.String(255))
    BuildName = db.Column("BuildName", db.String(255))
    BuildNo = db.Column("BuildNo", db.String(255))
    FloorNo = db.Column("FloorNo", db.String(255))
    RoomNo = db.Column("RoomNo", db.String(255))
    Cabinet = db.Column("Cabinet", db.String(255))
    LVRNo = db.Column("LVRNo", db.String(190), index=True)

    def to_json(self):
        """将查询数据转为json"""
        return {
            'ID': self.ID,
            'Campus': self.Campus,
            'BuildName': self.BuildName,
            'BuildNo': self.BuildNo,
            'FloorNo': self.FloorNo,
            'RoomNo': self.RoomNo,
            'Cabinet': self.Cabinet
        }

    def bn_to_json(self):
        return {
            'BuildName': self.BuildName
        }


class Dev_Campus(db.Model):
    """校区信息表模型"""
    __tablename__ = "dev_Campus"
    ID = db.Column("ID", db.Integer, primary_key=True)
    Campus = db.Column("Campus", db.String(255))