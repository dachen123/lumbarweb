var config = {};

var match1s = window.location.hostname.match(/upupapp.cn/);
var match2s = window.location.hostname.match(/lumbar.cn/);
if (match1s){
    config.server_domain = '/cm';
}
else if(match2s){
    config.server_domain = '/cm';
}
else{
    config.server_domain = '';
}


