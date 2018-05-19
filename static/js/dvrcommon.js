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
            var clone = $(this).parent().parent().clone()
            var devadd_td = $(this).parent().prevAll()
            var selectedValue_putaway = devadd_td.children("select#devadd_putaway").val()
            clone.find("option[value = '" + selectedValue_putaway + "']").attr("selected", "selected")
            var selectedValue_Type = devadd_td.children("select#devadd_type").val()
            clone.find("option[value = '" + selectedValue_Type + "']").attr("selected", "selected")
            var selectedValue_Campus = devadd_td.children("select#devadd_campus").val()
            clone.find("option[value = '" + selectedValue_Campus + "']").attr("selected", "selected")
            var selectedValue_Lvrno = devadd_td.children("select#devadd_build").val()
            clone.find("option[value = '" + selectedValue_Lvrno + "']").attr("selected", "selected")
            $("table#devadd_table > tbody").append(clone)
        });

        $(document).on("click", "a.devdelspan", function () {
            if ($("tr.devadd_newline").length == 1) {
                alert("新增行只有1行时不得删除")
            } else {
                $("table#devadd_table > tbody").append(this.parentElement.parentElement.remove())
            }
        });

        $(document).on("change", "select#devadd_campus", function () {
            var $v = $(this)
            var $lvr = $v.parent().next().children()
            if ($v.val() == "") {
                $lvr.append('<option value="">请选择弱电间</option>')
            } else {
                $lvr.empty()
            }
            js_dvr_querylvr($v.val(), $lvr)
        })

        $(document).on("change", "select#devadd_putaway", function () {
            var $v = $(this)
            var $selectCB = $v.parent().nextAll()
            var campus = $selectCB.children("select#devadd_campus")
            var lvr = $selectCB.children("select#devadd_build")
            if ($v.val() == "N") {
                campus.attr("disabled", "disabled")
                lvr.attr("disabled", "disabled")
            }else {
                campus.find("option[value='']").attr("selected", "selected")
                campus.removeAttr("disabled")
                lvr.find("option[value='']").attr("selected", "selected")
                lvr.removeAttr("disabled")
            }
        })
    }
)

function js_dvr_batchd() {
    url = self.location.href.split("&")[0].split("?")[0]
    if ($("select#ipage").val() == "delete") {
        $("[name='oper']").each(function () {
            if ($(this).prop('checked')) {
                console.log("add id")
            }
        })
        console.log("delete id")
    } else if ($("select#ipage").val() == "dvrup") {
        console.log("dvrup")
    } else if ($("select#ipage").val() == "dvrdown") {
        console.log("dvrdown")
    }
}

function js_dvr_create() {
    var url = Flask.url_for('adminbg.dvrmanage_add')
    console.log(url)
    layer.open({
        type: 2,
        skin: 'layui-layer-rim',
        title: "创建新设备",
        area: ['1230px', '400px'],
        content: url
    })
}

function js_dvr_querylvr(campus_name, nextLvrElement) {
    var posturl = Flask.url_for('adminbg.devquerylvr')
    var campusb64 = encodeURIComponent($.base64.encode(campus_name), 'utf-8')
    $.post(posturl, {
        campus: campusb64
    }, function (data) {
        if (data.length != 0){
            $.each(data, function (one) {
                eachone = data[one]
                nextLvrElement.append('<option value="'+ eachone.LVRNo +'">'+ eachone.LVRNo +'</option>')
            })
        } else if (campus_name == "campus_null"){
            nextLvrElement.append('<option value="lvr_null">请选择弱电间</option>')
        } else {
            nextLvrElement.append('<option value="lvr_null">该校区暂无弱电间信息</option>')
        }
    }).fail(function (status) {
        console.log(status)
        if (status.status == '404') {
            $("a.dvrmanageajax").remove()
        }
    })
}


function js_dvr_add() {
    var dvrinfo = $("tr.devadd_newline")
    var dvrinfo_datas = []
    dvrinfo.each(function(){
        var dvrinfo_data = {}
        dvrinfo_data["name"] = $(this).find("#devadd_name").val()
        dvrinfo_data["type"] = $(this).find("#devadd_type").val()
        dvrinfo_data["serial"] = $(this).find("#devadd_serial").val()
        dvrinfo_data["id"] = $(this).find("#devadd_id").val()
        dvrinfo_data["putaway"] = $(this).find("#devadd_putaway").val()
        dvrinfo_data["campus"] = $(this).find("#devadd_campus").val()
        dvrinfo_data["lvr"] = $(this).find("#devadd_build").val()
        dvrinfo_datas.push(dvrinfo_data)
    })
    if(dataCheak(dvrinfo_datas)){
        console.log(JSON.stringify(dvrinfo_datas))
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