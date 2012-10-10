//Mouse related functions

document.write( '<br /><br /><div class="kasse">');
document.write( '<div id="macAddr" class="headline">MAC </div>' );
document.write( '<div id="url"></div>' );
document.write( '<div id="tstamp"></div>' );
document.write( '<div id="upt"></div>' );
document.write( '</div><div class="kasse">');
document.write( '<div class="headline">Decoder</div>' );

document.write( '<div id="ddecodeDrops"></div>' );
document.write( '<div id="decodeErr"></div>' );
document.write( '<div id="decodeOflow"></div>' );
document.write( '</div><div class="kasse">');
document.write( '<div class="headline">Display</div>' );
document.write( '<div id="displayDrops"></div>' );
document.write( '<div id="displayErr"></div>' );
document.write( '<div id="displayOflow"></div>' );
document.write( '</div><div class="kasse">');
document.write( '<div class="headline">PTS</div>' );
document.write( '<div id="ptsDrops"></div>' );
document.write( '<div id="ptsOflow"></div>' );

document.write( '</div><div class="kassesidst">');
document.write( '<div class="headline">Misc</div>' );
document.write( '<div id="iframeErr"></div>' );
document.write( '<div id="stalled"></div>' );
document.write( '<div id="badStream"></div>' );
document.write( '<div id="operaCrash"></div>' );
document.write( '</div>');

 $(document).ready(function(){
	$("div.st").mouseenter(function(){
		var timeMac = $(this).attr('id').split("_",2);
		document.getElementById("tstamp").innerHTML = "time "+timeConverter(timeMac[0]);
		document.getElementById("macAddr").innerHTML = "mac "+timeMac[1];
		pullRedis(getRedisUrl(timeMac[0], timeMac[1]), 'min');
	});
	$("div.st").mousedown(function(event){
		if (event.which == 1){ //left click
			var timeMac = $(this).attr('id').split("_",2);
			var win = window.location = jsonUrl + "?unixTime="+timeMac[0]+'&mac='+timeMac[1]+"&logs=1";
			win.focus();
		}
	});
});


function showDetails(){
	var lasttime = 0;
	var uptime = 0;
	var lastErr;
	$.each(data, function(index, value) {
		upt = data[index]['upt'];
		document.getElementById("upt").innerHTML = "uptime: "+formatUptime (upt);
		url = returnChannel(data[index]['url']);
		document.getElementById("url").innerHTML = "url: "+url;
		badStream = data[index]['badStream'];
		document.getElementById("badStream").innerHTML = "badStream: "+badStream;
		ddecodeDrops = data[index]['ddecodeDrops'];
		document.getElementById("ddecodeDrops").innerHTML = "ddecodeDrops: "+ddecodeDrops;
		decodeErr = data[index]['decodeErr'];
		document.getElementById("decodeErr").innerHTML = "decodeErr: "+decodeErr;
		decodeOflow = data[index]['decodeOflow'];
		document.getElementById("decodeOflow").innerHTML = "decodeOflow: "+decodeOflow;
		displayDrops = data[index]['displayDrops'];
		document.getElementById("displayDrops").innerHTML = "displayDrops: "+displayDrops;
		displayErr = data[index]['displayErr'];
		document.getElementById("displayErr").innerHTML = "displayErr: "+displayErr;
		displayOflow = data[index]['displayOflow'];
		document.getElementById("displayOflow").innerHTML = "displayOflow: "+displayOflow;
		iframeErr = data[index]['iframeErr'];
		document.getElementById("iframeErr").innerHTML = "iframeErr: "+iframeErr;
		ptsDrops = data[index]['ptsDrops'];
		document.getElementById("ptsDrops").innerHTML = "ptsDrops: "+ptsDrops;
		ptsOflow = data[index]['ptsOflow'];
		document.getElementById("ptsOflow").innerHTML = "ptsOflow: "+ptsOflow;
		stalled = data[index]['stalled'];
		document.getElementById("stalled").innerHTML = "stalled: "+stalled;
		operaCrash = data[index]['operaCrash'];
		document.getElementById("operaCrash").innerHTML = "operaCrash: "+operaCrash;

	});
}
