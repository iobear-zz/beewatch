<html lang="en">
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<meta http-equiv="Content-Type" content="text/html" charset="UTF-8" />
		<title>Beewatch</title>
		<link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
		<link href="css/bootstrap-responsive.css" rel="stylesheet" media="screen">
		<link href="css/beewatch.css" rel="stylesheet" type="text/css">
	</head>
	<body>
		<br/><div class="container"><br/><br/>
		<script src="jslib/jquery.min.js"></script>
		<script src="jslib/jqURL.js"></script>
		<script src="settings.js"></script>
		<script src="cookie.js"></script>
		<script src="utils.js"></script>
		<script src="airties.js"></script>
		<script src="main.js"></script>
		<script src="channels.js"></script>
		<script src="index2.js"></script>
		<script src="jslib/bootstrap.min.js"></script>
		<br />

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
	
			<div class="navbar navbar-inverse navbar-fixed-top">
				<div class="navbar-inner">
					<div class="container">
						<button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse"></button>
						<div class="nav-collapse collapse">
							<ul class="nav">
								<li><a href="index.html" data-toggle="tab">Home</a></li>
							</ul>
						</div><!--/.nav-collapse -->
					</div>
				</div>
			</div>

		<?php
			if ($mac) {
				echo '<button onclick="bookmarkBox(mac)">bookmark</button> ';
				echo '<button onclick="goToTail()">tail</button>';
			}
		?>

		<button id="extraLog" onclick="extraLog(ip, mac)">extra log</button><br /><br />
		<script>
			if (mac) {
				calcDisplay('days',days,mac,daysago);
				pullRedis(getRedisUrl('',mac,days,0), 'days');
			}
		</script>
		<?php
			if ($mac) {
				echo "<br/><br/>";
			}
		?>

		<script src="mouseOver.js"></script>
		
		<div class="kasse">
			<div id="macAddr" class="headline">MAC </div>
			<div class="url"></div>
			<div class="tstamp"></div>
			<div class="upt"></div>
			<div class="uptSec"></div>
			<div class="fw"></div>
		</div>
		<div class="kasse">
			<div class="headline">Misc</div>
			<div class="ptsError"></div>
			<div class="Discontinuity"></div>
			<div class="iframeErr"></div>
			<div class="ip"></div>
		</div>
		<div class="kasse">
			<div class="headline">Misc</div>
			<div class="stalled"></div>
			<div class="badStream"></div>
			<div class="operaCrash"></div>
		</div>
		<div class="kasse">
			<div class="headline">Decoder</div>
			<div class="ddecodeDrops"></div>
			<div class="decodeErr"></div>
			<div class="decodeOflow"></div>
		</div>
		<div class="kassesidst">
			<div class="headline">Display</div>
			<div class="displayUflow"></div>
			<div class="displayDrops"></div>
			<div class="displayErr"></div>
		</div>
		<br /><br />
	</div>
		<div id="data"></div>
	</body>
</html>
