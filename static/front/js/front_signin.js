$(function(){
    $('#submit-btn').on('click',function(event){
        event.preventDefault();
        var zxbh_input=$('input[name=zxbh]');
        var password_input=$('input[name=password]');
        var remember_input=$('input[name=remember]');
        var zxbh=zxbh_input.val();
        var password=password_input.val();
        var remember=remember_input.checked?1:0;

        zlajax.post({
           'url':'/signin/',
           'data':{
               'zxbh':zxbh,
               'password':password,
               'remember':remember
           },
            'success':function(data){
               if(data['code']==200){
                   var return_to=$('#return-to-span').text();
                   if(return_to){
                       window.location=return_to;
                   }else{
                       window.location='/'
                   }
               }else{
                   zlalert.alertInfo(data['message']);
               }
            }
        });

    });
});