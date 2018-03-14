# !/usr/bin/python
# -*- coding: utf-8 -*-

from flask import (render_template, request, Blueprint)
from flask_login import login_required
from models import *
from log import eventlog
from base64 import b64decode
from urllib import unquote

serachview = Blueprint('serachview', __name__)


@serachview.route("/serach", methods=['GET', 'POST'])
@login_required
def serach():
    """
    搜索页面
    :return: serach.html模板搜索页面
    """
    page = request.args.get('page', 1, type=int)
    word = request.args.get('keyword', "", type=str)
    serach = unquote(b64decode(word)).decode('utf-8')
    serp = Dev_DeviceStatus.query.filter(
        (Dev_DeviceStatus.Campus.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.Location.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.RoomNo.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HostName.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.LAA.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HigherlinkIP.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.HigherlinkPort.like("%" + serach + "%"), "")[serach is None] |
        (Dev_DeviceStatus.DeviceModel.like("%" + serach + "%"), "")[serach is None]
    ).order_by(Dev_DeviceStatus.Campus.desc())
    paginateion = serp.paginate(
        page, per_page=Setting().pagination
    )
    count = serp.count()
    posts = paginateion.items
    eventlog(
        "[搜索]" + serach.encode('utf-8') + " 第" + str(page) + "页"
    )
    return render_template(
        'serach.html', posts=posts, count=count, pagination=paginateion, keyword=serach
    )
