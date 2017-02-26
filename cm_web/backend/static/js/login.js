	
function handle_ajax_ret(json,func){
    if (json.error_code == 'OK'){
        return func(json.result)
    }
    else{
        alert(JSON.stringify(json.message)); 
    }
}

function test_ajax(data){
    // alert("ok!");
    window.location.href=config.server_domain + "/ad_index";
}

function test_post_ajax(data){
    alert("ok!");
}

var config = {};

var match1s = window.location.hostname.match(/upupapp.cn/);
var match2s = window.location.hostname.match(/lumbar.cn/);
if (match1s){
    config.server_domain = '/cm';
}
else if(match2s){
    config.server_domain = '/cm';
}
else{
    config.server_domain = '';
}


function web_login(){
    if (!$('#login-account').val()){
        alert("请先输入帐号!");
        return;
    }
    // if (!$('#login-password').val()){
    //     alert("请先输入密码!");
    //     return;
    // }
    post_form = {}
    post_form['account'] = $('#login-account').val();
    post_form['password'] = hex_md5($('#login-password').val());

    $.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/login",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_ajax);
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});
}

$(function(){
    $('#web-login').on('click',function(){
        web_login(); 
    });
    $('input[name=account]').keydown(function(event){ 
        if(event.which==13){
            event.stopPropagation();    //  阻止事件冒泡
            web_login(); 
        } 
    });
    $('input[name=password]').keydown(function(event){ 
        if(event.which==13){
            event.stopPropagation();    //  阻止事件冒泡
            web_login(); 
        } 
    });

});
