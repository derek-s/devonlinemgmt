$(document).ready(
    function() {
        $.getJSON($SCRIPT_ROOT + '_querybuild', {
            campusname: ''
        }, function(data) {
            $.each(data, function(one) {
                $('#ddm-buildname').append(
                    '<li class="ajaxbname"><a href="javascript:void(0);">' + data[one].BuildName + '</a></li>'
                )
            })
        })
        $('#ddm-campus').on('click', function(e) {
            $('li.ajaxbname').remove()
            $('button#dropdownMenu2').html('全部' + '<span class="caret"></span>')
            var $target = $(e.target)
            $target.is('a') && $('button#dropdownMenu1').html($target.text() + '<span class="caret"></span>')
            var strbuild = encodeURI($target.text(), "utf-8")
            if ($target.text() == '全部') {
                strbuild = ""
            }
            $.getJSON($SCRIPT_ROOT + '_querybuild', {
                campusname: strbuild
            }, function(data) {
                $.each(data, function(one) {
                    $('#ddm-buildname').append(
                        '<li class="ajaxbname"><a href="javascript:void(0);">' + data[one].BuildName + '</a></li>'
                    )
                })
            })
        })
        $("#ddm-buildname").on('click', function(e) {
            var $target = $(e.target)
            $target.is('a') && $('button#dropdownMenu2').html($target.text() + '<span class="caret"></span>')
        })
        $("a#ajaxnext").bind('click', function() {
            $(this).text("正在加载，请稍后……")
            pagenum = $("li.active>a").text()
            datacount = $("tr.jsondata").length
            textabc = $.getJSON($SCRIPT_ROOT + '_queryipage', {
                count: datacount,
                pagenum: pagenum
            }, function(data) {

                trc = ""
                var tra = '<tr class="jsondata">'
                var trb = '</tr>'
                $.each(data, function(one) {
                    eachone = data[one]
                    trc += tra + "<td>" + eachone.ID + "</td><td>" + eachone.Campus + "</td><td>" + eachone.Location + "</td><td class='location'>" + eachone.RoomNo + "</td><td>" + eachone.HostName + "</td><td>" + eachone.LAA + "</td><td>" + eachone.HigherlinkIP + "</td><td>" + eachone.HigherlinkPort + "</td><td class='model'>" + eachone.DeviceModel + "</td>" + trb
                    hasnext = eachone.next
                })
                $("table#devinfolist>tbody tr:last-child").after(trc)
                if (!hasnext) {
                    $("a#ajaxnext").remove()
                } else {
                    $("a#ajaxnext").text('下一页')
                }
            }).fail(function(status) {
                if (status.status == '404') {
                    $("a#ajaxnext").remove()
                }
            })
        })
        $("table#devinfolist>tbody").on('click', '.location', function() {
            var str2;
            var tablehead = '<table class="tabledevinfo table table-striped table-hover"><tbody><tr><th>ID</th><th>校区</th><th>楼宇名称</th><th>楼栋号码</th><th>楼层</th><th>房间号</th><th>机柜数量</th></tr>'
            var tableend = "</tbody></table>"
            var campus = encodeURI($(this).prev().prev().text(), "utf-8")
            var location = encodeURI($(this).prev().text(), "utf-8")
            var roomno = encodeURI($(this).text(), "utf-8")
            console.log(campus, location, roomno)
            $.getJSON($SCRIPT_ROOT + '_querylvr', {
                campus: campus,
                location: location,
                roomno: roomno
            }, function(data) {
                $.each(data, function(one) {
                    lvrinfo = data[one]
                    str2 = "<tr><td>" + lvrinfo.ID + "</td><td>" + lvrinfo.Campus + "</td><td>" + lvrinfo.BuildName + "</td><td>" + lvrinfo.BuildNo + "</td><td>" + lvrinfo.FloorNo + "</td><td>" + lvrinfo.RoomNo + "</td><td>" + lvrinfo.Cabinet + "</td></tr>"
                })

                layer.open({
                    title: '弱电间信息',
                    type: 1,
                    skin: 'layui-layer-rim',
                    area: ['500px', '240px'],
                    content: tablehead + str2 + tableend
                });
            })
        })
        $("table#devinfolist>tbody").on('click', '.model', function() {
            var str2;
            var tablehead = '<table class="tabledevinfo table table-striped table-hover"><tbody><tr><th>序号</th><th>设备名称</th><th>设备分类</th><th>设备序列号</th><th>使用情况</th><th>唯一ID</th></tr>'
            var tableend = "</tbody></table>"
            strkey1 = encodeURI($(this).html(), "utf-8")
            $.getJSON($SCRIPT_ROOT + '_querydev', {
                keyword: strkey1
            }, function(data) {
                $.each(data, function(one) {
                    devinfo = data[one]
                    str2 = "<tr><td>" + devinfo.ID + "</td><td>" + devinfo.DeviceName + "</td><td>" + devinfo.DeviceCategory + "</td><td>" + devinfo.DeviceSN + "</td><td>" + devinfo.DeviceCondition + "</td><td>" + devinfo.DeviceID + "</td></tr>"
                })

                layer.open({
                    title: '设备信息',
                    type: 1,
                    skin: 'layui-layer-rim',
                    area: ['600px', '240px'],
                    content: tablehead + str2 + tableend
                });
            })
        })
    }
)