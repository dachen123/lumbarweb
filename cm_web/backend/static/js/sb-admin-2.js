/*!
 * Start Bootstrap - SB Admin 2 v3.3.7+1 (http://startbootstrap.com/template-overviews/sb-admin-2)
 * Copyright 2013-2016 Start Bootstrap
 * Licensed under MIT (https://github.com/BlackrockDigital/startbootstrap/blob/gh-pages/LICENSE)
 */
$(function() {
    $('#side-menu').metisMenu();
});

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
$(function() {
    $(window).bind("load resize", function() {
        var topOffset = 50;
        var width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $('div.navbar-collapse').addClass('collapse');
            topOffset = 100; // 2-row-menu
        } else {
            $('div.navbar-collapse').removeClass('collapse');
        }

        var height = ((this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height) - 1;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $("#page-wrapper").css("min-height", (height) + "px");
        }
    });

    var url = window.location;
    // var element = $('ul.nav a').filter(function() {
    //     return this.href == url;
    // }).addClass('active').parent().parent().addClass('in').parent();
    var element = $('ul.nav a').filter(function() {
        return this.href == url;
    }).addClass('active').parent();

    while (true) {
        if (element.is('li')) {
            element = element.parent().addClass('in').parent();
        } else {
            break;
        }
    }
});


function handle_ajax_ret(json,func){
    if (json.error_code == 'OK'){
        return func(json.result);
    }
    else{
        alert(JSON.stringify(json.message)); 
    }
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


    var urllib = OSS.urllib;
    var OSS = OSS.Wrapper;
function init_upload_crop_pic_model(modal_id,input_id,result_id,pic_type,width,height){ 
    var $uploadCrop; 
    var appServer = 'http://106.39.77.133:13389/get_oss_token';
    var bucket = 'chengmeitest';
    var region = 'oss-cn-beijing';
    var upload_key='';
    var STS = OSS.STS;
    var files = null;
    var crop_blob_file = null;
        // var ori_url = ""; 
        function readFile(input) { 
             if (input.files && input.files[0]) { 
                var reader = new FileReader(); 
                files = input.files;
                 
                reader.onload = function (e) { 
                    // ori_url = e.target.result;
                    $uploadCrop.croppie('bind', { 
                        url: e.target.result 
                    }); 
                } 
                 
                reader.readAsDataURL(input.files[0]); 
            } 
            else { 
                alert("获取不到图片，可能是您取消上传或是浏览器不支持裁剪"); 
		        $('#'+modal_id).modal('hide');
            } 
        } 
 
        $uploadCrop = $('#'+modal_id+' #upload-demo').croppie({ 
            viewport: { 
                width: width, 
                height: height, 
                type: 'square' 
            }, 
            boundary: { 
                width: 300, 
                height: 300 
            } 
        }); 
 
        $('#'+input_id).on('change', function () {  
            $("#"+modal_id+" .crop").show(); 
            readFile(this);  
            // $('#upload-demo').croppie('bind',{
            //     url:ori_url 
            // });
        }); 
        $('#'+modal_id+' #execute-crop').on('click', function (ev) { 
            $uploadCrop.croppie('result', 'blob').then(function (resp) { 
                crop_blob_file = resp;
                // popupResult({ 
                //     src: resp 
                // }); 

                // applyTokenDo(uploadFile);
                applyTokenDo(check_id_crop_and_upload);
            }); 
        }); 

        // $('#get-pic-btn').on('click',function(){
        //     initpopup() 
        // });
        $('#'+input_id).on('click',function(){
            initpopup() 
        });
         
    function popupResult(result) { 
        // var html; 
        // if (result.html) { 
        //     html = result.html; 
        // } 
        // if (result.src) { 
        //     html = '<img src="' + result.src + '" />'; 
        // } 
        // $("#"+result_id).val(result.src); 
    } 

    function initpopup(){
		$('#'+modal_id).modal('show');
        
    
    }

    var progress = function (p) {
      return function (done) {
        // var bar = document.getElementById('progress-bar');
        // bar.style.width = Math.floor(p * 100) + '%';
        // bar.innerHTML = ;
        $("#"+modal_id+' #crop-result').val('上传进度：'+Math.floor(p * 100) + '%'); 
        done();

      }
    };

    var uploadFile = function (client) {
      // var file = document.getElementById('crop-result').value;
      // var key = 'img/aaa.jpg';
      return client.multipartUpload(upload_key, new File([crop_blob_file],"crop.png"),{progress:progress}).then(function (res) {
        console.log('upload success: %j', res);
		$('#'+modal_id).modal('hide');
        if (res.url){
            $("#"+result_id).val(res.url); 
        }
        else{
            $("#"+result_id).val('http://'+bucket+'.'+region+'.aliyuncs.com/'+res.name); 
        }
        return res;
      });
    };

    var uploadOriFile = function (client) {
      // var file = document.getElementById('crop-result').value;
      // var key = 'img/aaa.jpg';
      return client.multipartUpload(upload_key, files[0],{progress:progress}).then(function (res) {
        console.log('upload success: %j', res);
		$('#'+modal_id).modal('hide');
        if (res.url){
            $("#"+result_id).val(res.url); 
        }
        else{
            $("#"+result_id).val('http://'+bucket+'.'+region+'.aliyuncs.com/'+res.name); 
        }
        return res;
      });
    };

    var check_id_crop_and_upload = function (client){
        $("#"+modal_id+' #crop-result').val('上传进度：0%'); 
        if($('#'+modal_id+' #is-crop').is(':checked')){
            uploadFile(client); 
        
        }
        else{
            uploadOriFile(client);
        }
    
    }

    var applyTokenDo = function (func) {
      var url = appServer;
      $.ajax({ 
          type: "GET", 
          url: appServer, 
          data:{'pic_type':pic_type},
          dataType: "json", 
          beforeSend: function(){ 
          }, 
          success: function(json){ 
              if (json.error_code == "OK"){
                     upload_key = json.result.upload_key;
                     var client = new OSS({
                       region: region,
                       accessKeyId: json.result.access_key_id,
                       accessKeySecret: json.result.access_key_secret,
                       stsToken: json.result.security_token,
                       bucket: bucket
                     });
                     return func(client);
              }
              else
                  alert(JSON.stringify(json.message));
          },
           error:function(){alert("错误：");}
      }); 
    
    };
} 


function get_list(url,start_index,count,func){
      $.ajax({ 
          type: "GET", 
          url: config.server_domain+url, 
          data:{'start_index':start_index,'count':count},
          dataType: "json", 
          beforeSend: function(){ 
          }, 
          success: function(json){ 
              handle_ajax_ret(json,func);
          },
           error:function(){alert("错误：");}
      }); 

}

function after_logout(data){
    window.location.href=config.server_domain+'/admin';
}

function logout(){
      $.ajax({ 
          type: "POST", 
          url: config.server_domain+"/logout", 
          dataType: "json", 
          beforeSend: function(){ 
          }, 
          success: function(json){ 
              handle_ajax_ret(json,after_logout);
          },
           error:function(){alert("错误：");}
      }); 

    
}

function current_page_start(current_page,count){
    var count_per_page = localStorage.getItem(count);
    var current_page_num = localStorage.getItem(current_page);
    if (!current_page_num){
        current_page_num = 1;
        localStorage.setItem(current_page,current_page_num);
    }
    return (current_page_num - 1)*count_per_page + 1;
}

function get_prev_page(url,func,current_page,count,ol_id){
    var current_page_num = parseInt(localStorage.getItem(current_page));
    if (current_page_num < 2 ){
        alert('已经在第一页了'); 
        return;
    }
    var count_per_page = parseInt(localStorage.getItem(count));
    $(ol_id).attr('start',prev_page_start(current_page_num,count_per_page));
    get_list(url,prev_page_start(current_page_num,count_per_page),count_per_page,func);
    set_prev_page_num(current_page_num,current_page);
}

function get_next_page(url,func,current_page,count,data_key,ol_id){
        var count_per_page = parseInt(localStorage.getItem(count));
      $.ajax({ 
          type: "GET", 
          url: config.server_domain+url, 
          data:{'start_index':next_page_start(current_page,count),'count':count_per_page},
          dataType: "json", 
          beforeSend: function(){ 
          }, 
          success: function(json){ 
              if (json.result[data_key].length > 0){
                    $(ol_id).attr('start',next_page_start(current_page,count));
                    handle_ajax_ret(json,func);
                    set_next_page_num(current_page); 
              }
              else{
                alert('没有更多的数据了'); 
              }
          },
           error:function(){alert("错误：");}
      }); 
}

function next_page_start(current_page,count){
    var count_per_page = localStorage.getItem(count);
    var current_page_num = localStorage.getItem(current_page);

    return parseInt(current_page_num) * parseInt(count_per_page) + 1;
}

function prev_page_start(current_page_num,count_per_page){
    return (current_page_num - 2) *count_per_page + 1;
}
//下一页返回后
function set_next_page_num(current_page){
    var current_page_num = localStorage.getItem(current_page);
    localStorage.setItem(current_page,parseInt(current_page_num)+1);
    return ;
}

//上一页返回后
function set_prev_page_num(current_page_num,current_page){
    localStorage.setItem(current_page,current_page_num-1);
    return 
}
