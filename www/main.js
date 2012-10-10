var daysago = 0;
var urls = {};
var macs = [];
macsToDisplay = [];

var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key2,value2) {
	if (key2 == "daysago") {
		daysago = value2;
	} else {
		daysago = 0;
	}
	var macsClean = 0;
	if (key2 == "macs") {
		macs = urldecode(value2);
		macsClean = macs.replace(/[^A-Fa-f0-9]/g, '').toUpperCase();
		macsToDisplay = macsClean.match(/.{1,12}/g);
	}
});

if (macsToDisplay) {
	for (var i = 0; i < macsToDisplay.length; i++) {
		macII = macsToDisplay[i];
		calcDisplay('days', 1, macII, daysago);
		pullRedis(getRedisUrl('', macII, 1, daysago), 'days');
	}
}

function urldecode(url) {
  return decodeURIComponent(url.replace(/\+/g, ' '));
}

function getRedisUrl(unixTime, macII, days, offset) {
	var url;
	if (days) {
		url = jsonUrl + "?json=1&days=" + days + "&mac=" + macII+"&offset="+offset;
	} else {
		url = jsonUrl + "?json=1&unixTime=" + unixTime + "&mac=" + macII;
	}
	return url;
}

var data;
function pullRedis(url, timeStr) {
	$.ajax({
		url: url,
		cache: "true",
		type: "GET",
		dataType: "json",
		success: function(source){
			data = source;
			if (timeStr == "days") {
				showInfo();
			} else if (timeStr == "min") {
				showDetails();
			} 
		},
		error: function(jqXHR, textStatus, errorThrown) {
			console.log(jqXHR);
			console.log(textStatus);
			console.log(errorThrown);
		}
	});							
}
