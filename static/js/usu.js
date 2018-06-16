$(document).ready(
    function () {
        $("#checkboxall").click(function () {
            if ($("#checkboxall").prop("checked")) {
                $("[name='oper']").prop("checked", true)
            } else {
                $("[name='oper']").prop("checked", false)
            }
        })
        $(document).on("click", '[name="oper"]', function(){
            var check=0
            if ($("#checkboxall").prop("checked")) {
                $("#checkboxall").prop("checked", false)
            }
            var inputcount = $("input[name='oper']").length
            $("input[name='oper']").each(function () {
                if($(this).prop("checked")){
                    check += 1
                }
                if(inputcount === check){
                    $("#checkboxall").prop("checked", true)
                }
            })
        })
        
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token)
                }
            }
        })
        $.base64.utf8encode = true;
        $.base64.utf8decode = true;
    }
)

function js_perm_modfiy(id){
    permhtml = '<div class="ilayer_modfiy"><label class="ilayer_modfiy_label">新权限</label>' +
    '<select id="iperm" name="action" id="bulk-action-selector-top">' +
    '<option value="suamdin">超级管理员</option>' +
    '<option value="admin">管理员</option>' +
    '<option value="ptman">普通用户</option>' +
    '</select><button id="ilay_Pbutton" class="btn btn-primary">保存修改</button></div>'
    layer.open({
        title: '编辑校区信息',
        type: 1,
        shade: 0,
        skin: 'layui-layer-rim', 
        area: ['420px', '240px'],
        content: permhtml
    });
    $('button#ilay_Pbutton').on('click', function() {
        $.ajax({
            url: $SCRIPT_ROOT + "admin/usrmanage/permodfiy",
            type: "POST",
            data: {
                id: id,
                newperm: $("select#iperm").val()
            },
            datetype: "json",
            success: function(resp) {
                resp = JSON.parse(resp)
                if (resp.status != 1) {
                    alert("修改失败 " + resp.message)
                }else{
                    alert("修改成功")
                    window.location.reload()
                }
            }
        })
    })  
}

function js_u_delete(id) {
    url = self.location.href.split("&")[0].split("?")[0]
    if (confirm('确定删除么？')){
        $.ajax({
            url: $SCRIPT_ROOT + "admin/usrmanage/usrdel",
            type: "post",
            data: {
                id: id
            },
            dateType: "json",
            success: function(resp) {
                resp = JSON.parse(resp)
                if (resp.status != 1) {
                    alert("删除失败")
                }else{
                    alert("删除成功")
                    window.location.href = url
                }
            }
        })
    }

}

function js_p_modfiy(id, name) {
    typehtml = "<div class='ilayer_modfiy'><label class='ilayer_modfiy_label'>修改密码</label><label class='ilayer_modfiy_label'>用户名"+ name +"</label>" + "<input id='i_cmp_lay'>" + "<button id='ilay_Cbutton' class='btn btn-primary'>保存修改</button></div>"
    layer.open({
        title: '编辑类型信息',
        type: 1,
        shade: 0,
        skin: 'layui-layer-rim',
        area: ['420px', '240px'],
        content: typehtml
    });
    $("button#ilay_Cbutton").on("click", function () {
        if (confirm('确定修改么？')) {
            $.ajax({
                url: $SCRIPT_ROOT + "admin/usrmanage/pwdmodfiy",
                type: "post",
                data: {
                    id: id,
                    pwd: $("input#i_cmp_lay").val()
                },
                dateType: "json",
                success: function (resp) {
                    resp = JSON.parse(resp)
                    if (resp.status != 1) {
                        alert("修改失败")
                    } else {
                        alert("修改成功")
                        window.location.reload()
                    }
                }
            })
        }
    })
}

function js_user_batchd() {
    if ($("select#ipage").val() == "delete") {
        console.log("1123")
    }
}