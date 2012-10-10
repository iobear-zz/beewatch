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
tailLink ='http://beewatch01.lx.tv.sk.waoo.org/tail.php?mac=' + mac;
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

<div id="data"></div>
<br /><br />
</body>
</html>
