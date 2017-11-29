$(document).ready(
    function() {
        $.getJSON($SCRIPT_ROOT + 'list', {}, function(data) {
            $.each(data, function(one) {
                $("table#devinfolist>tbody").append("<tr></tr>")
                eachone = data[one]
                $("table#devinfolist>tbody tr:last-child").append("<td>" + eachone.id + "</td><td>" + eachone.Location + "</td><td>" + eachone.HostName + "</td><td>" + eachone.LAA + "</td><td>" + eachone.HigherlinkIP + "</td><td>" + eachone.HigherlinkPort + "</td><td>" + eachone.DeviceModel + "</td>")
            })
        })
    })