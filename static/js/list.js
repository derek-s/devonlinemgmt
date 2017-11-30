$(document).ready(
    function() {
        var str2;
        $.getJSON($SCRIPT_ROOT + 'list', {}, function(data) {
            $.each(data, function(one) {
                $("table#devinfolist>tbody").append('<tr class="jsondata"></tr>')
                eachone = data[one]
                $("table#devinfolist>tbody tr:last-child").append("<td>" + eachone.ID + "</td><td class='location'>" + eachone.Location + "</td><td>" + eachone.HostName + "</td><td>" + eachone.LAA + "</td><td>" + eachone.HigherlinkIP + "</td><td>" + eachone.HigherlinkPort + "</td><td class='model'>" + eachone.DeviceModel + "</td>")
            })
        })
        $("button#serach").bind('click', function() {
            strkey = encodeURI($('input[name="devinfoserp"]').val(), "utf-8")
            $.getJSON($SCRIPT_ROOT + '_querydevinfo', {
                keyword: strkey
            }, function(data) {
                $("tr.jsondata").empty()
                $.each(data, function(one) {
                    $("table#devinfolist>tbody").append('<tr class="jsondata"></tr>')
                    eachone = data[one]
                    $("table#devinfolist>tbody tr:last-child").append("<td>" + eachone.ID + "</td><td>" + eachone.Location + "</td><td>" + eachone.HostName + "</td><td>" + eachone.LAA + "</td><td>" + eachone.HigherlinkIP + "</td><td>" + eachone.HigherlinkPort + "</td><td class='model'>" + eachone.DeviceModel + "</td>")
                })
            });
            return false;
        })
        $("table#devinfolist>tbody").on('click', '.location', function() {
            var str2;
            var tablehead = "<table class='tabledevinfo table table-striped table-hover'><tbody><tr><th>序号</th><th>楼宇名称</th><th>楼栋号码</th><th>楼层</th><th>房间号</th><th>机柜数量</th></tr>"
            var tableend = "</tbody></table>"
            strkey1 = encodeURI($(this).html(), "utf-8")
            $.getJSON($SCRIPT_ROOT + '_querylvr', {
                keyword: strkey1
            }, function(data) {
                $.each(data, function(one) {
                    lvrinfo = data[one]
                    str2 = "<tr><td>" + lvrinfo.ID + "</td><td>" + lvrinfo.BuildName + "</td><td>" + lvrinfo.BuildNo + "</td><td>" + lvrinfo.FloorNo + "</td><td>" + lvrinfo.RoomNo + "</td><td>" + lvrinfo.Cabinet + "</td></tr>"
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
            var tablehead = "<table class='tabledevinfo table table-striped table-hover'><tbody><tr><th>序号</th><th>设备名称</th><th>设备分类</th><th>设备序列号</th><th>使用情况</th><th>唯一ID</th></tr>"
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
                    skin: 'layui-layer-rim', //加上边框
                    area: ['600px', '240px'], //宽高
                    content: tablehead + str2 + tableend
                });
            })


        })
    })