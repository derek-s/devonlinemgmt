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