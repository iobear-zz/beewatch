function ip2long(a,b,c,d){for(c=b=0;d=a.split('.')[b++];c+=d>>8|b>4?NaN:d*(1<<-8*b))d=parseInt(+d&&d);return c} //from https://gist.github.com/tsaniel

function timeConverter(UNIX_timestamp) {
	var a = new Date(UNIX_timestamp * 1000);
	var hour = a.getHours();
	var min = a.getMinutes();
	var time = hour + ':' + min;
	return time;
}

function formatUptime(a) {
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

function secondsToTime(secs) { // from http://codeaid.net/javascript/convert-seconds-to-hours-minutes-and-seconds-%28javascript%29
	var hours = Math.floor(secs / (60 * 60));
	var divisor_for_minutes = secs % (60 * 60);
	var minutes = Math.floor(divisor_for_minutes / 60);
	var divisor_for_seconds = divisor_for_minutes % 60;
	var seconds = Math.ceil(divisor_for_seconds);
	var days = Math.floor(hours / 24);

	if (days) {
		return days + ' days';
	} else {
		return hours + 'H' + minutes;
	}
}

function resolveIP(ipstart, ipend) {
	if (ipend) {
		var ipUrl = jsonUrl + '?ipstart=' + ipstart + '&ipend=' + ipend;
	} else {
		var ipUrl = jsonUrl + '?ipstart=' + ipstart;
	}
	$.ajax({ type: 'GET',
		url: ipUrl,
	    dataType: 'html',
		async: false,
		success: function(text) {
			retur = text;
		}
	});
	return retur;
}

function goToBars(task) {
	if (task == 'range') {
		var ipStart = $('#ipstart').val();
		var ipStart = ip2long(ipStart);
		var ipEnd = $('#ipend').val();
		var ipEnd = ip2long(ipEnd);
		macs = resolveIP(ipStart, ipEnd);
		if (macs) {
			var gotoUrl = '/index2.php?daysago=0&macs=' + macs;
			window.location.href = gotoUrl;
			return false;
		} else {
			$('.ipRangeHTML').html('<span class="label label-warning">IP: no active box found</span>');
		}
	} else {
		var ipadr = $('#ipadr').val();
		mac = resolveIP(ip2long(ipadr));
		if (mac) {
			window.location.href = 'index2.php?mac=' + mac + '&days=5';
		} else {
			$('.ipHTML').html('<span class="label label-warning">mac: not found</span>');
		}
	}
}
