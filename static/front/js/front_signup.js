$(function () {
   $('#captcha-img').click(function (event) {
       var self= $(this);
       var src = self.attr('src');
       var newsrc = zlparam.setParam(src,'xx',Math.random());
       self.attr('src',newsrc);
   });
});

$(function () {
    $('#submit-btn').on('click', function () {
        var zxbh_input = $('input[name=zxbh]');
        var username_input = $('input[name=username]');
        var password_input = $('input[name=password1]');
        var password2_input = $('input[name=password2]');
        var graph_captcha_input = $('input[name=graph_captcha]');

        var zxbh = zxbh_input.val();
        var username = username_input.val();
        var password = password_input.val();
        var password2 = password2_input.val();
        var graph_captcha = graph_captcha_input.val();

        zlajax.post({
            'url': '/signup/',
            'data': {
                'zxbh': zxbh,
                'username': username,
                'password': password,
                'password2': password2,
                'graph_captcha': graph_captcha
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    var return_to = $('#return-to-span').text();
                    if (return_to) {
                        window.location = return_to
                    } else {
                        window.location = '/'
                    }
                } else {
                    zlalert.alertInfoToast(data['message']);
                }
            },
            'fail': function () {
                zlalert.alertNetworkError();
            }
        });
    });
});