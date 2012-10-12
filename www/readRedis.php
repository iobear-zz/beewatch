<?php
$unixTime = 0;
$unixTime = $_REQUEST['unixTime'];
$mac = $_REQUEST['mac'];
$days = $_REQUEST['days'];
$offset = $_REQUEST['offset'];

header('Cache-Control: no-cache, must-revalidate');
header('Expires: Wed, 2 Apr 1975 15:00:00 GMT');
header('Content-type: application/json');
header('Charset: UTF-8');

require "predis/autoload.php";
Predis\Autoloader::register();
try {
	$redis = new Predis\Client();
}
catch (Exception $e) {
	echo "Couldn't connected to Redis";
	echo $e->getMessage();
}

function makeHashArray($stuff) {
	foreach($stuff as $nogle){
		$nystreng = split(':', $nogle);
		$nytArray[$nystreng[0]] = $nystreng[1];
	}
	return $nytArray;
}

if ($unixTime) {
	$amountOfLoops = 1;
	$startTime = $unixTime;
} else {
	$amoutOfLoops = 86400 * ($days) / 300;
	$days = $days -1;
	$startTime = mktime(0, 0, 0, date('n'), date('j') - $days-$offset);
}

$i = 0;
if ($_REQUEST['logs'] == 1) { //dispay raw logs
	$amoutOfLoops = 2;
	$startTime = $startTime - 300;
	while($i<=$amoutOfLoops) {
		$redisString = "log".$startTime.$mac;
		$redisAnswer = $redis->zrange($redisString, 0, -1);
		if ($redisAnswer) {
			foreach($redisAnswer as $nogle){	
				echo $nogle;
			}
		}
		$i++;
		$startTime = $startTime + 300;
	}
} elseif ($_REQUEST['tail'] == 1) {	//tail logs
	$startTime = mktime(date(H),date(i),0,date(n),date(d),date(Y)); //sec = 00
	$startTime = round(($startTime+120)/300)*300; // force 5 min timeslot
	$startTime = $startTime - 300;
	
	while($i<=$amoutOfLoops) {
		$amoutOfLoops = 1;
		$redisString = "log".$startTime.$mac;
		$redisAnswer = $redis->zrange($redisString, 0, -1);
		if ($redisAnswer) {
			foreach($redisAnswer as $nogle){	
				echo $nogle;
			}
		}
		$i++;
		$startTime = $startTime + 300;
	}
} elseif ($_REQUEST['json'] == 1) { //display json format
	echo "[";
	$f = 0;
	while($i<=$amoutOfLoops) {
		$redisString = $startTime.$mac;
		$redisAnswer = $redis->zrange($redisString, 0, -1);
		if ($redisAnswer) {
			if ($f != 0) {
				echo ",";
			}
			echo json_encode(makeHashArray($redisAnswer));
			$f++;
		}
		$i++;
		$startTime = $startTime + 300;
	}
	echo "]";
} elseif ($_REQUEST['ipstart']) {
	if ($_REQUEST['ipend']) {
		$ipstart = $_REQUEST['ipstart'];
		$ipend = $_REQUEST['ipend'];
		if (is_numeric($ipend) && is_numeric($ipstart) && ($ipstart < $ipend)) {
			while ($ipend >= $ipstart) {
				echo $redis->get($ipstart);
				$ipstart++;
			}
		}
	} else {
		echo $redis->get($_REQUEST['ipstart']);
	}
}

?>
