$(function () {
    fullHeight();

	//轮播自动播放
	$('#cm-Carousel').carousel({
		//自动4秒播放
		interval : 4000,
	});
	$('#cm-Carousel').on('slide.bs.carousel', function () {
	    setTimeout(function(){
		    $('.slider-text').removeClass('animated swing');
		    $('.carousel-inner .active').find('.slider-text').addClass('animated swing');
		}, 500);


	});
    // $('#myCarousel').on('slid.bs.carousel', function () {
	//     setTimeout(function(){
	// 	    $('.slider-text').removeClass('animated fadeInUp');
	// 	    $('.carousel-inner .active').find('.slider-text').addClass('animated fadeInUp');
	// 	}, 500);
    //
    // });
    contentWayPoint();

    $('body').on('click','div[id^="news-"]',function(){
    //$('body').on('click','div.v-align',function(){
        event.stopPropagation(); 
        get_news_meta();
    });

    $('body').on('click','div[id^="im-"]',function(){
        event.stopPropagation(); 
        show_pm_modal();
    });


});

	var contentWayPoint = function() {
		var i = 0;
		$('.animate-box').waypoint( function( direction ) {

			if( direction === 'down' && !$(this.element).hasClass('animated') ) {
				
				i++;

				$(this.element).addClass('item-animate');
				setTimeout(function(){

					$('body .animate-box.item-animate').each(function(k){
						var el = $(this);
						setTimeout( function () {
							var effect = el.data('animate-effect');
							if ( effect === 'fadeIn') {
								el.addClass('fadeIn animated');
							} else if ( effect === 'fadeInLeft') {
								el.addClass('fadeInLeft animated');
							} else if ( effect === 'fadeInRight') {
								el.addClass('fadeInRight animated');
							} else {
								el.addClass('fadeInUp animated');
							}

							el.removeClass('item-animate');
						},  k * 200, 'easeInOutExpo' );
					});
					
				}, 100);
				
			}

		} , { offset: '85%' } );
	};

	var isMobile = {
		Android: function() {
			return navigator.userAgent.match(/Android/i);
		},
			BlackBerry: function() {
			return navigator.userAgent.match(/BlackBerry/i);
		},
			iOS: function() {
			return navigator.userAgent.match(/iPhone|iPad|iPod/i);
		},
			Opera: function() {
			return navigator.userAgent.match(/Opera Mini/i);
		},
			Windows: function() {
			return navigator.userAgent.match(/IEMobile/i);
		},
			any: function() {
			return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
		}
	};

	var fullHeight = function() {

		if ( !isMobile.any() ) {
			$('.js-fullheight').css('height', $(window).height());
			$(window).resize(function(){
				$('.js-fullheight').css('height', $(window).height());
			});
		}

	};


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

function show_pm_modal(){
    $li = $(event.target).parents('div[id^="im-"]');
    $('#company-media').find('img').attr('src',$li.attr('data-cover_image'));
    $('#modal-company-name').html($li.attr('data-company_name'));
    $('#modal-company-url').html($li.attr('data-company_url'));
    $('#modal-company-url').attr('href',$li.attr('data-company_url'));
    $('#modal-company-city').html($li.attr('data-company_addr'));
    $('#modal-pm-manager').html($li.attr('data-pm_manager'));
    $('#modal-company-description').html($li.attr('data-company_introduce'));
    $('#company-detail-modal').modal('show');
}


