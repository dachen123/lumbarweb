
function test_ajax(data){
    alert("完成!");
}
function test_update_ajax(data){
    alert("完成!");
    $('#update-member-modal').modal('hide');
}
function add_member(){
    // var member_name = $('#member-name').val();
    // var light_avatar = $('#member-pic-light').val();
    // var dark_avatar = $('#member-pic-dark').val();
    // var member_description = $('#member-description').val();
    var post_form = {};
    post_form['name'] = $('#member-name').val();
    post_form['light_avatar'] = $('#member-pic-light').val();
    post_form['dark_avatar'] = $('#member-pic-dark').val();
    post_form['description'] = $('#member-description').val();

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/add_team_member",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_ajax);
           $('#tab-all-member-list').trigger('click');
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});
}

function set_original_data_show(){
    var $li = $(event.target).parents("li[id^='member-']");
    $('#update-member-id-input').val($li.attr('id').slice(7));
    $('#update-member-pic-light').val($li.find('#member-light-avatar').html());
    $('#update-member-pic-dark').val($li.find('#member-dark-avatar').html());
    $('#update-member-name').val($li.find('#member-name').html());
    $('#update-member-description').val($li.find('#member-description').html());

}

function update_member(){
    var post_form = {};
    post_form['tm_id'] = $('#update-member-id-input').val();
    post_form['name'] = $('#update-member-name').val();
    post_form['light_avatar'] = $('#update-member-pic-light').val();
    post_form['dark_avatar'] = $('#update-member-pic-dark').val();
    post_form['description'] =$('#update-member-description').val() ;

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/update_team_member",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_update_ajax);
           $('#tab-all-member-list').trigger('click');
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});

}

// var member_html = '<li id="new-member" style="padding-bottom:3px;"><span id="member-name" style="display:inline-block;width:500px"></span><img id="member-avatar" src="" style="height:50px;margin-right:10px;"/><span style="display:none" id="member-light-avatar"></span><span  style="display:none" id="member-dark-avatar"></span><span  style="display:none" id="member-description"></span><button class="update-member-btn">编辑</button><button class="set-index-show">设置首页展示</button><button class="delete-tm-btn">删除</button></li>';

var member_html = '<li id="new-member" style="padding-bottom:3px;"><img id="member-avatar" src="" style="height:100px;margin-right:10px;"/><span id="member-name" style="display:inline-block;width:500px"></span><span style="display:none" id="member-light-avatar"></span><span  style="display:none" id="member-dark-avatar"></span><span  style="display:none" id="member-description"></span><button class="update-member-btn">编辑</button><button class="delete-tm-btn">删除</button></li>';

function get_list_done(data){
    $("ol#member-list-ol").empty();
    for (var elem in data.tm_meta_list){
        $("ol#member-list-ol").append(member_html);
        $("ol#member-list-ol #new-member").find('#member-name').html(data.tm_meta_list[elem].name);
        $("ol#member-list-ol #new-member").find('#member-light-avatar').html(data.tm_meta_list[elem].light_avatar);
        $("ol#member-list-ol #new-member").find('#member-avatar').attr('src',data.tm_meta_list[elem].light_avatar);
        $("ol#member-list-ol #new-member").find('#member-dark-avatar').html(data.tm_meta_list[elem].dark_avatar);
        $("ol#member-list-ol #new-member").find('#member-description').html(data.tm_meta_list[elem].description);
        $("ol#member-list-ol #new-member").attr('id','member-'+data.tm_meta_list[elem].tm_id);
    }
    
}

function set_team_top(value){
    var $li = $(event.target).parents("li[id^='member-']");
    var post_form = {};
    post_form['tm_id'] = $li.attr('id').slice(7);
    post_form['top'] = value;
	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/set_team_top",
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

var top_member_html = '<li id="new-member"><span id="member-name" style="display:inline-block;width:500px"></span><button class="cancel-index-show">取消首页展示</button></li>';

function get_top_list_done(data){
    $("ol#top-member-list-ol").empty();
    for (var elem in data.tm_meta_list){
        $("ol#top-member-list-ol").append(top_member_html);
        $("ol#top-member-list-ol #new-member").find('#member-name').html(data.tm_meta_list[elem].name);
        $("ol#top-member-list-ol #new-member").attr('id','member-'+data.tm_meta_list[elem].tm_id);
    }
    
}



    window.onload = function () {
        localStorage.setItem('member_current_page',1);
        localStorage.setItem('member_count_per_page',5);
        $('#prev-page').on('click',function(){
            get_prev_page('/get_team_member_list',get_list_done,'member_current_page','member_count_per_page','ol#member-list-ol'); 
        });
        $('#next-page').on('click',function(){
            get_next_page('/get_team_member_list',get_list_done,'member_current_page','member_count_per_page','tm_meta_list','ol#member-list-ol'); 
        });
        init_upload_crop_pic_model('crop-light-avatar-modal','upload-light','member-pic-light','team',149,200);
        init_upload_crop_pic_model('crop-dark-avatar-modal','upload-dark','member-pic-dark','team',149,200);
        init_upload_crop_pic_model('update-light-avatar-modal','light-avatar-upload','update-member-pic-light','team',149,200);
        init_upload_crop_pic_model('update-dark-avatar-modal','dark-avatar-upload','member-pic-dark','team',149,200);
        $('#tab-all-member-list').on('click',function(){
            get_list('/get_team_member_list',1,5,get_list_done);
        });
        $('#member-post').on('click',function(){
            add_member();
        });
        // $('.update-member-btn').on('click',function(){
        //     $('#update-member-modal').modal('show');
        // });
        $('body').on('click','.update-member-btn',function(){
            $('#update-member-modal').modal('show');
            set_original_data_show();
        
        });
        $('#update-post').on('click',function(){
            // add_member();
            update_member();
        });
        $('body').on('click','.cancel-index-show',function(){
            set_team_top('false');
        
        });
        $('body').on('click','.set-index-show',function(){
            set_team_top('true');
        
        });
        $('body').on('click','.delete-tm-btn',function(){
            delete_member();
        
        });
        $('#tab-top-member-list').on('click',function(){
            get_list('/get_top_team',1,-1,get_top_list_done);
        });

    };


function delete_member(){
    var $li = $(event.target).parents("li[id^='member-']");
    var post_form = {};
    post_form['tm_id'] = $li.attr('id').slice(7);

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/delete_team_member",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_ajax);
           $('#tab-all-member-list').trigger('click');
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});

}
