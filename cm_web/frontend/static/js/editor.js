$(function(){ 
    var $uploadCrop; 
        var ori_url = ""; 
        function readFile(input) { 
             if (input.files && input.files[0]) { 
                var reader = new FileReader(); 
                 
                reader.onload = function (e) { 
                    ori_url = e.target.result;
                    $uploadCrop.croppie('bind', { 
                        url: e.target.result 
                    }); 
                } 
                 
                reader.readAsDataURL(input.files[0]); 
            } 
            else { 
                alert("Sorry - you're browser doesn't support the FileReader API"); 
            } 
        } 
 
        $uploadCrop = $('#upload-demo').croppie({ 
            viewport: { 
                width: 200, 
                height: 200, 
                type: 'square' 
            }, 
            boundary: { 
                width: 300, 
                height: 300 
            } 
        }); 
 
        $('#upload').on('change', function () {  
            $(".crop").show(); 
            readFile(this);  
            $('#upload-demo').croppie('bind',{
                url:ori_url 
            });
        }); 
        $('.upload-result').on('click', function (ev) { 
            $uploadCrop.croppie('result', 'canvas').then(function (resp) { 
                popupResult({ 
                    src: resp 
                }); 
            }); 
        }); 

        $('#get-pic-btn').on('click',function(){
            initpopup() 
        });
         
    function popupResult(result) { 
        var html; 
        if (result.html) { 
            html = result.html; 
        } 
        if (result.src) { 
            html = '<img src="' + result.src + '" />'; 
        } 
        $("#result").val(result.src); 
    } 

    function initpopup(){
        // $('#detail').popup({
        //     scrolllock: true,
        //     autoopen: true,
        //     color: '#e7e7e7',
        //     blur: false,
        //     opacity: 0.9
        // });
		$('#myModal').modal('show');
        
    
    }
}); 

