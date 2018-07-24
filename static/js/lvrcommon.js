/// <reference path="C:\\Users\\Derek.S\\AppData\\Roaming\\npm\\node_modules\\@types\\jquery\\index.d.ts"/>
$(document).ready(
    function(){
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token)
                }
            }
        })
        $.base64.utf8encode = true;
        $.base64.utf8decode = true;
        id_array = new Array()

        $(document).on("change", "select#lvradd_campus", function () {
            var $v = $(this)
            var $build = $v.parent().next().children()
            if ($v.val() == "") {
                $build.append('<option value="">请选择楼宇</option>')
            } else {
                $build.empty()
            }
            js_dvr_querybuild($v.val(), $build)
        })

        $(document).on("change", "select#lvradd_build", function () {
            var $v = $(this)
            var $campus = $v.parent().prev().children()
            var $lvr = $v.parent().next().children()
            if ($v.val() == "") {
                $lvr.append('<option value="">请选择弱电间</option>')
            } else {
                $lvr.empty()
            }
            js_dvr_querylvr($campus.val(), $v.val(), $lvr)
        })

        $(document).on("click", "a.devaddspan", function () {
            var tParent = $(this).parent()
            var cbl_tr = $(this).parents().find(".devselect")
            var clone = $(this).parents("tr.devadd_newtable").clone()
            var devadd_td = $(this).parent().prevAll()
            var td_id = $(".td_id:last")
            var new_td_id = parseInt(td_id.text()) + 1
            clone.find("td.td_id").text(new_td_id)
            var selectedValue_Campus = cbl_tr.find("select#lvradd_campus").val()
            clone.find("option[value = '" + selectedValue_Campus + "']").attr("selected", "selected")
            var selectedValue_build = cbl_tr.find("select#lvradd_campus").val()
            clone.find("option[value = '" + selectedValue_build + "']").attr("selected", "selected")
            $("table#lvradd_table > tbody").append(clone)
            
        });

        $(document).on("click", "a.devdelspan", function () {
            if ($("td.devadd_newtd").length == 1) {
                alert("新增行只有1行时不得删除")
            } else {
                $(this).parents("td.devadd_newtd").remove()
            }
        });

    }
)

function js_dvr_querylvr(campus_name, build_name, nextLvrElement) {
    var posturl = Flask.url_for("adminbg.devquerylvr")
    var campusb64 = encodeURIComponent($.base64.encode(campus_name), 'utf-8')
    var buildb64 = encodeURIComponent($.base64.encode(build_name), 'utf-8')
    $.ajaxSetup({ 
        async : false 
    });       
    $.post(posturl, {
        campus: campusb64,
        build: buildb64
    }, function(data){
        if (data.length != 0){
            nextLvrElement.append('<option value="lvr_null">请选择弱电间</option>')
            $.each(data, function(one){
                eachone = data[one]
                nextLvrElement.append('<option value="'+ eachone.LVRNo +'">'+ eachone.LVRNo +'</option>')
            })
        } else if (build_name == "build_null"){
            nextLvrElement.append('<option value="lvr_null">请选择弱电间</option>')
        } else {
            nextLvrElement.append('<option value="lvr_null">该楼暂无弱电间</option>')
        }
    }).fail(function (status) {
        console.log(status)
    })

}

function js_dvr_querybuild(campus_name, nextBuildElement) {
    var posturl = Flask.url_for('adminbg.devquerybuild')
    var campusb64 = encodeURIComponent($.base64.encode(campus_name), 'utf-8')
    $.ajaxSetup({ 
        async : false 
    });   
    $.post(posturl, {
        campus: campusb64
    }, function (data) {
        if (data.length != 0){
            nextBuildElement.append('<option value="build_null">请选择楼宇</option>')
            $.each(data, function (one) {
                eachone = data[one]
                nextBuildElement.append('<option value="'+ eachone.BuildName +'">'+ eachone.BuildName +'</option>')
            })
        } else if (campus_name == "campus_null"){
            nextBuildElement.append('<option value="build_null">请选择楼宇</option>')
        } else {
            nextBuildElement.append('<option value="build_null">该校区暂无楼宇信息</option>')
        }
    }).fail(function (status) {
        console.log(status)
    })
}


function js_lvr_create() {
    var url = Flask.url_for('adminbg.lvradd')
    layer_add = layer.open({
        type: 2,
        skin: 'layui-layer-rim',
        title: "创建新弱电间",
        area: ['1200px', '500px'],
        content: url
    })
}

function js_lvr_addajax() {
    var lvrinfo = $("td.devadd_newtd")
    var lvrinfo_datas = []
    lvrinfo.each(function(){
        var lvrinfo_data = {}
        lvrinfo_data["name"] = $(this).find("#lvradd_name").val()
        lvrinfo_data["campus"] = $(this).find("#lvradd_campus").val()
        lvrinfo_data["build"] = $(this).find("#lvradd_build").val()
        lvrinfo_data["buildnum"] = $(this).find("#lvradd_buildnum").val()
        lvrinfo_data["floornum"] = $(this).find("#lvradd_floornum").val()
        lvrinfo_data["roomnum"] = $(this).find("#lvradd_roomnum").val()
        lvrinfo_data["equnum"] = $(this).find("#lvradd_equnum").val()
        lvrinfo_datas.push(lvrinfo_data)
    })
    if(dataCheak(lvrinfo_datas)){
        if(confirm('准备添加数据，是否继续？')){
            $.ajax({
                url: Flask.url_for('adminbg.lvradd'),
                type: 'POST',
                data: JSON.stringify(lvrinfo_datas),
                dataType: "json",
                contentType: "application/json",
                success: function(data){
                    if (data.status != 200) {
                        alert("添加失败")
                    }else{
                        alert("添加成功")
                        parent.location.reload()
                    }
                }
            })
        }
    }
}

function dataCheak(lvrinfo_datas){
    for (x in lvrinfo_datas){
        if (isNull(lvrinfo_datas[x].name)) {
            alert("存在未填写项，请核对数据。")
            return false
        }
        if(lvrinfo_datas[x].campus == "campus_null"){
            alert("存在未选择校区数据，请核对。")
            return false
        }
        if(lvrinfo_datas[x].build == "build_null"){
            alert("存在未选择楼宇数据，请核对。")
            return false
        }
        if (isNull(lvrinfo_datas[x].buildname)) {
            alert("存在未填写项，请核对数据。")
            return false
        }
        if (isNull(lvrinfo_datas[x].floornum)) {
            alert("存在未填写项，请核对数据。")
            return false
        }
        if (isNull(lvrinfo_datas[x].roomnum)) {
            alert("存在未填写项，请核对数据。")
            return false
        }
        if (isNull(lvrinfo_datas[x].equnum)) {
            alert("存在未填写项，请核对数据。")
            return false
        }
    }
    return true
}

function isNull( str ){
    if ( str == "" ) return true
    var regu = "^[ ]+$"
    var re = new RegExp(regu)
    return re.test(str)
    }


function js_lvr_idarry( id ){
    id_array.push(id)
    return id_array
}


function js_lvr_delLVRroom( idarray ){
    if(confirm("确定删除么？")){
        if(idarray){
            var jsondata = {
                "lvrno": idarray
            }
            $.ajax({
                url: Flask.url_for('adminbg.lvrdel'),
                type: "post",
                data: JSON.stringify(jsondata),
                contentType: "application/json",
                dataType: "json",
                success: function(resp) {
                    if (resp.status != 1) {
                        alert("删除失败 " + resp.message)
                        id_array.length = 0
                    }else{
                        alert("删除成功")
                        window.location.reload()
                    }
                }
            })
        }
    }
}

function js_lvr_modify(idarray, op){
    id = idarray[0]
    if(op == "get"){
        if(idarray){
            var postarray = {
                "op": "get",
                "id": id,
                "idarray": idarray
            }
            $.ajax({
                url: Flask.url_for('adminbg.lvrmodify'),
                type: "post",
                data: JSON.stringify(postarray),
                contentType: "application/json",
                dataType: "html",
                success: function(html) {
                    layer_devup = layer.open({
                        type: 1,
                        skin: 'layui-layer-rim',
                        title: "修改设备",
                        area: ['1200px', '500px'],
                        content: html
                    })
                }
            })
        }
    }
    else if(op == "post"){
        if(confirm("确定修改设备信息么？")){
            if(idarray){
                var lvr_array = new Array()
                var modify_lvr = $("td.devadd_newtd")
                modify_lvr.each(function(){
                    var lvrinfo_data = {}
                    lvrinfo_data["lvrno"] = $(this).find("#lvradd_name").val()
                    lvrinfo_data["campus"] = $(this).find("#lvradd_campus").val()
                    lvrinfo_data["build"] = $(this).find("#lvradd_build").val()
                    lvrinfo_data["buildNo"] = $(this).find("#lvradd_buildnum").val()
                    lvrinfo_data["floorNo"] = $(this).find("#lvradd_floornum").val()
                    lvrinfo_data["roomNo"] = $(this).find("#lvradd_roomnum").val()
                    lvrinfo_data["equnum"] = $(this).find("#lvradd_equnum").val()
                    lvr_array.push(lvrinfo_data)
                })
                var postarray = {
                    "op": "post",
                    "id": id,
                    "idarray": lvr_array
                }
                $.ajax({
                    url: Flask.url_for('adminbg.lvrmodify'),
                    type: "post",
                    data: JSON.stringify(postarray),
                    contentType: "application/json",
                    dataType: "json",
                    success: function(resp) {
                        console.log(resp)
                        if(resp.status != 1){
                            alert("修改失败")
                        }
                        else{
                            alert("修改成功")
                            window.location.reload()
                        }
                    }
                })
            }

        }
    }

}