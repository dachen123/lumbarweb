function handle_ajax_ret(json,func){
    if (json.error_code == 'OK'){
        return func(json.result,type_id)
    }
    else{
        alert(JSON.stringify(json.message)); 
    }
}
function handle_ajax_ret2(json,func){
    if (json.error_code == 'OK'){
        return func(json.result)
    }
    else{
        alert(JSON.stringify(json.message)); 
    }
}
                // 'news_id'   :str(self.id),
                // 'title'     :self.title,
                // 'cover_image'   :current_app.oss.original(self.cover_image),
                // 'content'       :self.content,
                // 'news_type'     :news_type.type_name if news_type \


var div_html = '<div id="new-news" class="col-md-6 col-sm-6 col-xs-12 list-item"><div class="img-wrap"><img src="" alt=""><div class="img-cover"></div></div><div id="news-time" class="list-item-date"></div><h3 id="news-title" class="list-item-title"></h3></div>';

function show_data(data,type_id){
    $("div#row-"+type_id).empty();
    for (var elem in data.news_list){
        $("div#row-"+type_id).append(div_html);
        $("div#row-"+type_id+" #new-news").find('img').attr('src',data.news_list[elem].cover_image);
        $("div#row-"+type_id+" #new-news").find('#news-time').html(data.news_list[elem].create_time);
        $("div#row-"+type_id+" #new-news").find('#news-title').html(data.news_list[elem].title);
        $("div#row-"+type_id+" #new-news").attr('id','news-'+data.news_list[elem].news_id);

    }
}

function get_list_by_type(start_index,count){
    $tab_li = $(event.target);
    type_id = $tab_li.attr('id').slice(6);
      $.ajax({ 
          type: "GET", 
          url: config.server_domain+'/get_news_list_by_type', 
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

function show_news_data(data){
    $('#modal-news-image').attr('src',data.news_meta.cover_image);
    $('#modal-news-title').html(data.news_meta.title);
    $('#modal-news-time').html(data.news_meta.create_time);
    $('#modal-news-content').html(data.news_meta.content);
    $('#modal-news-detail').modal('show');

}

function get_news_meta(){
    $div = $(event.target).parents('div[id^="news-"]');
    news_id = $div.attr('id').slice(5);
      $.ajax({ 
          type: "GET", 
          url: config.server_domain+'/get_news_meta', 
          data:{'news_id':news_id},
          dataType: "json", 
          beforeSend: function(){ 
          }, 
          success: function(json){ 
              handle_ajax_ret2(json,show_news_data);
          },
           error:function(){alert("错误：");}
      }); 

}

$(function(){
    $('body').on('click','.tab-li-class',function(){
        get_list_by_type(1,-1); 
    });

    $('body').on('click','div[id^="news-"]',function(){
        event.stopPropagation(); 
        get_news_meta();
    });

});


