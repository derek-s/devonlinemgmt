$(document).ready(
    function () {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token)
                }
            }
        })
        $.base64.utf8encode = true;
        $.base64.utf8decode = true;
        $("#checkboxall").click(function () {
            if ($("#checkboxall").prop("checked")) {
                $("[name='oper']").prop("checked", true)
            } else {
                $("[name='oper']").prop("checked", false)
            }
        })
        id_array = new Array()
        $("button#iopearbutton").click(function () {
            if ($("select#ipage").val() == "delete") {
                $("[name='oper']").each(function () {
                    if ($(this).prop('checked')) {
                        idary = js_delArray($(this).val())
                    }
                })
                js_bcampus_delete(idary)
            }
        })
    }
)

function js_bcampus_modfiy(id, cmpname) {
    cmphtml = "<div class='ilayer_modfiy'><label class='ilayer_modfiy_label'>校区名称</label>" + "<input id='i_cmp_lay' value=" + cmpname +">" + "<button id='ilay_Cbutton' class='btn btn-primary'>保存修改</button></div>"
    layer.open({
        title: '编辑校区信息',
        type: 1,
        shade: 0,
        skin: 'layui-layer-rim', //加上边框
        //area: ['420px', '240px'], //宽高
        content: cmphtml
      });
    $("button#ilay_Cbutton").on("click", function(){
        if(confirm('修改校区名称将同步修改其他数据表内引用字段，是否继续')){
            $.ajax({
                url: $SCRIPT_ROOT + "admin/basicinfo/campus/modfiy",
                type: "post",
                data: {
                    id: id,
                    cname: $("input#i_cmp_lay").val()
                },
                datetype: "json",
                success: function(resp) {
                    resp = JSON.parse(resp)
                    if (resp.status != 1) {
                        alert("添加失败 " + resp.message)
                    }else{
                        alert("添加成功")
                        window.location.reload()
                    }
                }
            })
        }
    })
}

function js_delArray_only(id, optype) {
    id_del= new Array()
    id_del.push(id)
    if (optype == "campus"){
        js_bcampus_delete(id_del)
    }
}

function js_delArray(id) {
    id_array.push(id)
    return id_array
}

function js_bcampus_delete(ary) {
    if (confirm('确定删除么？')){
        $.ajax({
            url: $SCRIPT_ROOT + "admin/basicinfo/campus/detele",
            type: "post",
            traditional:true,  
            data: {
                array_id: JSON.stringify(ary)
            },
            dateType: "json",
            success: function(resp) {
                resp = JSON.parse(resp)
                if (resp.status != 1) {
                    alert("删除失败")
                }else{
                    alert("删除成功")
                    location.reload()
                }
            }
        })
    }
}
