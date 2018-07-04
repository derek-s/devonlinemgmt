/// <reference path="C:\\Users\\Derek.S\\AppData\\Roaming\\npm\\node_modules\\@types\\jquery\\index.d.ts"/>
$(document).ready(
    function () {
        $("#checkboxall").click(function () {
            if ($("#checkboxall").prop("checked")) {
                $("[name='oper']").prop("checked", true)
            } else {
                $("[name='oper']").prop("checked", false)
            }
        })
        $(document).on("click", '[name="oper"]', function () {
            var check = 0
            if ($("#checkboxall").prop("checked")) {
                $("#checkboxall").prop("checked", false)
            }
            var inputcount = $("input[name='oper']").length
            $("input[name='oper']").each(function () {
                if ($(this).prop("checked")) {
                    check += 1
                }
                if (inputcount === check) {
                    $("#checkboxall").prop("checked", true)
                }
            })
        })
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token)
                }
            }
        })
        id_array = new Array()
        $.base64.utf8encode = true;
        $.base64.utf8decode = true;
        //下拉菜单
        $('#ddm-types').on('click', function (e) {
            var $target = $(e.target)
            $target.is('a') && $('button#dropdown_devtype').html($target.text() + '<span class="caret"></span>')
            var strbuild = encodeURIComponent($target.text(), "utf-8")
        })
        $("#ddm-online").on('click', function (e) {
            var $target = $(e.target)
            $target.is('a') && $('button#dropdown_devonline').html($target.text() + '<span class="caret"></span>')
        })
        $("button#adqbutton").on('click', function () {
            var teststr = "5YWo6YOo"
            var devtype = encodeURIComponent($.base64.encode($('#dropdown_devtype').text()), 'utf-8')
            var devonline = encodeURIComponent($.base64.encode($('#dropdown_devonline').text()), 'utf-8')
            if (devtype == teststr) {
                devtype = ""
                if (devonline == teststr) {
                    devonline = ""
                }
            } else if (devonline == teststr) {
                devonline = ""
            }
            window.open($SCRIPT_ROOT + "admin/dvrmanage/list?devtype=" + devtype + "&devonline=" + devonline)
        })
        $("button#indexsbutton").on('click', function () {
            //搜索
            var keyword = $("input#indexserach").val()
            window.open(Flask.url_for('adminbg.dvrsearch') + "?keyword=" + encodeURIComponent($.base64.encode(keyword)))
        })
        //页面跳转
        $('button.dvrsearch').click(function () {
            var page = $('#transfer_page').val();
            window.location.href = Flask.url_for('adminbg.dvrsearch', {
                keyword: keyword_url
            }) + "&page=" + page;
        })
        $('button.dvrlist').click(function () {
            var page = $('#transfer_page').val();
            window.location.href = Flask.url_for('adminbg.dvrmanagelist', {
                devtype: devtype_info,
                devonline: devonline_info
            }) + "&page=" + page;
        })
        $('button.dvrmanage').click(function () {
            var page = $('#transfer_page').val();
            window.location.href = Flask.url_for('adminbg.dvrmanage') + "?page=" + page;
        })
        $("a.dvrsajaxnet").bind('click', function () {
            //list加载下一页
            $(this).text("正在加载，请稍后……")
            var pagenum = $("li#pnactive>a").text()
            var datacount = $("tr.jsondata").length

            var word = $.base64.encode(keyword)
            var serach = encodeURIComponent(word, 'utf-8')
            var posturl = Flask.url_for('adminbg.dvrsearch')
            $.post(posturl, {
                count: datacount,
                pagenum: pagenum,
                keyword: serach
            }, function (data) {
                var trc = ""
                var tra = '<tr class="jsondata">'
                var trb = '</tr>'
                $.each(data, function (one) {
                    eachone = data[one]
                    trc += tra + "<td>" + eachone.ID + "</td><td>" + eachone.DeviceName + "</td><td>" + eachone.DeviceCategory + "</td><td>" + eachone.DeviceSN + "</td><td>" + eachone.DeviceCondition + "</td><td>" + eachone.DeviceID + "</td><td>" + "<button onclick='' type'button' class='btn btn-link inline_button_link'>管理</button>" + "</td>" + trb
                    hasnext = eachone.next
                })
                $("table#devinfolist>tbody tr:last-child").after(trc)
                if (!hasnext) {
                    $("a.dvrsajaxnet").remove()
                } else {
                    $("a.dvrsajaxnet").text('下一页')
                }
            }).fail(function (status) {
                if (status.status == '404') {
                    $("a.dvrsajaxnet").remove()
                }
            })
        })

        $("a.dvrlistajaxnet").bind('click', function () {
            $(this).text("正在加载，请稍后……")
            var pagenum = $("li#pnactive>a").text()
            var datacount = $("tr.jsondata").length
            var devtype = encodeURIComponent($.base64.encode($('#dropdown_devtype').text()), 'utf-8')
            var devonline = encodeURIComponent($.base64.encode($('#dropdown_devonline').text()), 'utf-8')
            var posturl = Flask.url_for('adminbg.dvrmanagelist', {
                devtype: devtype_info,
                devonline: devonline_info
            })
            $.post(posturl, {
                count: datacount,
                pagenum: pagenum,
                devtype: devtype,
                devonline: devonline
            }, function (data) {
                var trc = ""
                var tra = '<tr class="jsondata">'
                var trb = '</tr>'
                $.each(data, function (one) {
                    eachone = data[one]
                    trc += tra + "<td>" + eachone.ID + "</td><td><input id='oper-" + eachone.ID + "' type='checkbox' name='oper' value='" + eachone.ID + "' /></td><td>" + eachone.DeviceName + "</td><td>" + eachone.DeviceCategory + "</td><td>" + eachone.DeviceSN + "</td><td>" + eachone.DeviceCondition + "</td><td>" + eachone.DeviceID + "</td><td>" + "<button onclick='' type'button' class='btn btn-link inline_button_link'>管理</button>" + "</td>" + trb
                    hasnext = eachone.next
                })
                $("table#devinfolist>tbody tr:last-child").after(trc)
                if (!hasnext) {
                    $("a.dvrlistajaxnet").remove()
                } else {
                    $("a.dvrlistajaxnet").text('下一页')
                }
            }).fail(function (status) {
                if (status.status == '404') {
                    $("a.dvrlistajaxnet").remove()
                }
            })
        })
        $("a.dvrmanageajax").bind('click', function () {
            //list加载下一页
            $(this).text("正在加载，请稍后……")
            var pagenum = $("li#pnactive>a").text()
            var datacount = $("tr.jsondata").length
            var posturl = Flask.url_for('adminbg.dvrmanage')
            $.post(posturl, {
                count: datacount,
                pagenum: pagenum
            }, function (data) {
                var trc = ""
                var tra = '<tr class="jsondata">'
                var trb = '</tr>'
                $.each(data, function (one) {
                    eachone = data[one]
                    trc += tra + "<td>" + eachone.ID + "</td><td><input id='oper-" + eachone.ID + "' type='checkbox' name='oper' value='" + eachone.ID + "' /></td><td>" + eachone.DeviceName + "</td><td>" + eachone.DeviceCategory + "</td><td>" + eachone.DeviceSN + "</td><td>" + eachone.DeviceCondition + "</td><td>" + eachone.DeviceID + "</td><td>" + "<button onclick='' type'button' class='btn btn-link inline_button_link'>管理</button>" + "</td>" + trb
                    hasnext = eachone.next
                })
                $("table#devinfolist>tbody tr:last-child").after(trc)
                if (!hasnext) {
                    $("a.dvrmanageajax").remove()
                } else {
                    $("a.dvrmanageajax").text('下一页')
                }
            }).fail(function (status) {
                if (status.status == '404') {
                    $("a.dvrmanageajax").remove()
                }
            })
        })

        $(document).on("click", "a.devaddspan", function () {
            var tParent = $(this).parent()
            var devtype_selete = tParent.siblings().find("#devadd_type")
            var devputaway_selete = tParent.siblings().find("#devadd_putaway")
            var cbl_tr = $(this).parents().find(".devselect")
            var clone = $(this).parents("tr.devadd_newtable").clone()
            var devadd_td = $(this).parent().prevAll()
            var td_id = $(".td_id:last")
            var new_td_id = parseInt(td_id.text()) + 1
            clone.find("td.td_id").text(new_td_id)
            var selectedValue_putaway = devputaway_selete.val()
            clone.find("option[value = '" + selectedValue_putaway + "']").attr("selected", "selected")
            var selectedValue_Type = devtype_selete.val()
            clone.find("option[value = '" + selectedValue_Type + "']").attr("selected", "selected")
            var selectedValue_Campus = cbl_tr.find("select#devadd_campus").val()
            clone.find("option[value = '" + selectedValue_Campus + "']").attr("selected", "selected")
            var selectedValue_build = cbl_tr.find("select#devadd_build").val()
            clone.find("option[value = '" + selectedValue_build + "']").attr("selected", "selected")
            var selectedValue_lvrno = cbl_tr.find("select#devadd_lvr").val()
            clone.find("option[value = '" + selectedValue_lvrno + "']").attr("selected", "selected")
            $("table#devadd_table > tbody").append(clone)
            
        });

        $(document).on("click", "a.devdelspan", function () {
            if ($("td.devadd_newtd").length == 1) {
                alert("新增行只有1行时不得删除")
            } else {
                $(this).parents("td.devadd_newtd").remove()
            }
        });

        $(document).on("change", "select#devadd_campus", function () {
            var $v = $(this)
            var $build = $v.parent().next().children()
            if ($v.val() == "") {
                $build.append('<option value="">请选择楼宇</option>')
            } else {
                $build.empty()
            }
            js_dvr_querybuild($v.val(), $build)
        })

        $(document).on("change", "select#devadd_build", function () {
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

        $(document).on("change", "select#devadd_putaway", function () {
            var v = $(this).parent()
            var twotable = v.parent().siblings(".devtr_hide")
            var inputtable = v.parent().siblings(".devadd_trinput")
            var cbl_selete = inputtable.find("select")
            var haip = inputtable.find("input")
            if ($(this).val() == "N") {
                twotable.each(
                    function(){
                        $(this).attr("style", "display: none") // 显隐
                    }
                )
                cbl_selete.each(function(){
                    $(this).attr("disabled", "disabled")
                    $(this).find("option:first").attr("selected", "selected")
                })
                haip.each(function(){
                    $(this).val("")
                    $(this).attr("disabled", "disabled")
                    $(this).removeAttr("style")
                    $(this).val("")
                    
                })
            }else {
                twotable.each(
                    function(){
                        $(this).attr("style", "display: table-row")
                    }
                )
                cbl_selete.each(function(){
                    $(this).removeAttr("disabled", "disabled")
                    $(this).find("option:first").attr("selected", "selected")
                })
                haip.each(function(){
                    $(this).removeAttr("disabled", "disabled")
                    $(this).val("")
                })
            }
        })
    }
)

function js_dvr_batchd() {
    if ($("select#ipage").val() == "delete") {
        $("[name='oper']").each(function () {
            if ($(this).prop('checked')) {
                delarray = js_dvr_idarry($(this).val())
            }
        })
        js_dvr_delDevice(delarray)
    } else if ($("select#ipage").val() == "dvrup") {
        $("[name='oper']").each(function () {
            if ($(this).prop('checked')) {
                uparray = js_dvr_idarry($(this).val())
            }
        })
        js_dvr_putaway(uparray, "up")
    } else if ($("select#ipage").val() == "dvrdown") {
        $("[name='oper']").each(function () {
            if ($(this).prop('checked')) {
                downarray = js_dvr_idarry($(this).val())
            }
        })
        js_dvr_putaway(downarray, "down")
    }
}
function js_dvr_create() {
    var url = Flask.url_for('adminbg.dvrmanage_add')
    layer_add = layer.open({
        type: 2,
        skin: 'layui-layer-rim',
        title: "创建新设备",
        area: ['1050px', '500px'],
        content: url
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


function js_dvr_add() {
    var dvrinfo = $("td.devadd_newtd")
    var dvrinfo_datas = []
    dvrinfo.each(function(){
        var dvrinfo_data = {}
        dvrinfo_data["name"] = $(this).find("#devadd_name").val()
        dvrinfo_data["type"] = $(this).find("#devadd_type").val()
        dvrinfo_data["serial"] = $(this).find("#devadd_serial").val()
        dvrinfo_data["id"] = $(this).find("#devadd_id").val()
        dvrinfo_data["putaway"] = $(this).find("#devadd_putaway").val()
        dvrinfo_data["campus"] = $(this).find("#devadd_campus").val()
        dvrinfo_data["build"] = $(this).find("#devadd_build").val()
        dvrinfo_data["hostname"] = $(this).find("#devadd_hostname").val()
        dvrinfo_data["addr"] = $(this).find("#devadd_addr").val()
        dvrinfo_data["ip"] = $(this).find("#devadd_upip").val()
        dvrinfo_data["port"] = $(this).find("#devadd_upport").val()
        dvrinfo_data["lvr"] = $(this).find("#devadd_lvr").val()
        dvrinfo_datas.push(dvrinfo_data)
    })
    if(dataCheak(dvrinfo_datas)){
        if(confirm('准备添加数据，是否继续？')){
            $.ajax({
                url: Flask.url_for('adminbg.dvrmanage_add'),
                type: 'POST',
                data: JSON.stringify(dvrinfo_datas),
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

function dataCheak(dvrinfo_datas){
    for (x in dvrinfo_datas){
        if (isNull(dvrinfo_datas[x].name)) {
            alert("存在未填写项，请核对数据。")
            return false
        }
        if (dvrinfo_datas[x].type == "devtype_null") {
            alert("存在未选择设备类型数据，请核对。")
            return false
        }
        if (isNull(dvrinfo_datas[x].serial)) {
            alert("存在未填写项，请核对数据。")
            return false
        }
        if (isNull(dvrinfo_datas[x].id)) {
            alert("存在未填写项，请核对数据。")
            return false
        }
        if (dvrinfo_datas[x].putaway == "Y") {
            if(dvrinfo_datas[x].campus == "campus_null"){
                alert("存在未选择校区数据，请核对。")
                return false
            }
            if(dvrinfo_datas[x].build == "campus_null"){
                alert("存在未选择楼宇数据，请核对。")
                return false
            }
            if(dvrinfo_datas[x].lvr == "lvr_null"){
                alert("存在未选择弱电间数据，请核对。")
                return false
            }
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


function js_dvr_idarry( id ){
    id_array.push(id)
    return id_array
}

function js_dvr_delDevice( idarray ){
    if(confirm("确定删除么？")){
        $.ajax({
            url: Flask.url_for('adminbg.devdeldevice'),
            type: "post",
            data: {
                array_id: JSON.stringify(idarray)
            },
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

function js_dvr_putaway( idarray, op, gop ) {
    if(op == "up"){
        if(idarray){
            if(gop == "post"){
                $.ajax({
                    url: Flask.url_for('adminbg.devup'),
                    type: "post",
                    data: {
                        array_id: JSON.stringify(idarray),
                        op: "post"
                    },
                    dataType: "json",
                    contentType: "application/json",
                    success: function(resp) {
                        console.log(resp)
                    }
                })
            }
            else{
                $.ajax({
                    url: Flask.url_for('adminbg.devup'),
                    type: "post",
                    data: {
                        array_id: JSON.stringify(idarray),
                        op: "get"
                    },
                    dataType: "html",
                    success: function(html) {
                        layer_devup = layer.open({
                            type: 1,
                            skin: 'layui-layer-rim',
                            title: "上架设备",
                            area: ['1050px', '500px'],
                            content: html
                        })
                    }
                })
            }
        }
    }else{
        if(confirm("确定进行操作么？")){
            $.ajax({
                url: Flask.url_for('adminbg.devdown'),
                type: "post",
                data: {
                    array_id: JSON.stringify(idarray),
                },
                dataType: "JSON",
                success: function(resp) {
                    if(resp.status != 1) {
                        alert("修改失败 ", + resp.message)
                        id_array.length = 0
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
