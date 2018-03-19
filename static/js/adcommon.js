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
        if ($('#dropdownCampus').text() == "全部") {
            $("button#dropdownBuild").attr('disabled',true); 
        }else{
            $("button#dropdownBuild").attr('disabled',false); 
        }
        $('#ddm-campus').on('click', function(e) {
            $('li.ajaxbname').remove()
            $('button#dropdownBuild').html('全部' + '<span class="caret"></span>')
            var $target = $(e.target)
            $target.is('a') && $('button#dropdownCampus').html($target.text() + '<span class="caret"></span>')
            var strbuild = encodeURIComponent($target.text(), "utf-8")
            if ($target.text() == '全部') {
                strbuild = "";
                console.log("1")
                $("button#dropdownBuild").attr('disabled',true); 
            }else{
                $.post($SCRIPT_ROOT + '_querybuild', {
                    campusname: strbuild
                }, function(data) {
                    $.each(data, function(one) {
                        $('#ddm-buildname').append(
                            '<li class="ajaxbname"><a href="javascript:void(0);">' + data[one].BuildName + '</a></li>'
                        )
                    })
                })
                
                $("button#dropdownBuild").attr('disabled',false); 
            }
        })
        $("#ddm-buildname").on('click', function(e) {
            var $target = $(e.target)
            $target.is('a') && $('button#dropdownBuild').html($target.text() + '<span class="caret"></span>')
        })
    }
)