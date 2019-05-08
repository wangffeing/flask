$(function () {
    $(".highlight-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        var highlight = parseInt(tr.attr("data-highlight"));
        var url = "";
        if(highlight){
            url = "/pcenter/uhpost/";
        }else{
            url = "/pcenter/hpost/";
        }
        zlajax.post({
            'url': url,
            'data': {
                'post_id': post_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertSuccessToast('操作成功！');
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else{
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });
});


$(function () {
    $('.delete-post-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var post_id = self.parent().parent().attr('data-id');
        zlalert.alertConfirm({
            'title': '删除帖子',
            'msg': '确认删除该帖子吗?',
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/pcenter/dposts/',
                    'data': {
                        'post_id': post_id
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            zlalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        })
    })
});