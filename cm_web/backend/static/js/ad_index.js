function test_ajax(data){
    alert("完成!");
}

function test_post_ajax(data){
    alert("完成!");
    $('#post-image-modal').modal('hide');
}



var image_html = '<li id="new-image"><img src="" style="height:200px;padding-bottom:5px;"/><span id="image-title-span" style="display:none"></span><span id="image-content-span" style="display:none"></span><button class="update-image-btn" style="margin-left:300px;">编辑</button><button class="delete-image-btn">删除</button></li>';


function get_list_done(data){
    $("ol#image-list-ol").empty();
    for (var elem in data.image_list){
        $("ol#image-list-ol").append(image_html);
        $("ol#image-list-ol #new-image").find('img').attr('src',data.image_list[elem].image);
        $("ol#image-list-ol #new-image").find('#image-title-span').html(data.image_list[elem].title);
        $("ol#image-list-ol #new-image").find('#image-content-span').html(data.image_list[elem].content);
        $("ol#image-list-ol #new-image").attr('id','image-'+data.image_list[elem].image_id);
    }
    
}


function delete_image(post_form){
    var $li = $(event.target).parents("li[id^='image-']");
    var post_form = {};
    post_form['image_id'] = $li.attr('id').slice(6);

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/delete_image",
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

function update_image(){
    // var $li = $(event.target).parents("li[id^='image-']");
    var post_form = {};
    post_form['image_id'] = $('#image-id').val();
    post_form['image'] = $('#image-url').val();
    post_form['title'] = $('#image-title').val();
    post_form['content'] = $('#image-content').val();

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/update_image",
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

function add_image(){
    // var $li = $(event.target).parents("li[id^='image-']");
    var post_form = {};
    post_form['image'] = $('#image-url').val();
    post_form['title'] = $('#image-title').val();
    post_form['content'] = $('#image-content').val();

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/add_image",
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

function toggle_add_image(){
    $('#post-type').val('add');
    $('#post-image-modal').modal('show');
}

function toggle_update_image(){
    var $li = $(event.target).parents("li[id^='image-']");
    $('#post-type').val('update');
    $('#image-id').val($li.attr('id').slice(6));
    $('#image-url').val($li.find('img').attr('src'));
    $('#image-title').val($li.find('#image-title-span').html());

    $('#image-content').val($li.find('#image-content-span').html());
    $('#post-image-modal').modal('show');
}

function post_image(){
    if ($('#post-type').val() == 'update'){
        update_image();
         
    }
    else{
        add_image(); 
    }
}

window.onload = function (){
    $('#popup-post-layer').on('click',function(){
        toggle_add_image(); 
    });
    $('#post-image').on('click',function(){
        post_image(); 
    });
    $('body').on('click','.update-image-btn',function(){
        toggle_update_image(); 
    });
    $('body').on('click','.delete-image-btn',function(){
        delete_image(); 
    });
    get_list('/get_image_list',1,-1,get_list_done);
    init_upload_crop_pic_model('crop-carousel-modal','carousel-upload','image-url','index',200,92);
}
