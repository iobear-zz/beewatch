var urlMac = $.jqURL.qs().split('=')[0];

$(document).ready(function() {
	hideButtons();
});

function hideButtons() {
	if (urlMac != 'mac') {
		urlMac = '';
		$('button#extraLog').hide();
	}
}

function extraLog(host, mac) {
	var divisionChar = ':';
	var unformattedMAC = mac;
	var formattedMAC = unformattedMAC.replace('(.{2})', '$1' + divisionChar).substring(0, 17);

	console.log('host ' + host + ' mac ' + formattedMAC);
	if (host) {
		serverUrl = 'http://' + window.location.hostname + ':8080/api/v1/changeloglevel/' + host + '/' + mac + '/';
		$.ajax({
			url: serverUrl,
			type: 'POST',
			success: function(result) {
				console.log('ok');
		},
			error: function(jqXHR, textStatus, errorThrown) {
				console.log(textStatus);
				console.log(errorThrown);
			}
		});
	} else {
		alert('Missing ip!');
	}
}
