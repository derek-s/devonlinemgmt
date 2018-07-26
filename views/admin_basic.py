#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/21 21:47
# @Author  : Derek.S
# @Site    :
# @File    : admin_basic.py

from flask import request, url_for
from models import Setting, Dev_DeviceStatus, Dev_Campus, Dev_LVRInfo, Dev_DeviceInfo, DevDevType
from models import DevBuild
from base64 import b64decode
from urllib import unquote
from ext import db
import json


def basic_campus():
    """
    校区信息页面
    :return:
    """
    page = request.args.get('page', 1, type=int)
    request.script_root = url_for('indexview.index', _external=True)
    count = Dev_Campus.query.count()
    pagination = Dev_Campus.query.order_by(Dev_Campus.ID.asc()).paginate(
        page, per_page=Setting().pagination
    )
    datas = pagination.items
    result = {
        'datas': datas,
        'count': count,
        'pagination': pagination
    }
    return result


def basic_campus_search():
    """
    校区搜索页面
    :return:
    """
    request.script_root = url_for('indexview.index', _external=True)
    page = request.values.get('page', 1, type=int)
    word = request.values.get('keyword', "", type=str)
    search = b64decode(unquote(word)).decode('utf-8')
    select_result = Dev_Campus.query.filter(
        Dev_Campus.Campus.like("%" + search + "%")
    )
    pagination = select_result.paginate(
        page, per_page=Setting().pagination
    )
    count = select_result.count()
    posts = pagination.items
    result = {
        'posts': posts,
        'count': count,
        'pagination': pagination,
        'keyword': search
    }
    return result


def basic_campus_add():
    """
    增加校区功能
    :return:
    """
    campusname = request.values.get("campusname")
    if campusname == "":
        campus_add_status = {
            'status': 500,
            'message': '添加项为空'
        }
        return json.dumps(campus_add_status)
    else:
        campus_query_count = Dev_Campus.query.filter(Dev_Campus.Campus == campusname).count()
        if campus_query_count != 0:
            campus_table_query = Dev_Campus.query.filter(Dev_Campus.Campus == campusname).one()
            campus_table_name = campus_table_query.Campus
        else:
            campus_table_name = ''
        if campus_table_name == campusname:
            campus_add_status = {
                'status': 0,
                'message': '被添加项已存在'
            }
            return json.dumps(campus_add_status)
        else:
            new_campus = Dev_Campus(campusname)
            db.session.add(new_campus)
            db.session.commit()
            campus_add_status = {
                'status': 1,
                'message': 'success'
            }
            return json.dumps(campus_add_status)


def basic_campus_modfiy():
    """
    修改校区名称
    :param id: 校区id
    :return:  修改结果
    """
    try:
        campus_id = request.values.get("id")
        campus_new = request.values.get("cname")
        campus_info = Dev_Campus.query.filter(Dev_Campus.ID == campus_id).one()
        campus_old = campus_info.Campus
        DevBuild.query.filter(DevBuild.Campus == campus_old).update({DevBuild.Campus:campus_new})
        Dev_LVRInfo.query.filter(Dev_LVRInfo.Campus == campus_old).update({Dev_LVRInfo.Campus:campus_new})
        Dev_DeviceStatus.query.filter(Dev_DeviceStatus.Campus == campus_old).update({Dev_DeviceStatus.Campus:campus_new})
        Dev_Campus.query.filter(Dev_Campus.Campus == campus_old).update({Dev_Campus.Campus:campus_new})
        db.session.commit()
        campus_modfiy_status = {
            'status': 1,
            'message': 'success'
        }
        return json.dumps(campus_modfiy_status)
    except Exception as e:
        campus_modfiy_status = {
            'status': 5,
            'message': 'Server Error'
        }
        return json.dumps(campus_modfiy_status)


def basic_campus_delete():
    """
    删除校区功能
    :return:
    """
    delstatus = {
        'status': '',
        'message': ''
    }
    try:
        campus_id = request.values.get("array_id")
        for one in json.loads(campus_id.encode("utf-8")):
            campus_info = Dev_Campus.query.filter(
                Dev_Campus.ID == one
            )
            if campus_info:
                campus_info.delete()
        db.session.commit()
        delstatus['status'] = 1
        delstatus['message'] = "success"
        return json.dumps(delstatus)
    except Exception:
        delstatus['status'] = 500
        delstatus['message'] = "Server Error"
        return json.dumps(delstatus)


def basic_campus_layer():
    """
    楼宇信息修改页面弹窗加载校区名称
    :return: 查询结果json
    """
    campus_list = []
    campus_info = {
        "campus_info": campus_list,
        "status": 404
    }
    try:
        campus = Dev_Campus.query.all()
        for campus_one in campus:
            campus_info_one = {
                "id": campus_one.ID,
                "campus_name": campus_one.Campus.encode("utf-8")
            }
            campus_list.append(campus_info_one)
        campus_info['status'] = 1
        return json.dumps(campus_info)
    except Exception as e:
        campus_info['status'] = 404
        return json.dumps(campus_info)


def basic_build_list():
    """
    楼栋分类搜索
    :return:
    """
    page = request.args.get('page', 1, type=int)
    campus_id = request.args.get('campus_id', "-1", type=str)
    request.script_root = url_for('indexview.index', _external=True)
    if campus_id == "-1":
        build_count = DevBuild.query.count()
        pagination = DevBuild.query.order_by(DevBuild.ID.asc()).paginate(
            page, per_page=Setting().pagination
        )
        datas = pagination.items
        result = {
            "datas": datas,
            "count": build_count,
            "pagination": pagination,
            "campus_name": u"全部",
            "campus_id": campus_id
        }
        return result
    else:
        campus_info = Dev_Campus.query.filter(Dev_Campus.ID == int(campus_id)).one()
        campus_name = campus_info.Campus
        build_info = DevBuild.query.filter(
                DevBuild.Campus == campus_name
        )
        build_count = build_info.count()
        pagination = build_info.order_by(DevBuild.ID.asc()).paginate(
            page, per_page=Setting().pagination
        )
        datas = pagination.items
        result = {
            "datas": datas,
            "count": build_count,
            "pagination": pagination,
            "campus_name": campus_name,
            "campus_id": campus_id
        }
        return result


def basic_bulid_add():
    """
    增加楼栋
    :return:
    """
    campus_id = request.values.get("campus_id")
    bulidname = request.values.get("buildname")
    if bulidname == "":
        build_add_status = {
            'status': 500,
            'message': '添加项为空'
        }
        return json.dumps(build_add_status)
    else:
        campus_select = Dev_Campus.query.filter(
            Dev_Campus.ID == campus_id
        )
        campus_count = campus_select.count()
        if campus_count != 0:
            campus_select_one = campus_select.one()
            campus_name = campus_select_one.Campus
            build_select_count = DevBuild.query.filter(
                DevBuild.Campus == campus_name,DevBuild.BuildName == bulidname
            ).count()
            if build_select_count != 0:
                build_add_status = {
                    'status': 2,
                    'message': '添加项已存在'
                }
                return json.dumps(build_add_status)
            else:
                newbulid = DevBuild(campus_name, bulidname)
                db.session.add(newbulid)
                db.session.commit()
                build_add_status = {
                    'status': 1,
                    'message': 'success'
                }
                return json.dumps(build_add_status)
        else:
            build_add_status = {
                'status': 404,
                'message': '校区数据不存在'
            }
            return json.dumps(build_add_status)

def basic_build_delete():
    """
    删除楼栋
    :return:
    """
    delstatus = {
        'status': '',
        'messgae': ''
    }
    try:
        build_id = request.values.get("array_id")
        for one in json.loads(build_id.encode("utf-8")):
            build_info = DevBuild.query.filter(
                DevBuild.ID == one
            )
            if build_info:
                build_info.delete()
        db.session.commit()
        delstatus['status'] = 1
        delstatus['message'] = "success"
        return json.dumps(delstatus)
    except Exception:
        delstatus['status'] = 500
        delstatus['message'] = "Server Error"
        return json.dumps(delstatus)


def basic_build_modfiy():
    """
    修改楼栋信息
    :return:
    """
    try:
        build_id = request.values.get("id")
        build_name = request.values.get("bname")
        build_info = DevBuild.query.filter(DevBuild.ID == build_id).one()
        buildname_old = build_info.BuildName
        Dev_DeviceStatus.query.filter(
            Dev_DeviceStatus.Location == buildname_old).update(
            {Dev_DeviceStatus.Location:build_name}
        )
        Dev_LVRInfo.query.filter(
            Dev_LVRInfo.BuildName == buildname_old
        ).update(
            {Dev_LVRInfo.BuildName:build_name}
        )
        DevBuild.query.filter(
            DevBuild.BuildName == buildname_old
        ).update(
            {DevBuild.BuildName:build_name}
        )
        db.session.commit()
        build_modfiy_status = {
            'status': 1,
            'message': 'success'
        }
        return json.dumps(build_modfiy_status)
    except Exception as e:
        build_modfiy_status = {
        'status': 500,
        'message': 'Server Error'
        }
        return json.dumps(build_modfiy_status)


def basic_buildname_search():
    """
    楼栋名称搜索
    :return:
    """
    request.script_root = url_for('indexview.index', _external=True)
    page = request.values.get('page', 1, type=int)
    word = request.values.get('keyword', "", type=str)
    search = b64decode(unquote(word)).decode('utf-8')
    select_result = DevBuild.query.filter(
        DevBuild.BuildName.like("%" + search + "%")
    )
    pagination = select_result.paginate(
        page, per_page=Setting().pagination
    )
    count = select_result.count()
    posts = pagination.items
    result = {
        'posts': posts,
        'count': count,
        'pagination': pagination,
        'keyword': search
    }
    return result


def basic_type_index():
    """
    设备类型
    :return:
    """
    request.script_root = url_for('indexview.index', _external=True)
    page = request.values.get('page', 1, type=int)
    count = DevDevType.query.count()
    pagination = DevDevType.query.order_by(DevDevType.ID.asc()).paginate(
        page, per_page=Setting().pagination
    )
    datas = pagination.items
    result = {
        'datas': datas,
        'count': count,
        'pagination': pagination
    }
    return result


def basic_type_Add():
    """
    增加设备信息
    :return:
    """
    typename = request.values.get("typename")
    if typename == "":
        type_add_status = {
            'status': 500,
            'message': "添加项为空"
        }
        return json.dumps(type_add_status)
    else:
        type_query_count = DevDevType.query.filter(DevDevType.Type == typename).count()
        if type_query_count != 0:
            type_table_query = DevDevType.query.filter(DevDevType == typename).one()
            type_table_name = type_table_query.Type
        else:
            type_table_name = ""
        if type_table_name == typename:
            type_add_status = {
                'status': 0,
                'message': '被添加项已存在'
            }
            return json.dumps(type_add_status)
        else:
            new_type = DevDevType(typename)
            db.session.add(new_type)
            db.session.commit()
            type_add_status = {
                'status': 1,
                'message': 'success'
            }
            return json.dumps(type_add_status)


def basic_type_modfiy():
    """
    修改设备类型
    :return:
    """
    try:
        type_id = request.values.get("id")
        type_new = request.values.get("tname")
        type_info = DevDevType.query.filter(
            DevDevType.ID == type_id
        ).one()
        type_old = type_info.Type
        DevDevType.query.filter(DevDevType.Type == type_old).update({DevDevType.Type:type_new})
        Dev_DeviceInfo.query.filter(
            Dev_DeviceInfo.DeviceCategory == type_old
        ).update({Dev_DeviceInfo.DeviceCategory:type_new})
        db.session.commit()
        type_modfiy_status = {
            'status': 1,
            'message': 'success'
        }
        return json.dumps(type_modfiy_status)
    except Exception as e:
        type_modfiy_status = {
            'status': 5,
            'message': 'Server Error'
        }
        return json.dumps(type_modfiy_status)


def basic_type_delete():
    """
    删除设备类型
    :return:
    """
    try:
        type_id = request.values.get("array_id")
        for one in json.loads(type_id.encode("utf-8")):
            type_info = DevDevType.query.filter(
                DevDevType.ID == one
            )
            if type_info:
                type_info.delete()
        db.session.commit()
        delete_status = {
            'status': 1,
            'message': 'success'
        }
        return json.dumps(delete_status)
    except Exception as e:
        delete_status = {
            'status': 500,
            'message': 'success'
        }
        return json.dumps(delete_status)


def basic_type_search():
    """
    设备类型搜索
    :return:
    """
    request.script_root = url_for('indexview.index', _external=True)
    page = request.values.get('page', 1, type=int)
    word = request.values.get('keyword', "", type=str)
    search = b64decode(unquote(word)).decode('utf-8')
    select_result = DevDevType.query.filter(
        DevDevType.Type.like("%" + search + "%")
    )
    pagination = select_result.paginate(
        page, per_page=Setting().pagination
    )
    count = select_result.count()
    datas = pagination.items
    result = {
        'datas': datas,
        'count': count,
        'pagination': pagination,
        'keyword': search
    }
    return result