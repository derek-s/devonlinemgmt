# !/usr/bin/python
# -*- coding:UTF-8 -*-

from ext import db
from flask_login import UserMixin


class Permission:
    """用户权限常量"""
    domestic = 10
    administer = 70
    suadminister = 80


class User(UserMixin, db.Model):
    """用户信息模型"""
    __tablename__ = "dev_User"
    id = db.Column("ID", db.Integer, primary_key=True)
    username = db.Column("UserName", db.String(24))
    password = db.Column("PassWord", db.String(24))
    permissions = db.Column("Permissions", db.Integer)

    def can(self, permissions):
        return (self.permissions & Permission.administer) >= 64

    def cansu(self, permissions):
        return (self.permissions & Permission.suadminister) == 80

    def is_administrator(self):
        return self.can(self.permissions)

    def is_suadmin(self):
        return self.cansu(self.permissions)



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

    def __init__(self, Campus, Location, RoomNo, HostName, LAA, HigherlinkIP, HigherlinkPort, DeviceModel):
        self.Campus = Campus,
        self.Location = Location,
        self.RoomNo = RoomNo,
        self.HostName = HostName,
        self.LAA = LAA,
        self.HigherlinkIP = HigherlinkIP,
        self.HigherlinkPort = HigherlinkPort,
        self.DeviceModel = DeviceModel

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

    def __init__(self, DeviceName, DeviceCategory, DeviceSN, DeveiceCondition, DeviceID):
        self.DeviceName = DeviceName,
        self.DeviceCategory = DeviceCategory,
        self.DeviceCondition = DeveiceCondition,
        self.DeviceSN = DeviceSN,
        self.DeviceID = DeviceID

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
            'Cabinet': self.Cabinet,
            'LVRNo': self.LVRNo
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

    def __init__(self, Campus):
        self.Campus = Campus

class Dev_Loging(db.Model):
    __tablename__ = "dev_Loging"
    ID = db.Column("ID", db.Integer, primary_key=True)
    Date = db.Column("Date", db.String(255))
    UserName = db.Column("UserName", db.String(255))
    IP = db.Column("IP", db.String(255))
    Log = db.Column("Log", db.Text)

    def __init__(self, date, username, ip, log):
        self.Date = date
        self.UserName = username
        self.Log = log
        self.IP = ip

    def to_json(self):
        return{
            'ID': self.ID,
            'Date': self.Date,
            'UserName': self.UserName,
            'Log': self.Log,
            'IP': self.IP
        }


class Dev_Options(db.Model):
    """
    系统设置模型
    """
    __tablename__ = "dev_Options"
    ID = db.Column("ID", db.Integer, primary_key=True)
    optinoname = db.Column("option_name", db.String(255))
    optionvalue = db.Column("option_value", db.String(255))

    def __init__(self, id, optionname, optionvalue):
        self.id = id
        self.optionname = optionname
        self.optionvalue = optionvalue


class Setting():
    """设置信息"""
    def __init__(self):
        pagen = Dev_Options.query.filter_by(optinoname='pagination').one()
        self.pagination = int(pagen.optionvalue)
        page_index = Dev_Options.query.filter_by(optinoname='pagination_index').one()
        self.page_index = int(page_index.optionvalue)
    """
     pagination = 2
    """


class Dev_Note(db.Model):
    """
    通知公告模型
    """
    __tablename__ = "dev_Notice"
    id = db.Column("ID", db.Integer, primary_key=True)
    articlename = db.Column("ArticleName", db.Text)
    article = db.Column("Article", db.Text)
    createdate = db.Column("CreateDate", db.String(255))
    createuser = db.Column("CreateUser", db.String(255))

    def __init__(self, articlename, article, createdate, createuser):
        self.article = article
        self.articlename = articlename
        self.createdate = createdate
        self.createuser = createuser

    def to_json(self):
        return {
            'articlename': self.articlename,
            'createuser': self.createuser,
            'createdate': self.createdate,
            'article': self.article
        }


class DevPEvents(db.Model):
    """
    待办事件模型
    """
    __tablename__ = "dev_PersonEvent"
    id = db.Column("ID", db.Integer, primary_key=True)
    eventname = db.Column("EventName", db.Text)
    eventtime = db.Column("EventTime", db.Text)
    ecreationdate = db.Column("ECreationDate", db.Text)
    ecreationuser = db.Column("ECreationUser", db.Text)

    def __init__(self, eventname, eventtime, ecreationdate, ecreationuser):
        self.eventtime = eventtime
        self.eventname = eventname
        self.ecreationdate = ecreationdate
        self.ecreationuser = ecreationuser


class DevBuild(db.Model):
    """
    楼宇信息模型
    """
    __tablename__ = "dev_Build"
    ID = db.Column("ID", db.Integer, primary_key=True)
    Campus = db.Column("Campus", db.Text)
    BuildName = db.Column("BuildName", db.Text)

    def __init__(self, Campus, BuildName):
        self.Campus = Campus
        self.BuildName = BuildName

class DevDevType(db.Model):
    """
    设备类型模型
    """
    __tablename__ = "dev_DevType"
    ID = db.Column("ID", db.Integer, primary_key=True)
    Type = db.Column("Type", db.Text)

    def __init__(self, Type):
        self.Type = Type
