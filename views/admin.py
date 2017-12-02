# !/usr/bin/python
# -*- coding: UTF-8 -*-
from app import app
from decorators import admin_required
from flask_login import login_required
from flask import render_template


@app.route("/admin")
@login_required
@admin_required
def admin():
    """管理后台"""
    return render_template('admin.html')
