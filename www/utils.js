function ip2long(a,b,c,d){for(c=b=0;d=a.split('.')[b++];c+=d>>8|b>4?NaN:d*(1<<-8*b))d=parseInt(+d&&d);return c} //from https://gist.github.com/tsaniel

function timeConverter(UNIX_timestamp){
	var a = new Date(UNIX_timestamp*1000);
	var hour = a.getHours();
	var min = a.getMinutes();
	var time = hour+':'+min;
	return time;
}

function formatUptime(a){
	if (a.length > 4) {
		a = a.slice(0, -4);
		if (a == 1) {
			return a + ' day';
		} else {
			return a + ' days';
		}
	} else {
		return a;
	}
}

function resolveIP(ip) {
	var orderUrl = jsonUrl + "?ip="+ip;
	$.ajax({ type: "POST",   
		url: orderUrl,
	    dataType: "html",
		async: false,
		success : function(text) {
			retur = text;
		}
	});
	return retur;
}