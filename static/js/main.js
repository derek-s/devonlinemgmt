$(document).ready(
    function() {
        path =
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrf_token)
                    }
                }
            })
        $.base64.utf8encode = true;
        $.base64.utf8decode = true;
        //下拉菜单
        $("#ddm-logs").on('click', function(e) {
            var $target = $(e.target)
            $target.is('a') && $('button#dropdownlogs').html($target.text() + '<span class="caret"></span>')
        })
        $("button#logqbutton").on('click', function() {
            var teststr = "5YWo6YOo"
            var page = ""
            var name = $("input#logusers").val()
            var cat = $("#dropdownlogs").text()
            var uname = encodeURIComponent(($.base64.encode(name)), "utf-8")
            var catname = encodeURIComponent(($.base64.encode(cat)), 'utf-8')
            var datas = $("input#logdatas").val()
            if (catname == teststr) {
                catname = ""
            }
            js_ajaxlog(page, uname, catname, datas)
        })
    }
)
$(document).on("click", "button#transferlogs", function() {
    var teststr = "5YWo6YOo"
    var page = $("input#transfer_pagelog").val()
    var name = $("input#logusers").val()
    var cat = $("#dropdownlogs").text()
    var uname = encodeURIComponent(($.base64.encode(name)), "utf-8")
    var catname = encodeURIComponent(($.base64.encode(cat)), 'utf-8')
    var datas = $("input#logdatas").val()
    if (catname == teststr) {
        catname = ""
    }
    js_ajaxlog(page, uname, catname, datas)
});

function js_ajaxlog(page, uname, catname, datas) {
    var loading = layer.load(2, {
        shade: [0.3, '#fff']
    });
    $.post($SCRIPT_ROOT + 'log', {
        page: page,
        username: uname,
        cats: catname,
        date: datas
    }, function(data) {
        $("div#logtable").empty()
        var divmain = ($(data)).filter("div#main")
        $("div#logtable").append(divmain.find("div#logtable").html())
    })
    layer.close(loading);
}

function check(snum) {
    if (snum != "") {
        if (snum.indexOf(" ") > -1) {
            warningf("输入中包含空格")
            return false
        }
        return checknum(snum)
    } else {
        warningf("输入框不能为空")
        return false
    }
}

function checknum(sum) {
    if (!isNaN(sum)) {
        return true
    } else {
        warningf("请输入数字")
        return false
    }
}

function warningf(stra) {
    var warning = $("#warning")
    warning.removeClass("disno")
    warning.html(stra)
}

function js_ajaxnotes(page, uname, catname, datas) {
    var loading = layer.load(2, {
        shade: [0.3, '#fff']
    });

    $.post($SCRIPT_ROOT + 'notelist', {
        page: page,
        cuser: catname,
        aname: uname,
        cdata: datas
    }, function(data) {
        $("div#logtable").empty()
        var divmain = ($(data)).filter("div#main")
        $("div#logtable").append(divmain.find("div#logtable").html())
    })
    layer.close(loading);
}


$(document).on("click", "button#noticequery", function() {
    var teststr = "5YWo6YOo"
    var page = $("input#transfer_pagelog").val()
    var name = $("input#nnameinput").val()
    var cat = $("input#ncnameinput").val()
    var uname = encodeURIComponent(($.base64.encode(name)), "utf-8")
    var catname = encodeURIComponent(($.base64.encode(cat)), 'utf-8')
    var datas = $("input#ndatas").val()
    if (catname == teststr) {
        catname = ""
    }
    console.log(page, uname, catname.datas)
    js_ajaxnotes(page, uname, catname, datas)
});


function js_delete(id) {
    $.ajax({
        url: $PATH_ROOT + "/" + id + "/delete",
        type: "POST",
        dateType: "json",
        success: function(resp) {
            resp = JSON.parse(resp)
            if (resp.status != 1) {
                alert("删除失败")
            }
            alert("删除成功")
            location.reload()
        }
    })
}