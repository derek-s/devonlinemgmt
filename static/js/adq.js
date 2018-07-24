$(document).ready(
    function() {
        $.base64.utf8encode = true;
        $.base64.utf8decode = true;
        $("a#ajaxntindex").bind('click', function() {
            //index加载下一页
            $(this).text("正在加载，请稍后……")
            var pagenum = $("li#pnactive>a").text()
            var datacount = $("tr.jsondata").length
            $.post($SCRIPT_ROOT + '_queryipage', {
                count: datacount,
                pagenum: pagenum
            }, function(data) {

                var trc = ""
                var tra = '<tr class="jsondata">'
                var trb = '</tr>'
                $.each(data, function(one) {
                    eachone = data[one]
                    trc += tra + "<td>" + eachone.ID + "</td><td>" + eachone.Campus + "</td><td>" + eachone.Location + "</td><td class='location'>" + eachone.RoomNo + "</td><td>" + eachone.HostName + "</td><td>" + eachone.LAA + "</td><td>" + eachone.HigherlinkIP + "</td><td>" + eachone.HigherlinkPort + "</td><td class='model'>" + eachone.DeviceModel + "</td>" + trb
                    hasnext = eachone.next
                })
                $("table#devinfolist>tbody tr:last-child").after(trc)
                if (!hasnext) {
                    $("a#ajaxntindex").remove()
                } else {
                    $("a#ajaxntindex").text('下一页')
                }
            }).fail(function(status) {
                if (status.status == '404') {
                    $("a#ajaxntindex").remove()
                }
            })
            $(this).text("下一页")
        })
        $("a#ajaxntlist").bind('click', function() {
            //list加载下一页
            $(this).text("正在加载，请稍后……")
            var pagenum = $("li#pnactive>a").text()
            var datacount = $("tr.jsondata").length
            var ajaxcnameen = encodeURIComponent(ajaxcamname, 'utf-8')
            var ajaxbnameen = encodeURIComponent(ajaxbilname, 'utf-8')
            $.post($SCRIPT_ROOT + '_qindexlist', {
                count: datacount,
                pagenum: pagenum,
                campusname: ajaxcnameen,
                buildname: ajaxbnameen,
            }, function(data) {
                var trc = ""
                var tra = '<tr class="jsondata">'
                var trb = '</tr>'
                $.each(data, function(one) {
                    eachone = data[one]
                    trc += tra + "<td>" + eachone.ID + "</td><td>" + eachone.Campus + "</td><td>" 
                    + eachone.Location + "</td><td class='location'>" + eachone.RoomNo + "</td><td>" 
                    + eachone.HostName + "</td><td>" + eachone.LAA + "</td><td>" + eachone.HigherlinkIP 
                    + "</td><td>" + eachone.HigherlinkPort + "</td><td class='model'>" 
                    + eachone.DeviceModel + "</td>" + trb
                    hasnext = eachone.next
                })
                $("table#devinfolist>tbody tr:last-child").after(trc)
                if (!hasnext) {
                    $("a#ajaxntlist").remove()
                } else {
                    $("a#ajaxntlist").text('下一页')
                }
            }).fail(function(status) {
                if (status.status == '404') {
                    $("a#ajaxntlist").remove()
                }
            })
        })
        $("table#devinfolist>tbody").on('click', '.location', function() {
            //弱电间详情
            var str2;
            var tablehead = '<table class="tabledevinfo table table-striped table-hover"><tbody><tr><th>ID</th><th>校区</th><th>楼宇名称</th><th>楼栋号码</th><th>楼层</th><th>房间号</th><th>机柜数量</th><th>弱电间编号</th></tr>'
            var tableend = "</tbody></table>"
            var campus = encodeURIComponent($(this).prev().prev().text(), "utf-8")
            var location = encodeURIComponent($(this).prev().text(), "utf-8")
            var roomno = encodeURIComponent($(this).text(), "utf-8")
            $.post($SCRIPT_ROOT + '_querylvr', {
                campus: campus,
                location: location,
                roomno: roomno
            }, function(data) {
                $.each(data, function(one) {
                    lvrinfo = data[one]
                    str2 = "<tr><td>" + lvrinfo.ID + "</td><td>" + lvrinfo.Campus + "</td><td>" + lvrinfo.BuildName + "</td><td>" + lvrinfo.BuildNo + "</td><td>" + lvrinfo.FloorNo + "</td><td>" + lvrinfo.RoomNo + "</td><td>" + lvrinfo.Cabinet + "</td><td>" + lvrinfo.LVRNo + "</td></tr>"
                })

                layer.open({
                    title: '弱电间信息',
                    type: 1,
                    skin: 'layui-layer-rim',
                    area: ['600px', '240px'],
                    content: tablehead + str2 + tableend
                });
            })
        })
        $("table#devinfolist>tbody").on('click', '.model', function() {
            //设备详情
            var str2;
            var tablehead = '<table class="tabledevinfo table table-striped table-hover"><tbody><tr><th>序号</th><th>设备名称</th><th>设备分类</th><th>设备序列号</th><th>使用情况</th><th>唯一ID</th></tr>'
            var tableend = "</tbody></table>"
            strkey1 = encodeURIComponent($(this).html(), "utf-8")
            $.post($SCRIPT_ROOT + '_querydev', {
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
        $("button#adqbutton").on('click', function() {
            //分类查询
            var teststr = "5YWo6YOo"
            var campusname = encodeURIComponent(($.base64.encode($("#dropdownCampus").text())), 'utf-8')
            var buildname = encodeURIComponent(($.base64.encode($("#dropdownBuild").text())), 'utf-8')
            if (campusname == teststr) {
                campusname = ""
                if (buildname == teststr) {
                    buildname = ""
                }
            } else if (buildname == teststr) {
                buildname = ""
            }
            window.open($SCRIPT_ROOT + "admin/query/list?campusname=" + campusname + "&buildname=" + buildname)
        })
        
        $("a#ajaxntserach").on('click', function() {
            //搜索页ajax
            $(this).text("正在加载，请稍后……")
            var pagenum = $("li#pnactive>a").text()
            var datacount = $("tr.jsondata").length
            var word = $.base64.encode(ajaxkeyword)
            var serach = encodeURIComponent(word, 'utf-8')
            $.post($SCRIPT_ROOT + '_qserach', {
                count: datacount,
                pagenum: pagenum,
                keyword: serach
            }, function(data) {
                var trc = ""
                var tra = '<tr class="jsondata">'
                var trb = '</tr>'
                $.each(data, function(one) {
                    eachone = data[one]
                    trc += tra + "<td>" + eachone.ID + "</td><td>" + eachone.Campus + "</td><td>" + eachone.Location + "</td><td class='location'>" + eachone.RoomNo + "</td><td>" + eachone.HostName + "</td><td>" + eachone.LAA + "</td><td>" + eachone.HigherlinkIP + "</td><td>" + eachone.HigherlinkPort + "</td><td class='model'>" + eachone.DeviceModel + "</td>" + trb
                    hasnext = eachone.next
                })
                $("table#devinfolist>tbody tr:last-child").after(trc)
                if (!hasnext) {
                    $("a#ajaxntserach").remove()
                } else {
                    $("a#ajaxntserach").text('下一页')
                }
            }).fail(function(status) {
                if (status.status == '404') {
                    $("a#ajaxntserach").remove()
                }
            })
        })
    }
)