<html>
<head>
<meta http-equiv="Content-Type" content="text/html" charset="UTF-8" />
<title>beewatch - tail</title>
<?php
 $macIN = $_REQUEST['mac'];
 $macIM = ereg_replace("[^A-Fa-f0-9]", "", $macIN );
 $mac=substr($macIM, 0, 12);
 $mac = strtoupper($mac);
 echo "<script type=\"text/javascript\">";
 echo "mac='".$mac."';";
 echo "</script>";
?>
<script src="jquery.min.js"></script>
<script type="text/javascript"> 
    var lastByte = 0;

    if (typeof XMLHttpRequest == "undefined") {
		// this is only for really ancient browsers
		XMLHttpRequest = function () {
			try { return new ActiveXObject("Msxml2.xmlHttp.6.0"); }
			catch (e1) {}
			try { return new ActiveXObject("Msxml2.xmlHttp.3.0"); }
			catch (e2) {}
			try { return new ActiveXObject("Msxml2.xmlHttp"); }
			catch (e3) {}
			throw new Error("This browser does not support xmlHttpRequest.");
		};
	}

	function tailf() {
		if (mac) {
			var url = 'http://beewatch01.lx.tv.sk.waoo.org/readjson.php?mac=' + mac + '&tail=1';
			var ajax = new XMLHttpRequest();
			ajax.open("POST",url,true);
		}
		if (lastByte == 0) {
			// First request - get everything
		} else {
			// All subsequent requests - add the Range header
			ajax.setRequestHeader("Range", "bytes=" + parseInt(lastByte) + "-");
		}

		ajax.onreadystatechange = function() {
			if(ajax.readyState == 4) {
				if (ajax.status == 200) {
					// only the first request
					lastByte = parseInt(ajax.getResponseHeader("Content-length"));
					document.getElementById("thePlace").innerHTML = ajax.responseText;
					document.getElementById("theEnd").scrollIntoView()
				} else if (ajax.status == 206) {
					lastByte += parseInt(ajax.getResponseHeader("Content-length"));
					document.getElementById("thePlace").innerHTML += ajax.responseText;
					document.getElementById("theEnd").scrollIntoView()
				} else if (ajax.status == 416) {
					// no new data, so do nothing
				} else {
					//  Some error occurred - just display the status code and response
					alert("Ajax status: " + ajax.status + "\n" + ajax.getAllResponseHeaders());
				}
			}
		}
		ajax.send(null);
    }

	var myTimer;
	function stopLog(val) {
		window.clearInterval(val);
		$('#stopButton').hide();
	}

</script>
</head>
<body onLoad='tailf(); myTimer = setInterval("tailf()", 5000)'>
<div>
	<pre id="thePlace"></pre>
<div id="theEnd"></div>
 <div id="stopButton"><button onclick='stopLog(myTimer)'>Stop</button></div>
</div>
</body>
</html>