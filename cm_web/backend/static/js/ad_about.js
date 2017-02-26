function test_ajax(data){
    alert("完成!");
}

function test_ajax_and_fresh(data){
    alert("完成!");
    window.location.reload();
}

function ajax_and_trigger_tab(data){
    alert("完成!");
    $('#tab-top-about-list').trigger('click');
}

function test_post_ajax(data){
    alert("完成!");
    $('#post-tab-modal').modal('hide');
}



var tab_html = '<li id="new-tab" style="padding-bottom:5px;"><img src="" style="height:200px;"/><span id="tab-title-span" style="display:none;"></span><span id="tab-slogan-span" style="display:none;"></span><button class="update-tab-btn" style="margin-left:100px;">编辑</button><button class="set-index-show">设置首页展示</button><button class="delete-tab-btn">删除</button></li>';


function get_list_done(data){
    $("ol#tab-list-ol").empty();
    for (var elem in data.tab_list){
        $("ol#tab-list-ol").append(tab_html);
        $("ol#tab-list-ol #new-tab").find('img').attr('src',data.tab_list[elem].bg_image);
        $("ol#tab-list-ol #new-tab").find('#tab-title-span').html(data.tab_list[elem].title);
        $("ol#tab-list-ol #new-tab").find('#tab-slogan-span').html(data.tab_list[elem].slogan);
        $("ol#tab-list-ol #new-tab").attr('id','tab-'+data.tab_list[elem].tab_id);
    }
    
}


function delete_tab(post_form){
    var $li = $(event.target).parents("li[id^='tab-']");
    var post_form = {};
    post_form['tab_id'] = $li.attr('id').slice(4);

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/delete_tab",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_ajax_and_fresh);
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});

}

function update_tab(){
    // var $li = $(event.target).parents("li[id^='image-']");
    var post_form = {};
    post_form['tab_id'] = $('#tab-id').val();
    post_form['title'] = $('#tab-title').val();
    post_form['bg_image'] = $('#image-url').val();
    post_form['slogan'] = $('#tab-slogan').val();

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/update_tab",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_post_ajax);
           window.location.reload();
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});

}

function add_tab(){
    // var $li = $(event.target).parents("li[id^='image-']");
    var post_form = {};
    post_form['title'] = $('#tab-title').val();
    post_form['bg_image'] = $('#image-url').val();
    post_form['slogan'] = $('#tab-slogan').val();

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/add_tab",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_post_ajax);
           window.location.reload();
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});

}

function toggle_add_tab(){
    $('#post-type').val('add');
    $('#post-tab-modal').modal('show');
}

function set_tab_top(value){
    var $li = $(event.target).parents("li[id^='tab-']");
    var post_form = {};
    post_form['tab_id'] = $li.attr('id').slice(4);
    post_form['top'] = value;
	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/set_tab_top",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_ajax);
           $('#tab-top-about-list').trigger('click');
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});

}

function toggle_update_tab(){
    var $li = $(event.target).parents("li[id^='tab-']");
    $('#post-type').val('update');
    $('#tab-id').val($li.attr('id').slice(4));
    $('#tab-title').val($li.find('#tab-title-span').html());
    $('#image-url').val($li.find('img').attr('src'));
    $('#tab-slogan').val($li.find('#tab-slogan-span').html());
    $('#post-tab-modal').modal('show');
}

function post_tab(){
    if ($('#post-type').val() == 'update'){
        update_tab();
         
    }
    else{
        add_tab(); 
    }
}

var top_tab_html = '<li id="new-tab"><img src="" style="height:200px;"/><span id="tab-title-span" style="display:none;"></span><span id="tab-slogan-span" style="display:none;"></span><button class="cancel-index-show" style="margin-left:100px;">取消首页展示</button></li>';

function get_top_list_done(data){
    $("ol#top-tab-list-ol").empty();
    for (var elem in data.tab_list){
        $("ol#top-tab-list-ol").append(top_tab_html);
        $("ol#top-tab-list-ol #new-tab").find('img').attr('src',data.tab_list[elem].bg_image);
        $("ol#top-tab-list-ol #new-tab").find('#tab-title-span').html(data.tab_list[elem].title);
        $("ol#top-tab-list-ol #new-tab").find('#tab-slogan-span').html(data.tab_list[elem].slogan);
        $("ol#top-tab-list-ol #new-tab").attr('id','tab-'+data.tab_list[elem].tab_id);
    }
    
    
}

window.onload = function (){
    $('#popup-post-layer').on('click',function(){
        toggle_add_tab(); 
    });
    $('#post-tab').on('click',function(){
        post_tab(); 
    });
    $('body').on('click','.update-tab-btn',function(){
        toggle_update_tab(); 
    });
    $('body').on('click','.delete-tab-btn',function(){
        delete_tab(); 
    });
    get_list('/get_tab_list',1,-1,get_list_done);
    init_upload_crop_pic_model('crop-bg-image-modal','bg-image-upload','image-url','about',200,77);

    $('body').on('click','.cancel-index-show',function(){
        set_tab_top('false');
    
    });
    $('body').on('click','.set-index-show',function(){
        set_tab_top('true');
    
    });
        $('#tab-top-about-list').on('click',function(){
            get_list('/get_top_tab',1,-1,get_top_list_done);
        });
        $('#tab-about-list').on('click',function(){
            get_list('/get_tab_list',1,-1,get_list_done);
        });
}
