function jsload_addevent(username) {
    layer.open({
        title: '添加个人待办事项',
        type: 2,
        area: ['435px', '475px'],
        fixed: false, //不固定
        maxmin: false,
        content: $SCRIPT_ROOT + '/profile/' + username + '/add'
    });
}

function jsload_event(id) {
    layer.open({
        title: '添加个人待办事项',
        type: 2,
        area: ['435px', '475px'],
        fixed: false, //不固定
        maxmin: false,
        content: $SCRIPT_ROOT + '/event/' + id
    });
}

function js_delete(id) {
    $.ajax({
        url: $PATH_ROOT + "/delete",
        type: "POST",
        dateType: "json",
        success: function(resp) {
            resp = JSON.parse(resp)
            if (resp.status != 1) {
                alert("删除失败")
            }
            alert("删除成功")
            var eventbox = parent.layer.getFrameIndex(window.name);
            parent.location.reload();
        }
    })
}