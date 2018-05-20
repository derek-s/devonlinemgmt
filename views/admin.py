# !/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, request, url_for, flash, session, redirect, abort
from flask_login import login_required, current_user
from decorators import admin_required
from models import Dev_Loging, Setting
from log import eventlog, emptylog
from base64 import b64decode
from urllib import unquote
from sysmanger import optionsupdate
from notice import noticeindexlist
from pevent import peventsindexlist
from ext import passwdcreate

from .admin_dbquery import admin_query, admin_query_list, admin_query_serach
from .admin_lvr import  lvr_manager_index, lvr_manager_ajaxquery
from .admin_lvr import lvr_list_get, lvr_list_post, lvr_search_get, lvr_search_post
from .admin_dvr import dvr_manage_get, dvr_manage_post, dvr_list_get, dvr_list_post
from .admin_dvr import dvr_search_get, dvr_search_post, dev_getCampus, dev_getBuild, dev_getType
from .admin_dvr import dvr_add_post
from .admin_notice import notice_create_post, notice_modfiy_get, notice_modfiy_post, notice_list, notice_delete
from .admin_basic import basic_campus, basic_campus_search, basic_campus_add, basic_campus_modfiy
from .admin_basic import basic_campus_delete, basic_campus_layer,basic_build_list
from .admin_basic import basic_bulid_add, basic_build_delete, basic_build_modfiy, basic_buildname_search, basic_type_index
from .admin_basic import basic_type_Add, basic_type_modfiy, basic_type_delete, basic_type_search
from .admin_user import admin_userindex, user_per_modfiy, user_delete, user_pwd_modfiy, user_create


# test
from forms import CreateUser


adminbg = Blueprint('adminbg', __name__)


@adminbg.route("/admin")
@login_required
@admin_required
def admin():
    """
    管理后台视图
    :return: 返回管理页面
    """
    notice = noticeindexlist()
    event = peventsindexlist(current_user.username)
    return render_template('/admin/admin.html',
                           data=notice,
                           events=event
                           )


@adminbg.route("/admin/query")
@login_required
@admin_required
def query():
    """
    数据查询视图
    :return: 返回数据查询结果并构建相应页面
    """
    result = admin_query()
    return render_template(
        '/admin/dbquery.html',
        posts=result['posts'],
        count=result['count'],
        pagination=result['pagination'],
        campus=result['campus']
    )


@adminbg.route("/admin/query/list")
@login_required
@admin_required
def query_list():
    """
    后台查询视图 根据校区/楼宇进行查询
    :return: json
    """
    result = admin_query_list()
    return render_template(
        "/admin/dbquery_list.html",
        posts=result['posts'],
        count=result['count'],
        pagination=result['pagination'],
        campus=result['campus'],
        ctitle=result['campusname'],
        btitle=result['buildname']
    )


@adminbg.route("/admin/query/serach", methods=['GET', 'POST'])
@login_required
@admin_required
def query_serach():
    """
    数据查询搜索页
    :return:
    """
    result = admin_query_serach()
    return render_template(
        '/admin/dbquery_serach.html',
        posts=result['posts'],
        count=result['count'],
        pagination=result['pagiation'],
        keyword=result['keyword']
    )


@adminbg.route("/admin/lvrmanage")
@login_required
@admin_required
def lvrmanager():
    """
    弱电间管理视图
    :return: 返回数据查询结果并构建相应页面
    """
    result = lvr_manager_index()
    return render_template(
        '/admin/lvrmanager.html',
        posts=result['posts'],
        count=result['count'],
        pagination=result['pagination'],
        campus=result['campus'])


@adminbg.route("/admin/lvrmanage/_queryipage", methods=['POST'])
@login_required
@admin_required
def querylvrpage():
    """
    后台弱电间信息ajax查询
    :return:
    """
    return lvr_manager_ajaxquery()


@adminbg.route("/admin/lvrmanage/list", methods=['GET', 'POST'])
@login_required
@admin_required
def querylvrlist():
    """
    后台弱电间信息校区查询
    :return:
    """
    if request.method == 'GET':
        result = lvr_list_get()
        return render_template(
            "/admin/lvrmanage_list.html",
            posts=result['posts'],
            count=result['count'],
            pagination=result['pagination'],
            campus=result['campus'],
            ctitle=result['ctitle'],
            btitle=result['btitle']
        )
    elif request.method == 'POST':
        return lvr_list_post()
    else:
        abort(404)



@adminbg.route("/admin/lvrmanage/search", methods=['GET', 'POST'])
@login_required
@admin_required
def querylvrserach():
    """
    后台弱电间信息搜索
    :return:
    """
    if request.method == 'GET':
        result = lvr_search_get()
        return render_template(
            "/admin/lvrmanage_serach.html",
            posts=result['posts'],
            count=result['count'],
            pagination=result['pagination'],
            keyword=result['keyword']
        )
    elif request.method == 'POST':
        return lvr_search_post()
    else:
        abort(500)


@adminbg.route("/admin/dvrmanage", methods=['GET', 'POST'])
@login_required
@admin_required
def dvrmanage():
    """
    :return: 返回数据查询结果并构建相应页面
    """
    if request.method == 'GET':
        result = dvr_manage_get()
        return render_template(
            '/admin/dvrmanage.html',
            datas=result['datas'],
            count=result['count'],
            pagination=result['pagination'],
            devtype=result['devtype'],
            transferclass="dvrmanage"
        )
    elif request.method == 'POST':
        return dvr_manage_post()


@adminbg.route("/admin/dvrmanage/list", methods=['GET', 'POST'])
@login_required
@admin_required
def dvrmanagelist():
    """
    设备信息页分类查询
    :return:
    """
    if request.method == 'GET':
        result = dvr_list_get()
        return render_template(
            '/admin/devmanage_list.html',
            datas=result['datas'],
            count=result['count'],
            pagination=result['pagination'],
            devtype=result['devtype'],
            devtypebname=result['devtypebname'],
            devostatus=result['devostatus'],
            transferclass="dvrlist"
        )
    elif request.method == 'POST':
        return dvr_list_post()


@adminbg.route("/admin/dvrmanage/search", methods=['GET', 'POST'])
@login_required
@admin_required
def dvrsearch():
    """
    设备信息搜索视图
    :return:
    """
    if request.method == 'GET':
        result = dvr_search_get()
        return render_template(
            '/admin/devmanage_serach.html',
            datas=result['datas'],
            count=result['count'],
            pagination=result['pagination'],
            keyword=result['keyword'],
            transferclass="dvrsearch"
        )
    elif request.method == 'POST':
        return dvr_search_post()


@adminbg.route("/admin/dvrmanage/add", methods=['GET', 'POST'])
@login_required
@admin_required
def dvrmanage_add():
    """
    设备新增页面
    :return: 返回数据查询结果并构建相应页面
    """
    if request.method == 'GET':
        campus = dev_getCampus()
        dvrtype = dev_getType()
        return render_template(
            '/admin/dvrmanage_add.html',
            campus=campus,
            type=dvrtype
        )
    elif request.method == 'POST':
        return dvr_add_post()

@adminbg.route("/admin/basicinfo")
@login_required
@admin_required
def basicinfo():
    """
    基础信息页面
    :return: 返回数据查询结果并构建相应页面
    """
    return render_template('/admin/basicinfo.html')


@adminbg.route("/admin/basicinfo/campus")
@login_required
@admin_required
def basiccampus():
    """
    校区信息
    :return: 返回页面
    """
    bcampus = basic_campus()
    return  render_template(
        '/admin/basicinfo_C.html',
        datas=bcampus['datas'],
        count=bcampus['count'],
        pagination=bcampus['pagination']
        )


@adminbg.route("/admin/basicinfo/campus/search")
@login_required
@admin_required
def basic_c_search():
    """
    校区搜索
    :return: 返回页面
    """
    search = basic_campus_search()
    return render_template(
        '/admin/basicinfo_C_S.html',
        datas=search['posts'],
        count=search['count'],
        pagination=search['pagination'],
        keyword=search['keyword']
        )


@adminbg.route("/admin/basicinfo/campus/add", methods=['POST'])
@login_required
@admin_required
def basic_c_add():
    """
    添加校区
    :return: 返回添加结果
    """
    result = basic_campus_add()
    return result


@adminbg.route("/admin/basicinfo/campus/modfiy", methods=['POST'])
@login_required
@admin_required
def basic_c_modfiy():
    """
    修改校区
    :return: 返回修改结果
    """
    result = basic_campus_modfiy()
    return result


@adminbg.route("/admin/basicinfo/campus/delete", methods=['POST'])
@login_required
@admin_required
def basic_c_detele():
    result = basic_campus_delete()
    return result


@adminbg.route("/admin/basicinfo/_querycampus", methods=['POST'])
@login_required
@admin_required
def basic_c_query():
    return basic_campus_layer()


@adminbg.route("/admin/basicinfo/build")
@login_required
@admin_required
def basic_build():
    result = basic_build_list()
    return render_template(
        '/admin/basicinfo_B.html',
        datas=result['datas'],
        count=result['count'],
        pagination=result['pagination'],
        campus_name=result['campus_name'],
        campus_id=result['campus_id']
        )


@adminbg.route("/admin/basicinfo/build/add", methods=['POST'])
@login_required
@admin_required
def basic_b_add():
    result = basic_bulid_add()
    return result

@adminbg.route("/admin/basicinfo/build/delete", methods=['POST'])
@login_required
@admin_required
def basic_b_delete():
    result = basic_build_delete()
    return result


@adminbg.route("/admin/basicinfo/build/modfiy", methods=['POST'])
@login_required
@admin_required
def basic_b_modfiy():
    return basic_build_modfiy()


@adminbg.route("/admin/basicinfo/build/serach")
@login_required
@admin_required
def basic_b_search():
    result = basic_buildname_search()
    return render_template(
        '/admin/basicinfo_B_S.html',
        datas=result['posts'],
        count=result['count'],
        pagination=result['pagination'],
        keyword=result['keyword']
    )


@adminbg.route("/admin/basicinfo/devtype")
@login_required
@admin_required
def basic_t_index():
    result = basic_type_index()
    return render_template(
        '/admin/basicinfo_DT.html',
        datas=result['datas'],
        count=result['count'],
        pagination=result['pagination']
    )


@adminbg.route("/admin/basicinfo/devtype/add", methods=['POST'])
@login_required
@admin_required
def basic_t_Add():
    return basic_type_Add()


@adminbg.route("/admin/basicinfo/devtype/modfiy", methods=['POST'])
@login_required
@admin_required
def basic_t_modfiy():
    return basic_type_modfiy()


@adminbg.route("/admin/basicinfo/devtype/delete", methods=['POST'])
@login_required
@admin_required
def basic_t_delete():
    return basic_type_delete()


@adminbg.route("/admin/basicinfo/devtype/search")
@login_required
@admin_required
def basic_t_search():
    result = basic_type_search()
    return render_template(
        '/admin/basicinfo_DT_S.html',
        datas=result['datas'],
        count=result['count'],
        pagination=result['pagination'],
        keyword=result['keyword']
    )


@adminbg.route("/admin/usrmanage")
@login_required
@admin_required
def usrmanage():
    """
    :return: 返回数据查询结果并构建相应页面
    """
    result = admin_userindex()
    return render_template(
        '/admin/usrmanage.html',
        posts=result['posts'],
        count=result['count'],
        pagination=result['pagination'],
        all_count=result['count'],
        suadmin_count=result['suadmin_count'],
        admin_count=result['admin_count'],
        user_count=result['user_count'],
                           )


@adminbg.route("/admin/usrmanage/permodfiy", methods=['POST'])
@login_required
@admin_required
def usrpermodfiy():
    return user_per_modfiy()


@adminbg.route("/admin/usrmanage/usrdel", methods=['POST'])
@login_required
@admin_required
def usrdel():
    return user_delete()


@adminbg.route("/admin/usrmanage/pwdmodfiy", methods=['POST'])
@login_required
@admin_required
def usrpwdmodfiy():
    return user_pwd_modfiy()


@adminbg.route("/admin/usrcreate", methods=['GET', 'POST'])
@login_required
@admin_required
def usecreate():
    form = user_create()
    if form == 0:
        return redirect(url_for('adminbg.usrmanage'))
    pwd_v = passwdcreate()
    return render_template("/admin/usercreate.html", form=form, pwd_v=pwd_v)


@adminbg.route("/admin/sysmanage", methods=['GET', 'POST'])
@login_required
@admin_required
def sysmanage():
    """
    :return: 返回数据查询结果并构建相应页面
    """
    eventlog("[访问系统设置]")
    default_value = ""
    if request.method == 'POST':
        pagesize = request.form.get('syspagen', 1)
        pagesize_index = request.form.get('syspageindex', 1)
        if pagesize.isdigit():
            optionsupdate('pagination', int(pagesize))
            optionsupdate('pagination_index', int(pagesize_index))
            flash(u"修改完成", 'success')
            eventlog("[修改系统设置]")
        else:
            session.pop('_flashes', None)
            flash(u"分页条数输入有误，请检查输入", 'danger')
    syspagn = Setting().pagination
    syspage_index = Setting().page_index
    return render_template('/admin/sysmanage.html', syspagn=syspagn, syspageindex=syspage_index)


@adminbg.route("/admin/log", methods=['GET', 'POST'])
@login_required
@admin_required
def logviews():
    """
    操作日志界面
    :return: 返回数据查询结果并构建相应页面
    """
    if request.method == "GET":
        page = request.values.get('page', 1, type=int)
        uname = request.values.get('username', "", type=str)
        username = b64decode(unquote(uname))
        catsname = request.values.get('cats', "", type=str)
        cats = b64decode(unquote(catsname))
        date = request.values.get('date', "", type=str)
        logdata = Dev_Loging.query.filter(
            (Dev_Loging.UserName.like("%" + username + "%"), "")[username is None],
            (Dev_Loging.Date.like("%" + date + "%"), "")[date is None],
            (Dev_Loging.Log.like("%" + cats + "%"), "")[cats is None]
        )
        paginateion = logdata.paginate(
            page, per_page=Setting().pagination
        )
        posts = paginateion.items
        count = logdata.count()
        eventlog("[查看日志]" + " 第" + str(page) +"页")
        return render_template(
            '/admin/log.html', posts=posts, count=count, pagination=paginateion,
            page=page, username=uname, cats=catsname, date=date,
            thuname=username.decode('utf-8'), thcats=cats.decode('utf-8')
        )
    elif request.method == "POST":
        cleancode = request.values.get('logcode', 'None', type=str)
        if cleancode == "all":
            return emptylog()
        else:
            abort(500)


@adminbg.route("/admin/notecreate", methods=['GET', 'POST'])
@login_required
@admin_required
def notecreate():
    """
    通知公告创建页面
    :return:
    """
    if request.method == 'GET':
        eventlog("[访问创建公告页面]")
        notename = ""
        notecontent = ""
        return render_template(
            '/admin/notecreate.html',
            name=notename,
            editorcontent=notecontent,
            operation=u"创建公告"
        )
    if request.method == 'POST':
        id = notice_create_post()
        return redirect(url_for('adminbg.notecreate_id', id=id))



@adminbg.route("/admin/notecreate/<id>", methods=['GET', 'POST'])
@login_required
@admin_required
def notecreate_id(id):
    """
    通知公告修改页面
    :return:
    """
    if request.method == 'GET':
        try:
            eventlog("[访问修改公告页面 公告id: " + str(id) + "]")
            result = notice_modfiy_get(id)
            return render_template(
                '/admin/notecreate.html',
                name=result['notename'],
                editorcontent=result['notecontent'],
                operation=u"编辑公告"
            )
        except Exception as e:
            abort(500)
    if request.method == 'POST':

        try:
            note = notice_modfiy_post(id)
            return redirect(url_for('adminbg.notecreate_id', id=note))
        except Exception as e:
            abort(500)


@adminbg.route("/admin/notelist", methods=['GET', 'POST'])
@login_required
@admin_required
def notelist():
    """
    通知公告列表页
    :return:
    """
    notice = notice_list()
    return render_template(
        "/admin/noticelist.html",
        posts=notice['posts'],
        count=notice['count'],
        pagination=notice['pagination'],
        page=notice['page']
    )


@adminbg.route("/admin/notelist/<int:id>/delete", methods=['POST'])
@login_required
@admin_required
def notedel(id):
    """
    删除通知公告
    :param id: 公告id
    :return:
    """
    notice_delete_result = notice_delete(id)
    return notice_delete_result

@adminbg.route("/admin/_dvrquerylvr", methods=['POST'])
@login_required
@admin_required
def devquerylvr():
    campus = request.values.get("campus")
    result = dev_getBuild(campus)
    return result