	//Display 24hour status bar, for AirTies

var macIII = 0;
function genGreyBar(startsec, macII) {
	var f = startsec + 86100; //length of the bar = ~24h
	while (startsec <= f) {
		document.write('<div id=' + startsec + '_' + macII + ' title="no info" class="st"></div>');
		startsec = startsec + 300; //5min jump
	}
}

function calcDisplay(mode, uxdate, macII) {
	var monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Juni', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
	var now = new Date();
	var date = now.getDate();
	var month = now.getMonth();
	var year = now.getFullYear();
	var foo = new Date(year, month, date, 0, 0, 0, 0); //find beginning of day
	var unixtime_ms = foo.getTime(); // Returns milliseconds
	var unixtime = Math.floor(unixtime_ms * 0.001); //returns seconds since epoc
	if (daysago) {
		unixtime = unixtime - (86400 * daysago);
	}
	if (mode == 'days') {
		var daysec = uxdate * 86400; //amout of sec to process
		unixtime = unixtime + 86400; //adding an extra day, to wiew the present day
		var startsec = unixtime - daysec;

		while (startsec < unixtime) {
			genGreyBar(startsec, macII);
			var humanDate = new Date(startsec * 1000);
			document.write('<div class="date">' + humanDate.getDate() + ' ' + monthNames[humanDate.getMonth()] + ' ' + macII + '</div><br />');
			startsec = startsec + 86400;
		}
	}
}

var ip = '';
function showInfo() {
	var lasttime = 0;
	var uptime = 0;
	var lastErr = 0;
	var lastDerr = 0;
	var JSONvalue = 0;
	var stbErr = new Array();
	var displayErr = new Array();
	var errorList = new Array();
	var displayElist = new Array();
	errorList = ['badStream', 'ddecodeDrops', 'decodeErr', 'decodeOflow', 'iframeErr', 'ptsError', 'Discontinuity', 'stalled'];
	displayElist = ['displayDrops', 'displayErr', 'displayUflow'];

	$.each(data, function(index, JSONvalue) {
		var error5min = 0;
		var missingMcast = 0;
		var rtsperr = 0;
		var invaliddata = 0;
		var err = 0;
		var dErr = 0;
		invaliddata = data[index]['invaliddata'];
		missingMcast = data[index]['mcast'];
		rtsperr = data[index]['rtsperr'];
		for (key in JSONvalue) {
			if ($.inArray(key, errorList) !== -1) { //construct errors array
				if (JSONvalue[key]) {
					stbErr[key] = JSONvalue[key];
				}
			}
			if ($.inArray(key, displayElist) !== -1) { //construct diplay error array
				if (JSONvalue[key]) {
					displayErr[key] = JSONvalue[key];
				}
			}
		}

		for (var k in stbErr) { //sum errors
			if (stbErr[k]) {
				err = err + parseInt(stbErr[k]);
			}
		}

		for (var de in displayErr) { //sum errors
			if (displayErr[de]) {
				dErr = dErr + parseInt(displayErr[de]);
			}
		}

		if (data[index]['mac']) {
			macIII = data[index]['mac'];
		}

		var tstamp = parseInt(data[index]['stime']) + '_' + macIII;
		var mcast = data[index]['url'];
		var upt = parseInt(data[index]['uptSec']);

		if (!(upt)) {
			upt = parseInt(data[index]['upt']);
		}

		ip = data[index]['ip'];
		fw = data[index]['fw'];
		if (tstamp && document.getElementById(tstamp)) {
			if (rtsperr) {
				document.getElementById(tstamp).title = rtsperr;
				$('#' + tstamp).addClass('bwError');
			} else if (upt >= lasttime) {
				if (missingMcast) {
					document.getElementById(tstamp).title = 'no multicast';
					$('#' + tstamp).addClass('bwError');
				} else if (mcast) {
					document.getElementById(tstamp).title = mcast + '_ip:' + ip;
					if (err == lastErr) {
						showErr = 0;
					} else {
						showErr = err - lastErr;
					}

					if (dErr == lastDerr) {
						showDErr = 0;
					} else {
						showDErr = dErr - lastDerr;
					}

					if (showErr < 1 && showDErr < 1) {
						$('#' + tstamp).addClass('bwNoError');
						document.getElementById(tstamp).title = '';
					} else if (showErr < 8 && showErr > 0) {
						$('#' + tstamp).addClass('bwWarn');
					} else if (showErr > 7) {
						$('#' + tstamp).addClass('bwError');
					} else {
						$('#' + tstamp).addClass('bwDisplayError');
					}
					lastErr = err;
					lastDerr = dErr;
				} else {
					document.getElementById(tstamp).title = 'no video';
					$('#' + tstamp).addClass('bwNoInfo');
				}
			} else if (upt) {
					document.getElementById(tstamp).title = 'reboot';
					$('#' + tstamp).addClass('bwInfo');
			} else if (missingMcast) {
					document.getElementById(tstamp).title = 'no multicast';
					$('#' + tstamp).addClass('bwError');
			} else if (invaliddata) {
					document.getElementById(tstamp).title = 'invalid data';
					$('#' + tstamp).addClass('bwError');
			}
			if (upt && upt > 0) {
				lasttime = upt;
			}
		}
	});
}
