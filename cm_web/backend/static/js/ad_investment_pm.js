
function test_ajax(data){
    alert("完成!");
}
function test_update_ajax(data){
    alert("完成!");
    $('#update-investment-modal').modal('hide');
}

function test_add_type_ajax(data){
    alert("完成!");
    $('#add-investment-type-modal').modal('hide');
}
function add_investment(){
    var post_form = {};
    post_form['company_name'] = $('#company-name').val();
    post_form['cover_image'] = $('#company-cover-pic').val();
    post_form['company_url'] = $('#company-link-url').val();
    post_form['company_addr'] = $('#company-addr').val();
    post_form['pm_manager'] = $('#man-in-charge').val();
    post_form['company_introduce'] = $('#company-description').val();
    post_form['type_id'] = investment_type[$('#company-type').val()];

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/add_investment",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_ajax);
           $('#tab-all-investment-list').trigger('click');
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});
}

function set_original_data_show(){
    var $li = $(event.target).parents("li[id^='investment-']");
    $('#update-company-id').val($li.attr('id').slice(11));
    $('#update-company-name').val($li.find('#company-name-span').html());
    $('#update-company-cover-pic').val($li.find('#company-cover-pic-span').html());
    $('#update-company-link-url').val($li.find('#company-link-url-span').html());
    $('#update-company-addr').val($li.find('#company-addr-span').html());
    $('#update-man-in-charge').val($li.find('#man-in-charge-span').html());
    $('#update-company-description').val($li.find('#company-description-span').html());
    $('#update-company-type').val($li.find('#company-type-span').html());

}

function update_investment(){
    var post_form = {};
    post_form['im_id'] = $('#update-company-id').val();
    post_form['company_name'] = $('#update-company-name').val();
    post_form['cover_image'] = $('#update-company-cover-pic').val();
    post_form['company_url'] = $('#update-company-link-url').val();
    post_form['company_addr'] = $('#update-company-addr').val();
    post_form['pm_manager'] = $('#update-man-in-charge').val();
    post_form['company_introduce'] = $('#update-company-description').val();
    post_form['type_id'] = investment_type[$('#update-company-type').val()];

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/update_investment",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_update_ajax);
           $('#tab-all-investment-list').trigger('click');
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});

}


var investment_html = '<li id="new-investment" style="padding-bottom:5px;"><img id="cover-pic" src="" style="height:100px;margin-right:10px;" /><span id="company-name-span" style="display:inline-block;width:500px"></span><span style="display:none" id="company-cover-pic-span"></span><span  style="display:none" id="company-link-url-span"></span><span  style="display:none" id="company-addr-span"></span><span  style="display:none" id="man-in-charge-span"></span><span  style="display:none" id="company-description-span"></span><span  style="display:none" id="company-type-span"></span><button class="update-investment-btn">编辑</button><button class="set-index-show">设置首页展示</button><button class="delete-im-btn">删除</button></li>';

function get_list_done(data){
    $("ol#all-investment-list-ol").empty();
    for (var elem in data.im_info_list){
        $("ol#all-investment-list-ol").append(investment_html);
        $("ol#all-investment-list-ol #new-investment").find('#company-name-span').html(data.im_info_list[elem].company_name);
        $("ol#all-investment-list-ol #new-investment").find('#company-cover-pic-span').html(data.im_info_list[elem].cover_image);
        $("ol#all-investment-list-ol #new-investment").find('img#cover-pic').attr('src',data.im_info_list[elem].cover_image);
        $("ol#all-investment-list-ol #new-investment").find('#company-link-url-span').html(data.im_info_list[elem].company_url);
        $("ol#all-investment-list-ol #new-investment").find('#company-addr-span').html(data.im_info_list[elem].company_addr);
        $("ol#all-investment-list-ol #new-investment").find('#man-in-charge-span').html(data.im_info_list[elem].pm_manager);
        $("ol#all-investment-list-ol #new-investment").find('#company-description-span').html(data.im_info_list[elem].company_introduce);
        $("ol#all-investment-list-ol #new-investment").find('#company-type-span').html(data.im_info_list[elem].company_type);
        $("ol#all-investment-list-ol #new-investment").attr('id','investment-'+data.im_info_list[elem].im_id);
    }
    
}

var investment_type_html = '<li id="new-investment-type"><span id="type-name" style="display:inline-block;width:500px"></span><button class="delete-investment-type-btn">删除</button></li>';

function add_investment_type(){
    var post_form = {};
    post_form['type_name'] = $('#investment-type-input').val();

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/add_investment_type",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_add_type_ajax);
           // $('#tab-investment-type-list').trigger('click');
           window.location.reload();
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});
    
}

var investment_type = {};

function get_investment_type_done(data){
    investment_type = {};
    $("ol#investment-type-list-ol").empty();
    for (var elem in data.type_meta_list){
        $("ol#investment-type-list-ol").append(investment_type_html);
        $("ol#investment-type-list-ol #new-investment-type").find('#type-name').html(data.type_meta_list[elem].type_name);
        $("ol#investment-type-list-ol #new-investment-type").attr('id','im-type-'+data.type_meta_list[elem].im_type_id);
        investment_type[data.type_meta_list[elem].type_name] = data.type_meta_list[elem].im_type_id;
    }

}

function delete_investment_type(){
    var $li = $(event.target).parents("li[id^='im-type-']");
    var post_form = {};
    post_form['type_id'] = $li.attr('id').slice(8);

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/delete_investment_type",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_ajax);
           // $('#tab-investment-type-list').trigger('click');
           window.location.reload();
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});

}

function set_im_top(value){
    var $li = $(event.target).parents("li[id^='investment-']");
    var post_form = {};
    post_form['im_id'] = $li.attr('id').slice(11);
    post_form['top'] = value;
	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/set_im_top",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_ajax);
           $('#tab-top-investment-list').trigger('click');
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});

}

var top_im_html = '<li id="new-investment" style="padding-bottom:5px;"><img id="investment-cover-pic" src="" style="height:100px;margin-right:10px;" /><span id="company-name-span" style="display:inline-block;width:400px"></span><button class="cancel-index-show">取消首页展示</button></li>';

function get_top_list_done(data){
    $("ol#top-investment-list-ol").empty();
    for (var elem in data.im_info_list){
        $("ol#top-investment-list-ol").append(top_im_html);
        $("ol#top-investment-list-ol #new-investment").find('#company-name-span').html(data.im_info_list[elem].company_name);
        $("ol#top-investment-list-ol #new-investment").find('#investment-cover-pic').attr('src',data.im_info_list[elem].cover_image);
        $("ol#top-investment-list-ol #new-investment").attr('id','investment-'+data.im_info_list[elem].im_id);
    }
    
}




    window.onload = function () {

        localStorage.setItem('im_current_page',1);
        localStorage.setItem('im_count_per_page',5);
        $('#prev-page').on('click',function(){
            get_prev_page('/get_investment_list',get_list_done,'im_current_page','im_count_per_page','ol#all-investment-list-ol'); 
        });
        $('#next-page').on('click',function(){
            get_next_page('/get_investment_list',get_list_done,'im_current_page','im_count_per_page','im_info_list','ol#all-investment-list-ol'); 
        });
        init_upload_crop_pic_model('crop-company-cover-modal','company-cover-pic-file','company-cover-pic','investment',200,150);
        init_upload_crop_pic_model('update-company-cover-modal','update-company-cover-pic-file','update-company-cover-pic','investment',200,150);
        $('#tab-all-investment-list').on('click',function(){
            get_list('/get_investment_list',1,5,get_list_done);
        });
        $('#tab-investment-type-list').on('click',function(){
            get_list('/get_im_type_list',1,-1,get_investment_type_done);
        });
        get_list('/get_im_type_list',1,-1,get_investment_type_done);
        $('#popup-add-layer').on('click',function(){
            $('#add-investment-type-modal').modal('show');
        });
        $('#add-type').on('click',function(){
            add_investment_type();
        });
        $('body').on('click','.delete-investment-type-btn',function(){
            delete_investment_type();
        
        });
        $('#company-post').on('click',function(){
            add_investment();
        });

        $('body').on('click','.update-investment-btn',function(){
            $('#update-investment-modal').modal('show');
            set_original_data_show();
        
        });
        $('#update-company').on('click',function(){
            update_investment();
        });
        $('body').on('click','.cancel-index-show',function(){
            set_im_top('false');
        
        });
        $('body').on('click','.set-index-show',function(){
            set_im_top('true');
        
        });
        $('body').on('click','.delete-im-btn',function(){
            delete_im();
        
        });
        $('#tab-top-investment-list').on('click',function(){
            get_list('/get_top_im',1,-1,get_top_list_done);
        });


    };

function delete_im(){
    var $li = $(event.target).parents("li[id^='investment-']");
    var post_form = {};
    post_form['im_id'] = $li.attr('id').slice(11);

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/delete_investment",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_ajax);
           $('#tab-all-investment-list').trigger('click');
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});

}

