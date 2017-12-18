$(document).ready(
    function() {
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
            var page = 1
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