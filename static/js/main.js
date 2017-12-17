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
            var uname = encodeURIComponent(($.base64.encode($("input#logusers").text())), "utf-8")
            var catname = encodeURIComponent(($.base64.encode($("#dropdownlogs").text())), 'utf-8')
            console.log($("input#logusers").val())
            if (catname == teststr) {
                catname = ""
            }
            $.post($SCRIPT_ROOT + 'log', {
                page: page,
                username: uname,
                cats: catname
            }, function(data) {
                /* $("div#rightcont").empty()
                 var divmain = ($(data)).filter("div#main")
                 $("div#rightcont").append(divmain.find("div#rightcont").html()) */
            })
        })
    }
)

function js_ajaxlog(page) {
    $.post($SCRIPT_ROOT + 'log', {
        page: page

    }, function(data) {
        $("div#rightcont").empty()
        var divmain = ($(data)).filter("div#main")
        $("div#rightcont").append(divmain.find("div#rightcont").html())
    })
}