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
    }
)

function js_bcampus_modfiy(id, cmpname) {
    cmphtml = "<div class='ilayer_modfiy'><label class='ilayer_modfiy_label'>校区名称</label>" + "<input id='i_cmp_lay' value=" + cmpname +">" + "<button id='ilay_Cbutton' class='btn btn-primary'>保存修改</button></div>"
    layer.open({
        title: '编辑校区信息',
        type: 1,
        shade: 0,
        skin: 'layui-layer-rim', 
        area: ['420px', '240px'],
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
    url = self.location.href.split("&")[0]
    id_del= new Array()
    id_del.push(id)
    if (optype == "campus"){
        js_bcampus_delete(id_del, url)
    }else if (optype == "build"){
        js_bbuils_delete(id_del, url)
    }
}

function js_delArray(id) {
    id_array.push(id)
    return id_array
}

function js_bcampus_delete(ary, reloadurl) {
    if (confirm('确定删除么？')){
        $.ajax({
            url: $SCRIPT_ROOT + "admin/basicinfo/campus/delete",
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
                    window.location.href = reloadurl
                }
            }
        })
    }
}

function js_bbuils_delete(ary, reloadurl) {
    if (confirm('确定删除么？')){
        $.ajax({
            url: $SCRIPT_ROOT + "admin/basicinfo/build/delete",
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
                    window.location.href = reloadurl
                }
            }
        })
    }
}

function js_b_batchd() {
    url = self.location.href.split("&")[0]
    if ($("select#ipage").val() == "delete") {
        $("[name='oper']").each(function () {
            if ($(this).prop('checked')) {
                idary = js_delArray($(this).val())
            }
        })
        js_bbuils_delete(idary, url)
    }
}

function js_C_batchd() {
    url = self.location.href.split("&")[0]
    if ($("select#ipage").val() == "delete") {
        $("[name='oper']").each(function () {
            if ($(this).prop('checked')) {
                idary = js_delArray($(this).val())
            }
        })
        js_bcampus_delete(idary, url)
    }
}

function js_bbuild_modfiy(id, BuildName) {
    buildhtml = "<div class='ilayer_modfiy'><label class='ilayer_modfiy_label'>楼栋名称</label>" + "<input id='i_cmp_lay' value=" + BuildName +">" + "<button id='ilay_Cbutton' class='btn btn-primary'>保存修改</button></div>"
    layer.open({
        title: '编辑校区信息',
        type: 1,
        shade: 0,
        skin: 'layui-layer-rim', 
        area: ['420px', '240px'],
        content: buildhtml
      });
    $("button#ilay_Cbutton").on("click", function(){
        if(confirm('修改校区名称将同步修改其他数据表内引用字段，是否继续')){
            $.ajax({
                url: $SCRIPT_ROOT + "admin/basicinfo/build/modfiy",
                type: "post",
                data: {
                    id: id,
                    bname: $("input#i_cmp_lay").val()
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