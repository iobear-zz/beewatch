<?php
$unixTime = $_REQUEST['unixTime'];
$mac = $_REQUEST['mac'];
$logs = $_REQUEST['logs'];
$days = $_REQUEST['days'];
$offset = $_REQUEST['offset'];
$tail = $_REQUEST['tail'];

header('Cache-Control: no-cache, must-revalidate');
header('Expires: Wed, 2 Apr 1975 15:00:00 GMT');
header('Content-type: application/json');
header('Charset: UTF-8');

//if ($unixTime) {
//$unixTime = (intval($unixTime)+120)/300*300;
//$unixTime = ($unixTime+120)/300*300;
//round to strict 5 min interval
//}

require "predis/autoload.php";
Predis\Autoloader::register();

try {
    $redis = new Predis\Client();
}
catch (Exception $e) {
    echo "Couldn't connected to Redis";
    echo $e->getMessage();
}

$days = $days -1;

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
	$amoutOfLoops = 86400 * ($days + 1) / 300;
	if ($offset) {
		$startTime = mktime(0, 0, 0, date('n'), date('j') - $days-$offset);
	} else {
		$startTime = mktime(0, 0, 0, date('n'), date('j') - $days-$offset);
	}
}

$i = 0;
if ($logs == 1) { //dispay raw logs
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
} elseif ($tail== 1) {	//tail logs
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
} else { //display json format
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
}
?>
