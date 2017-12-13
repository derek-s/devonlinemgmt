# !/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, request, url_for
from flask_login import login_required
from decorators import admin_required
from models import Dev_Loging, Setting
from log import eventlog

adminbg = Blueprint('adminbg', __name__)


@adminbg.route("/admin")
@login_required
@admin_required
def admin():
    """
    管理后台视图
    :return: 返回管理页面
    """
    return render_template('/admin/admin.html')


@adminbg.route("/admin/query")
@login_required
@admin_required
def query():
    """
    数据查询视图
    :return: 返回数据查询结果并构建相应页面
    """
    return render_template('/admin/dbquery.html')


@adminbg.route("/admin/lvrmanage")
@login_required
@admin_required
def lvrmanager():
    """
    弱电间管理视图
    :return: 返回数据查询结果并构建相应页面
    """
    return render_template('/admin/lvrmanager.html')


@adminbg.route("/admin/dvrmanage")
@login_required
@admin_required
def dvrmanage():
    """
    :return: 返回数据查询结果并构建相应页面
    """
    return render_template('/admin/dvrmanage.html')


@adminbg.route("/admin/dvrstatus")
@login_required
@admin_required
def dvrstatus():
    """
    :return: 返回数据查询结果并构建相应页面
    """
    return render_template('/admin/dvrstatus.html')


@adminbg.route("/admin/basicinfo")
@login_required
@admin_required
def basicinfo():
    """
    :return: 返回数据查询结果并构建相应页面
    """
    return render_template('/admin/basicinfo.html')


@adminbg.route("/admin/usrmanage")
@login_required
@admin_required
def usrmanage():
    """
    :return: 返回数据查询结果并构建相应页面
    """
    return render_template('/admin/usrmanage.html')


@adminbg.route("/admin/sysmanage")
@login_required
@admin_required
def sysmanage():
    """
    :return: 返回数据查询结果并构建相应页面
    """
    return render_template('/admin/sysmanage.html')


@adminbg.route("/admin/log", methods=['GET', 'POST'])
@login_required
@admin_required
def logviews():
    """
    :return: 返回数据查询结果并构建相应页面
    """
    page = request.args.get('page', 1, type=int)
    logdata = Dev_Loging.query.filter()
    paginateion = logdata.paginate(
        page, per_page=Setting.pagination
    )
    posts = paginateion.items
    count = logdata.count()
    eventlog("[查看日志]" + " 第" + str(page) +"页")
    return render_template('/admin/log.html', posts=posts, count=count, pagination=paginateion)
