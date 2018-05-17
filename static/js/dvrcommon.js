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
            console.log(1)
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
            var selectedValue_Campus = $(this).parent().prevAll().children("select#devadd_campus").val()
            clone.find("option[value = '" + selectedValue_Campus + "']").attr("selected", "selected")
            var selectedValue_Lvrno = $(this).parent().prevAll().children("select#devadd_build").val()
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
            if ($v.val() == "n") {
                $selectCB.children("select#devadd_campus").attr("disabled", "disabled")
                $selectCB.children("select#devadd_build").attr("disabled", "disabled")
            }else {
                $selectCB.children("select#devadd_campus").removeAttr("disabled")
                $selectCB.children("select#devadd_build").removeAttr("disabled")
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
    layer.open({
        type: 1,
        skin: 'layui-layer-rim',
        title: "创建新设备",
        area: ['500px', '300px'],
        content: "测试"


    })
}

function js_dvr_querylvr(campus_name, nextLvrElement) {
    var posturl = Flask.url_for('adminbg.devquerylvr')
    var campusb64 = encodeURIComponent($.base64.encode(campus_name), 'utf-8')
    $.post(posturl, {
        campus: campusb64
    }, function (data) {
        $.each(data, function (one) {
            eachone = data[one]
            nextLvrElement.append('<option value="' + eachone.LVRNo + '">' + eachone.LVRNo + '</option>')
        })
    }).fail(function (status) {
        if (status.status == '404') {
            $("a.dvrmanageajax").remove()
        }
    })
}
