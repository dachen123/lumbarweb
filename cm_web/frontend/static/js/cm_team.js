$(function () {
	// var $everyBodySay = $('#everybody-say')
	// , oldContent = $everyBodySay.html();
    //
	// $('.img-warp').on('mouseenter', function () {
	// 	var $this = $(this)
	// 	, $p = $this.find('.name');
    //
	// 	$everyBodySay.find('h3').html( $p.data('say') );
	// 	$everyBodySay.find('p').html( $p.text() );
	// 	$p.addClass('show');
	// 	var $thisImg = $(this).find("img").first();
	// 	var bakImgUrl=  $thisImg.attr('src');
	// 	var targetImgUrl = $thisImg.attr('data');
	// 	if (targetImgUrl) {
	// 	  $thisImg.attr('src', targetImgUrl);
	// 	  $thisImg.attr('data', bakImgUrl);
	// 	}
	// }).on('mouseleave', function () {
	// 	$(this).find('.name').removeClass('show');
	// 	$everyBodySay.html( oldContent );
	// 	var $thisImg = $(this).find("img").first();
	// 	var bakImgUrl=  $thisImg.attr('src');
    // var targetImgUrl = $thisImg.attr('data');
    // if (targetImgUrl) {
    //   $thisImg.attr('src', targetImgUrl);
    //   $thisImg.attr('data', bakImgUrl);
    // }
	// });

	$('#cm-Carousel').carousel({
		//自动4秒播放
		interval : false,
	});

    $('body').on('click','div.img-warp',function(){
        show_modal();
    });

});

function show_modal(){
    $div = $(event.target).parents('div.img-warp');
    $('#person-pic').find('img').attr('src',$div.attr('data-img'));
    $('#person-introduce').find('p').html($div.attr('data-content'));
    $('#person-detail-modal').modal('show');
}
