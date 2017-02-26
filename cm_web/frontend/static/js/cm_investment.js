function handle_ajax_ret(json,func){
    if (json.error_code == 'OK'){
        return func(json.result,type_id)
    }
    else{
        alert(JSON.stringify(json.message)); 
    }
}
                        
            // 'im_id'     :str(self.id),
            // 'company_name'  :self.company_name,
            // 'cover_image'   :current_app.oss.original(self.cover_image),
            // 'company_url'   :self.company_url,
            // 'company_addr'  :self.company_addr,
            // 'pm_manager'    :self.pm_manager,
            // 'company_introduce' : self.company_introduce,


var item_li ='<li id="new-im" class="col-sm-6 col-md-3 col-xs-12" data-company_name="" data-cover_image="" data-company_url="" data-company_addr="" data-pm_manager="" data-company_introduce=""><div class="item-box"><div class="item-media"><img class="img-responsive" src=""/></div><div class="item-box-desc"><h4 id="company-name"></h4></div></div></li>';
function show_data(data,type_id){
    $("ul#ul-"+type_id).empty();
    for (var elem in data.im_list){
        $("ul#ul-"+type_id).append(item_li);
        $("ul#ul-"+type_id+" #new-im").attr('data-company_name',data.im_list[elem].company_name);
        $("ul#ul-"+type_id+" #new-im").attr('data-cover_image',data.im_list[elem].cover_image);
        $("ul#ul-"+type_id+" #new-im").attr('data-company_url',data.im_list[elem].company_url);
        $("ul#ul-"+type_id+" #new-im").attr('data-company_addr',data.im_list[elem].company_addr);
        $("ul#ul-"+type_id+" #new-im").attr('data-pm_manager',data.im_list[elem].pm_manager);
        $("ul#ul-"+type_id+" #new-im").attr('data-company_introduce',data.im_list[elem].company_introduce);
        $("ul#ul-"+type_id+" #new-im").find("#company-name").html(data.im_list[elem].company_name);
        $("ul#ul-"+type_id+" #new-im").find("img").attr("src",data.im_list[elem].cover_image);
        $("ul#ul-"+type_id+" #new-im").attr('id','im-'+data.im_list[elem].im_id);
    }


}

function get_list_by_type(start_index,count,func){
    $tab_li = $(event.target);
    type_id = $tab_li.attr('id').slice(6);
      $.ajax({ 
          type: "GET", 
          url: config.server_domain+'/get_im_list_by_type', 
          data:{'type_id':type_id,'start_index':start_index,'count':count},
          dataType: "json", 
          beforeSend: function(){ 
          }, 
          success: function(json){ 
              handle_ajax_ret(json,show_data);
          },
           error:function(){alert("错误：");}
      }); 

}

$(function(){
    $('body').on('click','.tab-li-class',function(){
        get_list_by_type(1,-1); 
    });
    $('body').on('click','li[id^="im-"]',function(){
        show_modal();
    });
});

function show_modal(){
    $li = $(event.target).parents('li[id^="im-"]');
    $('#company-media').find('img').attr('src',$li.attr('data-cover_image'));
    $('#modal-company-name').html($li.attr('data-company_name'));
    $('#modal-company-url').html($li.attr('data-company_url'));
    $('#modal-company-url').attr('href',$li.attr('data-company_url'));
    $('#modal-company-city').html($li.attr('data-company_addr'));
    $('#modal-pm-manager').html($li.attr('data-pm_manager'));
    $('#modal-company-description').html($li.attr('data-company_introduce'));
    $('#company-detail-modal').modal('show');
}
