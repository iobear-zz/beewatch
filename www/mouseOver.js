//Mouse related functions 

document.write( '<br /><br /><div class="kasse">');
document.write( '<div id="macAddr" class="headline">MAC </div>' );
document.write( '<div class="url"></div>' );
document.write( '<div class="tstamp"></div>' );
document.write( '<div class="upt"></div>' );
document.write( '</div><div class="kasse">');
document.write( '<div class="headline">Decoder</div>' );

document.write( '<div class="ddecodeDrops"></div>' );
document.write( '<div class="decodeErr"></div>' );
document.write( '<div class="decodeOflow"></div>' );
document.write( '</div><div class="kasse">');
document.write( '<div class="headline">Display</div>' );
document.write( '<div class="displayDrops"></div>' );
document.write( '<div class="displayErr"></div>' );
document.write( '<div class="displayOflow"></div>' );
document.write( '</div><div class="kasse">');
document.write( '<div class="headline">PTS</div>' );
document.write( '<div class="ptsDrops"></div>' );
document.write( '<div class="ptsOflow"></div>' );

document.write( '</div><div class="kassesidst">');
document.write( '<div class="headline">Misc</div>' );
document.write( '<div class="iframeErr"></div>' );
document.write( '<div class="stalled"></div>' );
document.write( '<div class="badStream"></div>' );
document.write( '<div class="operaCrash"></div>' );
document.write( '</div>');

 $(document).ready(function(){
	$("div.st").mouseenter(function(){
		var timeMac = $(this).attr('id').split("_",2);
		$(".tstamp").html("time "+timeConverter(timeMac[0]));
		$(".macAddr").html("mac "+timeMac[1]);
		pullRedis(getRedisUrl(timeMac[0], timeMac[1]), 'min');
	});
	$("div.st").mousedown(function(event){
		if (event.which == 1){ //left click
			var timeMac = $(this).attr('id').split("_",2);
			//var win = window.location = jsonUrl + "?unixTime="+timeMac[0]+'&mac='+timeMac[1]+"&logs=1";
			var win = window.location = "tail.php?unixTime="+timeMac[0]+'&mac='+timeMac[1]+"&logs=1";
			win.focus();
		}
	});
});

function showDetails(){
	var lasttime = 0;
	var uptime = 0;
	var lastErr;
	$.each(data, function(index, JSONvalue) {
		$.each(JSONvalue, function(name, val) {
			if (name == "upt") {
				val = formatUptime(val);
			}
			$("."+name).html(name + ': ' + val);
		});
	});
}
