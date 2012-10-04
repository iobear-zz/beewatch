function returnChannel(chan) {
	var ch = new Object();
	var retur = "";
	ch['233.138.48.168'] = 'DR1 HD';
	ch['233.138.48.190'] = 'TV2 OJ HD';
	ch['233.138.48.145'] = 'Silver HD';
	ch['233.138.48.202'] = 'Kanal 5';
	ch['233.138.48.132'] = 'Kanal 4';
	ch['233.138.48.163'] = 'DR HD';
	ch['88.83.68.50'] = 'Edgeware1 RTSP';
	ch['88.83.68.54'] = 'Edgeware2 RTSP';
	ch['233.138.48.187'] = 'TV2 News';
	ch['233.138.48.198'] = 'RTL HD';
	
	for (var k in ch) {
	    if (chan == k) {
			retur = ch[k];
	    }
	}
	
	if (!retur) {
		retur = chan;
		if (!chan) {
			retur = "no video";
		}
	}
	return retur;
}