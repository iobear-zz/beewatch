//Mouse related functions

 $(document).ready(function() {
	$('div.st').mouseenter(function() {
		var timeMac = $(this).attr('id').split('_', 2);
		$('.tstamp').html('time ' + timeConverter(timeMac[0]));
		$('.macAddr').html('mac ' + timeMac[1]);
		pullRedis(getRedisUrl(timeMac[0], timeMac[1]), 'min');
	});
	$('div.st').mousedown(function(event) {
		if (event.which == 1) { //left click
			var timeMac = $(this).attr('id').split('_', 2);
			var win = window.location = 'tail.php?unixTime=' + timeMac[0] + '&mac=' + timeMac[1] + '&logs=1';
			win.focus();
		}
	});
});

function showDetails() {
	var lasttime = 0;
	var uptime = 0;
	var lastErr;
	$.each(data, function(index, JSONvalue) {
		$.each(JSONvalue, function(name, val) {
			if (name == 'upt') {
				val = formatUptime(val);
			}
			if (name == 'uptSec') {
				val = secondsToTime(val);
			}
			if (name == 'url') {
				val = returnChannel(val);
			}
			$('.' + name).html(name + ': ' + val);
		});
	});
}
