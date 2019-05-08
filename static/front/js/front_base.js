//
// $(function () {
//     $("#submit").click(function (event) {
//         //阻止按钮的提交表单的事件
//         event.preventDefault();
//         //获取标签
//         var keyword = $("input[name=keyword]");
//
//         //1.要在模板的meta标签中渲染一个csrf-token
//         //2.在ajax请求的头部汇总设置X-CSRFtoken
//         zlajax.post({
//             'url':'/index/',
//             'data':{
//                 'keyword':keyword,
//             },
//         });
//     });
// });

function search() {
    var keyword = $('#search').val();
    var dst = "/search/" + keyword;
    if (keyword != '') {
        window.location = dst;
    } else {
        return false;
    };
}

$(document).ready(function(){
    $('#search-btn').click(
        function(){
          search();
        }
    );
});