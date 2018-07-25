#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/21 14:24
# @Author  : Derek.S
# @Site    : 设备信息管理
# @File    : admin_dvr.py

from flask import jsonify, request, url_for
from models import Setting, Dev_DeviceInfo, DevDevType, Dev_LVRInfo, DevBuild, Dev_DeviceStatus, Dev_Campus
from log import eventlog
from base64 import b64decode
from urllib import unquote
from ext import db
import json
from .admin_lvr import LVRNumRefresh

import traceback


def dvr_manage_get():
    page = request.args.get('page', 1, type=int)
    request.script_root = url_for('indexview.index', _external=True)
    count = Dev_DeviceInfo.query.count()
    pagination = Dev_DeviceInfo.query.order_by(Dev_DeviceInfo.ID.asc()).paginate(
        page, per_page=Setting().pagination
    )
    datas = pagination.items
    devtype = DevDevType.query.all()
    result = {
        'datas': datas,
        'count': count,
        'pagination': pagination,
        'devtype': devtype
    }
    return result


def dvr_manage_post():
    count = request.values.get('count', None, type=int)
    pagenum = request.values.get('pagenum', None, type=int)
    page_num = ((count / Setting().pagination + pagenum), 0)[count / Setting().pagination == 0]
    dvrinfo = Dev_DeviceInfo.query.order_by(Dev_DeviceInfo.ID.asc()).paginate(
        (page_num), per_page=Setting().pagination
    )
    dvrinfotemp = []
    hasnext = {
        'next': dvrinfo.has_next
    }
    for devx in dvrinfo.items:
        jsonlist = devx.to_json()
        jsonlist.update(hasnext)
        dvrinfotemp.append(jsonlist)
    return jsonify(dvrinfotemp)


def dvr_list_get():
    page = request.args.get('page', 1, type=int)
    request.script_root = url_for('indexview.index', _external=True)
    devtype = b64decode(unquote(request.args.get('devtype', "", type=str)))
    devonline = unquote(request.args.get('devonline', "", type=str))
    if devonline == "5piv":
        devonline = "Y"
    elif devonline == "5ZCm":
        devonline = "N"
    devinfo = dvrselectsql(devtype, devonline)
    pagination = devinfo.paginate(
        page, per_page=Setting().pagination
    )
    count = devinfo.count()
    datas = pagination.items
    dev_types = DevDevType.query.all()
    result = {
        'datas': datas,
        'count': count,
        'pagination': pagination,
        'devtype': dev_types,
        'devtypebname': devtype.decode('utf-8'),
        'devostatus': devonline
    }
    return result


def dvr_list_post():
    devtype = b64decode(unquote(request.values.get('devtype', "", type=str)))
    devonline = unquote(request.values.get('devonline', "", type=str))
    if devonline == "5piv":
        devonline = "Y"
    elif devonline == "5ZCm":
        devonline = "N"
    count = request.values.get('count', None, type=int)
    pagenum = request.values.get('pagenum', None, type=int)
    page_num = ((count / Setting().pagination + pagenum), 0)[count / Setting().pagination == 0]
    devinfo = dvrselectsql(devtype, devonline)
    dvrinfo = devinfo.paginate(
        page_num, per_page=Setting().pagination
    )
    dvrinfotemp = []
    hasnext = {
        'next': dvrinfo.has_next
    }
    for devx in dvrinfo.items:
        jsonlist = devx.to_json()
        jsonlist.update(hasnext)
        dvrinfotemp.append(jsonlist)
    return jsonify(dvrinfotemp)


def dvrselectsql(devtype, devonline):
    """
    设备信息查询sql
    :return:
    """
    devinfo = Dev_DeviceInfo.query.filter(
        (Dev_DeviceInfo.DeviceCategory.like("%" + devtype + "%"), "")[devtype is None],
        (Dev_DeviceInfo.DeviceCondition.like("%" + devonline + "%"), "")[devonline is None]
    ).order_by(Dev_DeviceInfo.ID.asc())
    return devinfo


def dvr_search_get():
    request.script_root = url_for('indexview.index', _external=True)
    page = request.args.get('page', 1, type=int)
    word = request.args.get('keyword', "", type=str)
    serach = unquote(b64decode(word)).decode('utf-8')
    serp = dvrsearchsql(serach)
    pagination = serp.paginate(
        page, per_page=Setting().pagination
    )
    count = serp.count()
    datas = pagination.items
    eventlog(
        "[管理后台设备信息 搜索]" + serach.encode('utf-8') + " 第" + str(page) + "页"
    )
    result = {
        'datas': datas,
        'count': count,
        'pagination': pagination,
        'keyword': serach
    }
    return result


def dvr_search_post():
    pagenum = request.values.get('pagenum', None, type=int)
    count = request.values.get('count', None, type=int)
    word = request.values.get('keyword', None, type=str)
    search = b64decode(unquote(word)).decode('utf-8')
    serp = dvrsearchsql(search)
    page_num = ((count / Setting().pagination + pagenum), 0)[count / Setting().pagination == 0]
    paginateion = serp.paginate(
        page_num, per_page=Setting().pagination
    )
    serachresult = []
    hasnext = {
        'next': paginateion.has_next
    }
    for serachone in paginateion.items:
        jsonlist = serachone.to_json()
        jsonlist.update(hasnext)
        serachresult.append(jsonlist)
    eventlog(
        "[ajax加载搜索页面下一页]" + search.encode('utf-8') + " 第" + str(page_num) + "页"
    )
    return jsonify(serachresult)


def dvrsearchsql(keyword):
    search_result = Dev_DeviceInfo.query.filter(
        (Dev_DeviceInfo.DeviceName.like("%" + keyword + "%"), "")[keyword is None] |
        (Dev_DeviceInfo.DeviceCategory.like("%" + keyword + "%"), "")[keyword is None] |
        (Dev_DeviceInfo.DeviceSN.like("%" + keyword + "%"), "")[keyword is None] |
        (Dev_DeviceInfo.DeviceID.like("%" + keyword + "%"), "")[keyword is None]
    ).order_by(Dev_DeviceInfo.ID.asc())
    return search_result


def dev_getCampus():
    campus = Dev_Campus.query.all()
    return campus


def dev_getType():
    type = DevDevType.query.all()
    return type


def dev_getBuild(campus):
    campus_decode = b64decode(unquote(campus)).decode('utf-8')
    result = DevBuild.query.filter_by(
        Campus=campus_decode
    ).all()
    Build = []
    Build_result = []
    for each in result:
        Build.append(each.BuildName)
    for each_build in Build:
        name = {
            "BuildName": each_build
        }
        Build_result.append(name)
    return jsonify(Build_result)



def dvr_add_post():
    dvrdatas = request.get_json()
    for each_dvrinfo in dvrdatas:
        devname = each_dvrinfo['name']
        devtype = each_dvrinfo['type']
        devserial = each_dvrinfo['serial']
        devid = each_dvrinfo['id']
        devputaway = each_dvrinfo['putaway']
        devcampus = each_dvrinfo['campus']
        devlvr = each_dvrinfo['lvr']
        devbuild = each_dvrinfo['build']
        devhostname = each_dvrinfo['hostname']
        devaddr = each_dvrinfo['addr']
        devip = each_dvrinfo['ip']
        devport =each_dvrinfo['port']
        devinfo_db = Dev_DeviceInfo(devname, devtype, devserial, devputaway, devid)
        devstatus_db = Dev_DeviceStatus(devcampus, devbuild, devlvr, devhostname, devaddr, devip, devport, devserial, devputaway)
        db.session.add(devinfo_db)
        if devputaway == "Y":
            db.session.add(devstatus_db)
        else:
            pass
        db.session.commit()
    status = {
        'status': 200
    }
    LVRNumRefresh()
    return jsonify(status)


def dev_getLVR(campus, build):
    campus_decode = b64decode(unquote(campus)).decode('utf-8')
    build_decode = b64decode(unquote(build)).decode('utf-8')
    result = Dev_LVRInfo.query.filter_by(
        Campus=campus_decode,
        BuildName=build_decode
    ).all()
    Lvr = []
    Lvr_result = []
    for each in result:
        Lvr.append(each.LVRNo)
    for each_lvrno in Lvr:
        no = {
            "LVRNo": each_lvrno
        }
        Lvr_result.append(no)
    return jsonify(Lvr_result)


def dev_checkDeviceid(devid):
    id = devid['deviceid']
    result = Dev_DeviceInfo.query.filter_by(
        DeviceID=id
    ).count()
    id_select_result = {
        "id_select_result": result
    }
    return jsonify(id_select_result)


def dev_devup(jsondata):
    if jsondata["op"] == 'get':
        count = 0
        try:
            campus = dev_getCampus()
            dvrtype = dev_getType()
            dev_id = jsondata["idarray"]
            result_array = []
            for one in dev_id:
                deviceinStatus = Dev_DeviceStatus.query.filter(
                    Dev_DeviceStatus.DeviceModel == one
                )
                if deviceinStatus.count():
                    statusResult = deviceinStatus.one()
                    if statusResult.DeviceCondition == "Y":
                        continue
                    deviceinInfo = Dev_DeviceInfo.query.filter(
                        Dev_DeviceInfo.DeviceID == one
                    ).one()
                    infoResult = deviceinInfo
                    count += 1
                    result = {
                        'count': count,
                        'statusResult': statusResult,
                        'infoResult': infoResult
                    }
                    result_array.append(result)
                else:
                    count += 1
                    deviceinInfo = Dev_DeviceInfo.query.filter(
                        Dev_DeviceInfo.DeviceID == one
                    ).one()
                    infoResult = deviceinInfo
                    result = {
                        'count': count,
                        'statusResult': '',
                        'infoResult': infoResult
                    }
                    result_array.append(result)
            return result_array, campus, dvrtype
        except Exception as e:
            print(e)
            result = {
                "status": 404,
                "message": "Error"
            }
            return json.dumps(result)
    elif jsondata["op"] == 'post':
        idarray = jsondata["idarray"]
        result = {
            "status": 0,
            "message": "Error"
        }
        for each_dev in idarray:
            dev_id = each_dev["id"]
            DevS_Campus = each_dev["campus"]
            DevS_Location = each_dev["build"]
            DevS_RoomNo = each_dev["lvr"]
            DevS_HostName = each_dev["hostname"]
            DevS_LAA = each_dev["addr"]
            DevS_IP = each_dev["ip"]
            DevS_Port = each_dev["port"]
            DevS_ID = dev_id
            deviceinStatus = Dev_DeviceStatus.query.filter(
                Dev_DeviceStatus.DeviceModel == dev_id
            )
            if deviceinStatus.count():
                deviceinStatus.update({
                    Dev_DeviceStatus.Campus: DevS_Campus,
                    Dev_DeviceStatus.Location: DevS_Location,
                    Dev_DeviceStatus.RoomNo: DevS_RoomNo,
                    Dev_DeviceStatus.HostName: DevS_HostName,
                    Dev_DeviceStatus.LAA: DevS_LAA,
                    Dev_DeviceStatus.HigherlinkIP: DevS_IP,
                    Dev_DeviceStatus.HigherlinkPort: DevS_Port,
                    Dev_DeviceStatus.DeviceCondition: "Y"
                })
                deviceinInfo = Dev_DeviceInfo.query.filter(
                    Dev_DeviceInfo.DeviceID == dev_id
                )
                deviceinInfo.update({Dev_DeviceInfo.DeviceCondition: "Y"})
                db.session.commit()
                result = {
                    'status': 1,
                    'message': "ok"
                }
            else:
                DevS_DB = Dev_DeviceStatus(
                    DevS_Campus,
                    DevS_Location,
                    DevS_RoomNo,
                    DevS_HostName,
                    DevS_LAA,
                    DevS_IP,
                    DevS_Port,
                    DevS_ID,
                    "Y"
                )
                deviceinInfo = Dev_DeviceInfo.query.filter(
                    Dev_DeviceInfo.DeviceID == dev_id
                )
                deviceinInfo.update({Dev_DeviceInfo.DeviceCondition: "Y"})
                db.session.add(DevS_DB)
                db.session.commit()
                result = {
                    'status': 1,
                    'message': "ok"
                }
        LVRNumRefresh()
        return json.dumps(result)


def dev_devdown():
    try:
        dev_id = request.values.get("array_id")
        for one in json.loads(dev_id.encode("utf-8")):
            device = Dev_DeviceInfo.query.filter(
                Dev_DeviceInfo.DeviceID == one
            )
            if device:
                for each_Row in device:
                    device_Condition = each_Row.DeviceCondition
                    if device_Condition != "N":
                        device.update({Dev_DeviceInfo.DeviceCondition: "N"})
                        Dev_DeviceStatus.query.filter(
                            Dev_DeviceStatus.DeviceModel == one
                        ).update({Dev_DeviceStatus.DeviceCondition: "N"})
                    else:
                        pass
            db.session.commit()
            DCondition_result = {
                'status': 1,
                'message': 'ok'
            }
        LVRNumRefresh()
        return json.dumps(DCondition_result)
    except Exception as e:
        print(e)
        DCondition_result = {
            'status': 500,
            'message': 'Server Error'
        }
        return json.dumps(DCondition_result)


def dev_devdel():
    try:
        dev_id = request.values.get("array_id")
        for one in json.loads(dev_id.encode("utf-8")):
            device = Dev_DeviceInfo.query.filter(
                Dev_DeviceInfo.DeviceID == one
            )

            if device.one().DeviceCondition == "Y":
                delete_status = {
                    'status': 2,
                    'message': '删除前请先下架设备'
                }
                return json.dumps(delete_status)
            else:
                device.delete()
                db.session.commit()
                delete_status = {
                    'status': 1,
                    'message': 'success'
                }
        LVRNumRefresh()
        return json.dumps(delete_status)
    except Exception as e:
        delete_status = {
            'status': 500,
            'message': 'error'
        }
        return json.dumps(delete_status)

def dev_m(jsondata):
    id_array = jsondata['idarray']
    infoResult = ""
    try:
        for each_id in id_array:
            device = Dev_DeviceInfo.query.filter(
                Dev_DeviceInfo.DeviceID == each_id
            )
            if device.count():
                infoResult = device.one()
        return infoResult, dev_getType()
    except Exception as e:
        pass


def dev_m_post(jsondata):
    id_array = jsondata['idarray'][0]
    id = jsondata["id"]
    newid = id_array["id"]
    name = id_array["name"]
    serial = id_array["serial"]
    type = id_array["type"]
    try:
        device = Dev_DeviceInfo.query.filter(
            Dev_DeviceInfo.DeviceID == id
        )

        if device.count():
            device.update({
                Dev_DeviceInfo.DeviceName: name,
                Dev_DeviceInfo.DeviceID: newid,
                Dev_DeviceInfo.DeviceSN: serial,
                Dev_DeviceInfo.DeviceCategory: type
            })

        device_status = Dev_DeviceStatus.query.filter(
            Dev_DeviceStatus.DeviceModel == id
        )
        
        if device_status.count():
            device_status.update({
                Dev_DeviceStatus.DeviceModel: newid
            })

        db.session.commit()
        result = {
            'status': 1,
            'message': "ok"
        }
        LVRNumRefresh()
        return json.dumps(result)
    except Exception as e:
        result = {
            'status': 0,
            'message': "Error"
        }
        return json.dumps(result)