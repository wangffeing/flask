$(function () {
    $(".manage-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var user_id = tr.attr("data-id");
        var usermanage = parseInt(tr.attr("user_manage"));
        var url = "";
        if(usermanage){
            url = "/pcenter/muser/";
        }else{
            url = "/pcenter/umuser/";
        }
        zlajax.post({
            'url': url,
            'data': {
                'user_id': user_id
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