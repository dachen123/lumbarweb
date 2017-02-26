
//     var urllib = OSS.urllib;
//     var OSS = OSS.Wrapper;
// function init_upload_crop_pic_model(modal_id,input_id,result_id,pic_type){ 
//     var $uploadCrop; 
//     var appServer = 'http://127.0.0.1:7777/get_oss_token';
//     var bucket = 'chengmeitest';
//     var region = 'oss-cn-beijing';
//     var upload_key='';
//     var STS = OSS.STS;
//     var crop_blob_file = null;
//         // var ori_url = ""; 
//         function readFile(input) { 
//              if (input.files && input.files[0]) { 
//                 var reader = new FileReader(); 
//                  
//                 reader.onload = function (e) { 
//                     // ori_url = e.target.result;
//                     $uploadCrop.croppie('bind', { 
//                         url: e.target.result 
//                     }); 
//                 } 
//                  
//                 reader.readAsDataURL(input.files[0]); 
//             } 
//             else { 
//                 alert("Sorry - you're browser doesn't support the FileReader API"); 
//             } 
//         } 
//  
//         $uploadCrop = $('#'+modal_id+' #upload-demo').croppie({ 
//             viewport: { 
//                 width: 200, 
//                 height: 200, 
//                 type: 'square' 
//             }, 
//             boundary: { 
//                 width: 300, 
//                 height: 300 
//             } 
//         }); 
//  
//         $('#'+input_id).on('change', function () {  
//             $("#"+modal_id+" .crop").show(); 
//             readFile(this);  
//             // $('#upload-demo').croppie('bind',{
//             //     url:ori_url 
//             // });
//         }); 
//         $('#'+modal_id+' #execute-crop').on('click', function (ev) { 
//             $uploadCrop.croppie('result', 'blob').then(function (resp) { 
//                 crop_blob_file = resp;
//                 // popupResult({ 
//                 //     src: resp 
//                 // }); 
//
//                 applyTokenDo(uploadFile);
//             }); 
//         }); 
//
//         $('#'+input_id).on('click',function(){
//             initpopup() 
//         });
//          
//     function popupResult(result) { 
//     } 
//
//     function initpopup(){
// 		$('#'+modal_id).modal('show');
//         
//     
//     }
//
//     var progress = function (p) {
//       return function (done) {
//         $("#"+result_id).val(Math.floor(p * 100) + '%'); 
//         done();
//       }
//     };
//
//     var uploadFile = function (client) {
//       return client.multipartUpload(upload_key, new File([crop_blob_file],"crop.png"),{progress:progress}).then(function (res) {
//         console.log('upload success: %j', res);
// 		$('#'+modal_id).modal('hide');
//         // $("#"+result_id).val(res.url); 
//
//         if (res.url){
//             $("#"+result_id).val(res.url); 
//         }
//         else{
//             $("#"+result_id).val('http://'+bucket+'.'+region+'.aliyuncs.com/'+res.name); 
//         }
//         return res;
//       });
//     };
//
//     var applyTokenDo = function (func) {
//       var url = appServer;
//       $.ajax({ 
//           type: "GET", 
//           url: appServer, 
//           data:{'pic_type':pic_type},
//           dataType: "json", 
//           beforeSend: function(){ 
//           }, 
//           success: function(json){ 
//               if (json.error_code == "OK"){
//                      upload_key = json.result.upload_key;
//                      var client = new OSS({
//                        region: region,
//                        accessKeyId: json.result.access_key_id,
//                        accessKeySecret: json.result.access_key_secret,
//                        stsToken: json.result.security_token,
//                        bucket: bucket
//                      });
//                      return func(client);
//               }
//               else
//                   alert(JSON.stringify(json.message));
//           },
//            error:function(){alert("错误：");}
//       }); 
//     
//     };
// } 

    window.onload = function () {
        init_upload_crop_pic_model('myModal','upload','pic_url','news',200,113);
        $('#news-post').on('click',function(){
            add_news();
        });

        // $('#tab-news-list').on('click',function(){
        //     get_list('get_news_list',1,20,get_list_done);
        // });
        get_list('/get_news_type_list',1,-1,get_type_list_done);
        
    };


function test_ajax(data){
    alert("ok!");
    window.location.href="/ad_news";
}

function test_update_ajax(data){
    alert("ok!");
}

var news_type={};
function get_type_list_done(data){
    for (var elem in data.type_meta_list){
        news_type[data.type_meta_list[elem].type_name] = data.type_meta_list[elem].news_type_id;
    }
}

function add_news(){
    var post_form = {};
    post_form['title'] = $('#news-title').val();
    post_form['cover_image'] = $('#pic_url').val();
    post_form['content'] = editor.$txt.html();
    post_form['type_id'] = news_type[$('#news-type').val()];

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/add_news",
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


