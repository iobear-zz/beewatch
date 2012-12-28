<html>
<head>
<meta http-equiv="Content-Type" content="text/html" charset="UTF-8" />
<title>Beewatch</title>
<script src="jquery.min.js"></script>
<script src="settings.js"></script>
<script src="cookie.js"></script>
<script src="airties.js"></script>
<script src="main.js"></script>
<script src="utils.js"></script>
<script src="channels.js"></script>

<?php
$macIN = $_REQUEST['mac'];
$days = $_REQUEST['days'];
$macIM = ereg_replace("[^A-Fa-f0-9]", "", $macIN );
$mac=substr($macIM, 0, 12);
$mac = strtoupper($mac);
echo "<script>";
echo "mac='".$mac."';";
echo "days='".$days."';";
?>
var tailLink ='http://' + window.location.hostname + '/tail.php?mac=' + mac;
function goToTail() {
	window.location = tailLink;
}
</script>
<?php

if ($mac) {
	echo '<button onclick="bookmarkBox(mac)">bookmark</button> ';
	echo '<button onclick="goToTail()">tail</button><br /><br />';
}
?>

</head>
<link href="default.css" rel="stylesheet" type="text/css">
<body>
<script>
if (mac) {
	calcDisplay('days',days,mac,daysago);
	pullRedis(getRedisUrl('',mac,days,0), 'days');
}
</script>
<script src="mouseOver.js"></script>
<br /><br />
<div class="kasse">
	<div id="macAddr" class="headline">MAC </div>
	<div class="url"></div>
	<div class="tstamp"></div>
	<div class="upt"></div>
	<div class="uptSec"></div>
	<div class="fw"></div>
</div>
<div class="kasse">
	<div class="headline">Decoder</div>
	<div class="ddecodeDrops"></div>
	<div class="decodeErr"></div>
	<div class="decodeOflow"></div>
</div>
<div class="kasse">
	<div class="headline">Display</div>
	<div class="displayUflow"></div>
	<div class="displayDrops"></div>
	<div class="displayErr"></div>
</div>
<div class="kasse">
	<div class="headline">Misc</div>
	<div class="ptsError"></div>
	<div class="Discontinuity"></div>
	<div class="iframeErr"></div>
</div>
<div class="kassesidst">
	<div class="headline">Misc</div>
	<div class="stalled"></div>
	<div class="badStream"></div>
	<div class="operaCrash"></div>
</div>
</script>
<br /><br />

<div id="data"></div>
</body>
</html>
