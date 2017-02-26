
function test_ajax(data){
    alert("完成!");
}
function test_update_ajax(data){
    alert("完成!");
    $('#update-addr-modal').modal('hide');
}
function add_addr(){
    var post_form = {};
    post_form['city'] = $('#city').val();
    post_form['cover_image'] = $('#addr-cover-pic').val();
    post_form['detail_addr'] = $('#detail-addr').val();
    post_form['phone'] = $('#phone').val();
    post_form['mail'] = $('#email').val();
    post_form['fax_no'] = $('#fax').val();
    post_form['baidu_share'] = $('#addr-baidu-location').val();

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/add_addr",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_ajax);
           $('#tab-all-addr-list').trigger('click');
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});
}

function set_original_data_show(){
    var $li = $(event.target).parents("li[id^='addr-']");
    $('#update-addr-id').val($li.attr('id').slice(5));
    $('#update-city').val($li.find('#city-span').html());
    $('#update-addr-cover-pic').val($li.find('#addr-cover-pic-span').html());
    $('#update-detail-addr').val($li.find('#detail-addr-span').html());
    $('#update-phone').val($li.find('#phone-span').html());
    $('#update-email').val($li.find('#email-span').html());
    $('#update-fax').val($li.find('#fax-span').html());
    $('#update-addr-baidu-location').val($li.find('#baidu-location-span').html());

}

function update_addr(){
    var post_form = {};

    post_form['addr_id'] = $('#update-addr-id').val();
    post_form['city'] = $('#update-city').val();
    post_form['cover_image'] = $('#update-addr-cover-pic').val();
    post_form['detail_addr'] = $('#update-detail-addr').val();
    post_form['phone'] = $('#update-phone').val();
    post_form['mail'] = $('#update-email').val();
    post_form['fax_no'] = $('#update-fax').val();
    post_form['baidu_share'] = $('#update-addr-baidu-location').val();

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/update_addr",
		dataType:"json",
        data:post_form,
		success:function(json){
           handle_ajax_ret(json,test_update_ajax);
           $('#tab-all-addr-list').trigger('click');
		},
		error:function(){
            alert('网络错误，请重试!');
		}
	});

}


var addr_html = '<li id="new-addr" style="padding-bottom:5px;"><img id="addr-cover-pic" style="height:100px;"/><span id="detail-addr-span" style="display:inline-block;width:500px"></span><span style="display:none" id="city-span"></span><span  style="display:none" id="addr-cover-pic-span"></span><span  style="display:none" id="phone-span"></span><span  style="display:none" id="email-span"></span><span  style="display:none" id="fax-span"></span><span  style="display:none" id="baidu-location-span"></span><button class="update-addr-btn">编辑</button><button class="delete-addr-btn">删除</button></li>';


function get_list_done(data){
    $("ol#all-addr-list-ol").empty();
    for (var elem in data.addr_meta_list){
        $("ol#all-addr-list-ol").append(addr_html);
        $("ol#all-addr-list-ol #new-addr").find('#city-span').html(data.addr_meta_list[elem].city);
        $("ol#all-addr-list-ol #new-addr").find('#addr-cover-pic-span').html(data.addr_meta_list[elem].cover_image);
        $("ol#all-addr-list-ol #new-addr").find('#addr-cover-pic').attr('src',data.addr_meta_list[elem].cover_image);
        $("ol#all-addr-list-ol #new-addr").find('#detail-addr-span').html(data.addr_meta_list[elem].detail_addr);
        $("ol#all-addr-list-ol #new-addr").find('#phone-span').html(data.addr_meta_list[elem].phone);
        $("ol#all-addr-list-ol #new-addr").find('#email-span').html(data.addr_meta_list[elem].mail);
        $("ol#all-addr-list-ol #new-addr").find('#fax-span').html(data.addr_meta_list[elem].fax_no);
        $("ol#all-addr-list-ol #new-addr").find('#baidu-location-span').html(data.addr_meta_list[elem].baidu_share);
        $("ol#all-addr-list-ol #new-addr").attr('id','addr-'+data.addr_meta_list[elem].addr_id);
    }
    
}

function delete_addr(post_form){
    var $li = $(event.target).parents("li[id^='addr-']");
    var post_form = {};
    post_form['addr_id'] = $li.attr('id').slice(5);

	$.ajax({
		cache:false,
		type:'POST',
		url:config.server_domain + "/delete_addr",
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

    window.onload = function () {
        init_upload_crop_pic_model('crop-addr-cover-modal','addr-cover-file','addr-cover-pic','addr',200,179);
        init_upload_crop_pic_model('update-addr-cover-modal','update-addr-cover-file','update-addr-cover-pic','addr',200,179);

        $('#tab-all-addr-list').on('click',function(){
            get_list('/get_addr_list',1,20,get_list_done);
        });
        $('#addr-post').on('click',function(){
            add_addr();
        });

        $('body').on('click','.update-addr-btn',function(){
            $('#update-addr-modal').modal('show');
            set_original_data_show();
        
        });
        $('body').on('click','.delete-addr-btn',function(){
            delete_addr();
        
        });
        $('#update-addr').on('click',function(){
            update_addr();
        });


    };

