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
        $('#ddm-types').on('click', function(e) {
            var $target = $(e.target)
            $target.is('a') && $('button#dropdown_devtype').html($target.text() + '<span class="caret"></span>')
            var strbuild = encodeURIComponent($target.text(), "utf-8")
        })
        $("#ddm-online").on('click', function(e) {
            var $target = $(e.target)
            $target.is('a') && $('button#dropdown_devonline').html($target.text() + '<span class="caret"></span>')
        })
        $("button#adqbutton").on('click', function(){
            var teststr = "5YWo6YOo"
            var devtype = encodeURIComponent($.base64.encode($('#dropdown_devtype').text()), 'utf-8')
            var devonline = encodeURIComponent($.base64.encode($('#dropdown_devonline').text()), 'utf-8')
            if (devtype == teststr){
                devtype = ""
                if (devonline == teststr){
                    devonline = ""
                }
            }else if (devonline == teststr){
                devonline = ""
            }
            window.open($SCRIPT_ROOT + "admin/dvrmanage/list?devtype=" + devtype + "&devonline=" + devonline)
        })
    }
)