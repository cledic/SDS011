<?php
try {
	/*** connect to SQLite database ***/
	$dbh = new PDO("sqlite:/media/data/SDS011Data.sqlite");
}

catch(PDOException $e)
{
	echo $e->getMessage();
}

$dati_temp="";
$dati_umid="";
$dati_press="";
$dati_time="";

// Search for the last day recordered.
$stmt = $dbh->prepare("select date as dm from samples  group by date order by date desc;");
$stmt->execute();
$row = $stmt->fetch();
$dati_data = $row['dm'];
$dt_from = $row['dm'];

// First select to read value 24 hours later
$sql = "select strftime('%H', time) as tm, AVG(temp) as temp_avg, AVG(press) as press_avg, AVG(umid) as umid_avg from samples where (date >= date('now','-1 day')) and (time >= strftime('%H', time('now','localtime'))) GROUP BY date(time), strftime('%H', time);";

foreach ($dbh->query($sql) as $row) 
{
    #
    $dati_temp = $dati_temp . "," . $row['temp_avg'];
    $dati_umid = $dati_umid . "," . $row['umid_avg'];
    $dati_press = $dati_press . "," . $row['press_avg'];
    $dati_time = $dati_time . ",\"h".$row['tm'].":00\"";
}

// Select the data after averaging the values sampled by an hour
$sql = "select strftime('%H', time) as tm, AVG(temp) as temp_avg, AVG(press) as press_avg, AVG(umid) as umid_avg from samples where (date >= '$dati_data') GROUP BY date(time), strftime('%H', time);";

foreach ($dbh->query($sql) as $row) 
{
    #
    $dati_temp = $dati_temp . "," . $row['temp_avg'];
    $dati_umid = $dati_umid . "," . $row['umid_avg'];
    $dati_press = $dati_press . "," . $row['press_avg'];
    $dati_time = $dati_time . ",\"h".$row['tm'].":00\"";
}

$dbh = null;

// Removing the first comma
$dati_temp = substr($dati_temp, 1);
$dati_umid = substr($dati_umid, 1);
$dati_press = substr($dati_press, 1);
$dati_time = substr($dati_time, 1);

// Format the string for Javascript
$dati_temp = "[".$dati_temp."],";
$dati_umid = "[".$dati_umid."],";
$dati_press = "[".$dati_press."],";
$dati_time = "[".$dati_time."],\n";
?>

<!doctype html>
<html>
	<head>
		<title>Valori di Temperatura, Pressione e Umidita giornalieri</title>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js"></script>
		<meta name = "viewport" content = "initial-scale = 1, user-scalable = yes">
		<style>
			canvas{
			}
		</style>
	</head>
	<body>
		<canvas id="line-chart" width="800" height="640"></canvas>
	<script>

new Chart(document.getElementById("line-chart"), {
  type: 'line',
  data: {
    labels: <?php echo $dati_time ?>
    datasets: [{ 
        data: <?php echo $dati_temp ?>
        yAxisID: "y-axis-0",
        label: "Temperatura",
        borderColor: "#3e95cd",
        fill: true
      }, { 
        data: <?php echo $dati_umid ?>
        yAxisID: "y-axis-0",
        label: "Umidita %",
        borderColor: "#8e5ea2",
        fill: true
      }, { 
        data: <?php echo $dati_press ?>
        yAxisID: "y-axis-1",
        label: "Pressione Atmosferica",
        borderColor: "#c45850",
        fill: true
      }
    ]
  },
  options: {
    scales: {
      yAxes: [{
      scaleLabel: {
        display: true,
        labelString: ' Temperatura e Umidita\' ',
		fontSize : 16
      },		  
        position: "left",
        "id": "y-axis-0"
      }, {
      scaleLabel: {
        display: true,
        labelString: ' Pressione Atmosferica hPa ',
		fontSize : 16,
		fontColor : "#c45850",
      },		  
        position: "right",
        "id": "y-axis-1"
      }],
	  xAxes: [{
      scaleLabel: {
        display: true,
        labelString: ' Letture orarie da ieri a oggi ',
		fontSize : 22
      }
    }]
	  
    },
    title: {
      display: true,
      text: 'Valori di Temperatura, Pressione ed Umidita\' nelle 24h'
    },
	// Boolean - whether or not the chart should be responsive and resize when the browser does.
	responsive: true,
	// Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
	maintainAspectRatio: false,
  }
});	
	</script>
	</body>
</html>
