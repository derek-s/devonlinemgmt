$(document).ready(
    function() {
        $.getJSON($SCRIPT_ROOT + 'list', {}, function(data) {
            $.each(data, function(one) {
                $("table#devinfolist>tbody").append('<tr class="jsondata"></tr>')
                eachone = data[one]
                $("table#devinfolist>tbody tr:last-child").append("<td>" + eachone.ID + "</td><td>" + eachone.Location + "</td><td>" + eachone.HostName + "</td><td>" + eachone.LAA + "</td><td>" + eachone.HigherlinkIP + "</td><td>" + eachone.HigherlinkPort + "</td><td>" + eachone.DeviceModel + "</td>")
            })
        })
        $("button#serach").bind('click', function() {
            var strkey = encodeURI($('input[name="devinfoserp"]').val(), "utf-8")
            $.getJSON($SCRIPT_ROOT + '_querydevinfo', {
                keyword: strkey
            }, function(data) {
                $("tr.jsondata").empty()
                $.each(data, function(one) {
                    $("table#devinfolist>tbody").append('<tr class="jsondata"></tr>')
                    eachone = data[one]
                    $("table#devinfolist>tbody tr:last-child").append("<td>" + eachone.ID + "</td><td>" + eachone.Location + "</td><td>" + eachone.HostName + "</td><td>" + eachone.LAA + "</td><td>" + eachone.HigherlinkIP + "</td><td>" + eachone.HigherlinkPort + "</td><td>" + eachone.DeviceModel + "</td>")
                })
            });
            return false;
        })
    })