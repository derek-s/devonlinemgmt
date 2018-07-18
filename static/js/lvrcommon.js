/// <reference path="C:\\Users\\Derek.S\\AppData\\Roaming\\npm\\node_modules\\@types\\jquery\\index.d.ts"/>
$(document).ready(
    function(){
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token)
                }
            }
        })
        $.base64.utf8encode = true;
        $.base64.utf8decode = true;

        $(document).on("change", "select#lvradd_campus", function () {
            var $v = $(this)
            var $build = $v.parent().next().children()
            if ($v.val() == "") {
                $build.append('<option value="">请选择楼宇</option>')
            } else {
                $build.empty()
            }
            js_dvr_querybuild($v.val(), $build)
        })

        $(document).on("change", "select#lvradd_build", function () {
            var $v = $(this)
            var $campus = $v.parent().prev().children()
            var $lvr = $v.parent().next().children()
            if ($v.val() == "") {
                $lvr.append('<option value="">请选择弱电间</option>')
            } else {
                $lvr.empty()
            }
            js_dvr_querylvr($campus.val(), $v.val(), $lvr)
        })

        $(document).on("click", "a.devaddspan", function () {
            var tParent = $(this).parent()
            var cbl_tr = $(this).parents().find(".devselect")
            var clone = $(this).parents("tr.devadd_newtable").clone()
            var devadd_td = $(this).parent().prevAll()
            var td_id = $(".td_id:last")
            var new_td_id = parseInt(td_id.text()) + 1
            clone.find("td.td_id").text(new_td_id)
            var selectedValue_Campus = cbl_tr.find("select#lvradd_campus").val()
            clone.find("option[value = '" + selectedValue_Campus + "']").attr("selected", "selected")
            var selectedValue_build = cbl_tr.find("select#lvradd_campus").val()
            clone.find("option[value = '" + selectedValue_build + "']").attr("selected", "selected")
            $("table#lvradd_table > tbody").append(clone)
            
        });

        $(document).on("click", "a.devdelspan", function () {
            if ($("td.devadd_newtd").length == 1) {
                alert("新增行只有1行时不得删除")
            } else {
                $(this).parents("td.devadd_newtd").remove()
            }
        });

    }
)

function js_dvr_querylvr(campus_name, build_name, nextLvrElement) {
    var posturl = Flask.url_for("adminbg.devquerylvr")
    var campusb64 = encodeURIComponent($.base64.encode(campus_name), 'utf-8')
    var buildb64 = encodeURIComponent($.base64.encode(build_name), 'utf-8')
    $.ajaxSetup({ 
        async : false 
    });       
    $.post(posturl, {
        campus: campusb64,
        build: buildb64
    }, function(data){
        if (data.length != 0){
            nextLvrElement.append('<option value="lvr_null">请选择弱电间</option>')
            $.each(data, function(one){
                eachone = data[one]
                nextLvrElement.append('<option value="'+ eachone.LVRNo +'">'+ eachone.LVRNo +'</option>')
            })
        } else if (build_name == "build_null"){
            nextLvrElement.append('<option value="lvr_null">请选择弱电间</option>')
        } else {
            nextLvrElement.append('<option value="lvr_null">该楼暂无弱电间</option>')
        }
    }).fail(function (status) {
        console.log(status)
    })

}

function js_dvr_querybuild(campus_name, nextBuildElement) {
    var posturl = Flask.url_for('adminbg.devquerybuild')
    var campusb64 = encodeURIComponent($.base64.encode(campus_name), 'utf-8')
    $.ajaxSetup({ 
        async : false 
    });   
    $.post(posturl, {
        campus: campusb64
    }, function (data) {
        if (data.length != 0){
            nextBuildElement.append('<option value="build_null">请选择楼宇</option>')
            $.each(data, function (one) {
                eachone = data[one]
                nextBuildElement.append('<option value="'+ eachone.BuildName +'">'+ eachone.BuildName +'</option>')
            })
        } else if (campus_name == "campus_null"){
            nextBuildElement.append('<option value="build_null">请选择楼宇</option>')
        } else {
            nextBuildElement.append('<option value="build_null">该校区暂无楼宇信息</option>')
        }
    }).fail(function (status) {
        console.log(status)
    })
}

