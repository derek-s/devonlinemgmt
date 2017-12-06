# !/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template
from flask_login import login_required
from decorators import admin_required

adminbg = Blueprint('adminbg', __name__)


@adminbg.route("/admin")
@login_required
@admin_required
def admin():
    """管理后台"""
    return render_template('/admin/admin.html')
