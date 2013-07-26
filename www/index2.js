var urlMac = $.jqURL.qs().split('=')[0];

$(document).ready(function() {
	hideButtons();
});

function hideButtons() {
	if (urlMac != 'mac') {
		urlMac = '';
		$('button#bookmarkBTN').hide();
		$('button#tailBTN').hide();
	}
}

function extraLog(host, mac) {
	var mac1 = mac.substring(0, 2);
	var mac2 = mac.substring(2, 4);
	var mac3 = mac.substring(4, 6);
	var mac4 = mac.substring(6, 8);
	var mac5 = mac.substring(8, 10);
	var mac6 = mac.substring(10, 12);

	var formattedMAC = mac1 + ':' + mac2 + ':' + mac3 + ':' + mac4 + ':' + mac5 + ':' + mac6;

	if (host) {
		serverUrl = 'http://' + window.location.hostname + ':8080/api/v1/changeloglevel/' + host + '/' + formattedMAC + '/';
		$.ajax({
			url: serverUrl,
			type: 'POST',
			success: function(result) {
				console.log('ok');
			}
		});
	} else {
		alert('Missing ip!');
	}
}
