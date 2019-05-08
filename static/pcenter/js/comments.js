$(function () {
    $('.delete-comment-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var comment_id = self.parent().parent().attr('data-id');
        zlalert.alertConfirm({
            'title': '删除评论',
            'msg': '确认删除该评论吗?',
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/pcenter/dcomments/',
                    'data': {
                        'comment_id': comment_id
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