$(document).ready(
    function() {
        $("#checkboxall").click(function () {
            if ($("#checkboxall").prop("checked")) {
                $("[name='oper']").prop("checked", true)
            } else {
                $("[name='oper']").prop("checked", false)
            }
        })
        $("[name='oper']").click(function () {
            $("[name='oper']").each(function(){
                console.log(($(this)).text())
            })
            if ($("#checkboxall").prop("checked")) {
                $("#checkboxall").prop("checked", false)
            }
            if ($("[name='oper']").prop("checked")) {
                
            }
        })
        
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

function js_dvr_batchd() {
    url = self.location.href.split("&")[0].split("?")[0]
    if ($("select#ipage").val() == "delete") {
        $("[name='oper']").each(function () {
            if ($(this).prop('checked')) {
                console.log("add id")
            }
        })
        console.log("delete id")
    }else if($("select#ipage").val() == "dvrup"){
        console.log("dvrup")
    }else if($("select#ipage").val() == "dvrdown"){
        console.log("dvrdown")
    }
}