<?php

if (!isset($_REQUEST['host']))
        {
         $_REQUEST['host'] = '%';
        }
$host = $_REQUEST['host'];

try{
$dbHandle = new PDO("sqlite:rrd/ntpstatus.sqlite");
}catch( PDOException $exception ){
        echo "Can NOT connect to sqlite3 database ntpstatus.sqlite";
        die($exception->getMessage());
}

$sqlShowLog = "SELECT * FROM status WHERE host LIKE '${host}';";
$result = $dbHandle->query($sqlShowLog);
echo nl2br("date,host,offset,freq,sjit,cjit,wander,disp,jitter\n");
while ($entry = $result->fetch()) {
	$date = $entry['date'];
	$host = $entry['host'];
	$offset = $entry['offset'];
	$freq = $entry['freq'];
	$sjit = $entry['sjit'];
	$cjit = $entry['cjit'];
	$wander = $entry['wander'];
	$disp = $entry['disp'];
	$output = "$date, $host, $offset, $freq, $sjit, $cjit, $wander, $disp, 0\n";
	echo nl2br($output);
}

?>
