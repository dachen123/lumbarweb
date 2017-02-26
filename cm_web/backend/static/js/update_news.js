
    window.onload = function () {
        init_upload_crop_pic_model('myModal','upload','pic_url','news',200,113);
        $('#news-post').on('click',function(){
            update_news();
        });

        get_origin_data_show();
        get_list('/get_news_type_list',1,-1,get_type_list_done);
        
    };

function show_data(data){
    // post_form['news_id'] = localStorage.getItem('news_id');
    $('#news-title').val(data.news_meta.title);
    $('#pic_url').val(data.news_meta.cover_image);
    editor.$txt.html(data.news_meta.content);
    $('#news-type').val(data.news_meta.news_type);
    
}

function get_origin_data_show(){
    var post_form = {};
    post_form['news_id'] = localStorage.getItem('news_id');
	$.ajax({
		cache:false,
		type:'GET',
		url:config.server_domain + "/get_news_meta",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,show_data);
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});
    
}

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

function update_news(){
    var post_form = {};
    post_form['news_id'] = localStorage.getItem('news_id');
    post_form['title'] = $('#news-title').val();
    post_form['cover_image'] = $('#pic_url').val();
    post_form['content'] = editor.$txt.html();
    post_form['type_id'] = news_type[$('#news-type').val()];

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/update_news",
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


