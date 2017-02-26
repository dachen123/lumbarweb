function test_ajax(data){
    alert("完成!");
}

function test_update_ajax(data){
    alert("完成!");
}

function test_add_type_ajax(data){
    alert("完成!");
    $('#add-news-type-modal').modal('hide');
}


var news_html = '<li id="new-news"><img id="news-cover-pic" src="" style="height:100px;margin-right:10px;"/><span id="title" style="display:inline-block;width:400px"></span><span style="display:none" id="cover_image"></span><button class="update-news-btn">编辑</button><button class="set-index-show">设置首页展示</button><button class="delete-news-btn">删除</button></li>';


function get_list_done(data){
    $("ol#news-list-ol").empty();
    for (var elem in data.news_meta_list){
        $("ol#news-list-ol").append(news_html);
        $("ol#news-list-ol #new-news").find('#title').html(data.news_meta_list[elem].title);
        $("ol#news-list-ol #new-news").find('#cover_image').html(data.news_meta_list[elem].cover_image);
        $("ol#news-list-ol #new-news").find('#news-cover-pic').attr('src',data.news_meta_list[elem].cover_image);
        $("ol#news-list-ol #new-news").attr('id','news-'+data.news_meta_list[elem].news_id);
    }
    
}


var news_type_html = '<li id="new-news-type"><span id="type-name" style="display:inline-block;width:500px"></span><button class="delete-news-type-btn">删除</button></li>';

function add_news_type(){
    var post_form = {};
    post_form['type_name'] = $('#news-type-input').val();

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/add_news_type",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_add_type_ajax);
           $('#tab-news-type-list').trigger('click');
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});
    
}

function get_news_type_done(data){
    $("ol#news-type-list-ol").empty();
    for (var elem in data.type_meta_list){
        $("ol#news-type-list-ol").append(news_type_html);
        $("ol#news-type-list-ol #new-news-type").find('#type-name').html(data.type_meta_list[elem].type_name);
        $("ol#news-type-list-ol #new-news-type").attr('id','news-type-'+data.type_meta_list[elem].news_type_id);
    }

}

function delete_news_type(){
    var $li = $(event.target).parents("li[id^='news-type-']");
    var post_form = {};
    post_form['type_id'] = $li.attr('id').slice(10);

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/delete_news_type",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_ajax);
           $('#tab-news-type-list').trigger('click');
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});

}

function set_news_top(value){
    var $li = $(event.target).parents("li[id^='news-']");
    var post_form = {};
    post_form['news_id'] = $li.attr('id').slice(5);
    post_form['top'] = value;
	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/set_news_top",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_ajax);
           $('#tab-top-news-list').trigger('click');
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});

}

var top_news_html = '<li id="new-news"><img id="news-cover-pic" src="" style="height:100px;margin-right:10px;"/><span id="title" style="display:inline-block;width:400px"></span><button class="cancel-index-show">取消首页展示</button></li>';

function get_top_list_done(data){
    $("ol#top-news-list-ol").empty();
    for (var elem in data.news_meta_list){
        $("ol#top-news-list-ol").append(top_news_html);
        $("ol#top-news-list-ol #new-news").find('#title').html(data.news_meta_list[elem].title);
        $("ol#top-news-list-ol #new-news").find('#news-cover-pic').attr('src',data.news_meta_list[elem].cover_image);
        $("ol#top-news-list-ol #new-news").attr('id','news-'+data.news_meta_list[elem].news_id);
    }
    
}


    window.onload = function () {
        // init_upload_crop_pic_model('myModal','upload','pic_url','news');
        // $('#news-post').on('click',function(){
        //     add_news();
        // });
        localStorage.setItem('news_current_page',1);
        localStorage.setItem('news_count_per_page',5);
        $('#prev-page').on('click',function(){
            get_prev_page('/get_news_list',get_list_done,'news_current_page','news_count_per_page','ol#news-list-ol'); 
        });
        $('#next-page').on('click',function(){
            get_next_page('/get_news_list',get_list_done,'news_current_page','news_count_per_page','news_meta_list','ol#news-list-ol'); 
        });
        

        $('#tab-news-list').on('click',function(){
            get_list('/get_news_list',1,5,get_list_done);
        });
        get_list('/get_news_list',1,5,get_list_done);

        //类型编辑
        
        $('#tab-news-type-list').on('click',function(){
            get_list('/get_news_type_list',1,20,get_news_type_done);
        });
        $('#popup-add-layer').on('click',function(){
            $('#add-news-type-modal').modal('show');
        });
        $('#add-type').on('click',function(){
            add_news_type();
        });
        $('body').on('click','.delete-news-type-btn',function(){
            delete_news_type();
        
        });
        $('body').on('click','.update-news-btn',function(){
            update_news_redirect();
        
        });
        $('body').on('click','.cancel-index-show',function(){
            set_news_top('false');
        
        });
        $('body').on('click','.set-index-show',function(){
            set_news_top('true');
        
        });
        $('body').on('click','.delete-news-btn',function(){
            delete_news();
        
        });

        $('#tab-top-news-list').on('click',function(){
            get_list('/get_top_news',1,-1,get_top_list_done);
        });
    };

function update_news_redirect(){
    var $li = $(event.target).parents("li[id^='news-']");
    localStorage.setItem('news_id',$li.attr('id').slice(5));
    window.location.href = config.server_domain + '/update_news';
}

function delete_news(){
    var $li = $(event.target).parents("li[id^='news-']");
    var post_form = {};
    post_form['news_id'] = $li.attr('id').slice(5);

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/delete_news",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_ajax);
           window.location.reload();
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});

}
