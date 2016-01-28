<!DOCTYPE HTML>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>VirtualCamp</title>
		<link href="styles.css" type="text/css" rel="stylesheet" />
	</head>

	<body>
		<div id="header">
			Virtual<span id="title">Camp</span><span id="logout"><a href="index.php">logout</a></span>
		</div>
		<h1>Shelbyville Parks Dept. Day Camp</h1>
		<table>
			<tr>
				<td id="todayAttendance">
				<ul>
					Today's Attendance
					<hr />
					<?php
					$server = "titan.csse.rose-hulman.edu";
					$user = "smithij";
					$pass = "qwerty123";
					$db = array("Database"=>"FBGM3000", "UID"=>$user, "PWD"=>$pass);
					print_r("getting here");
					$conn = sqlsrv_connect($server, $db) or die("Couldn't connect to $server");
					if($conn){
						echo "Good Job!";
					}else{
						echo "I hate this...";
						die( print_r( sqlsrv_errors(), true));
					}

					$query = "exec GetTodaysAttendance";

					$result = sqlsrv_query($conn, $query);

					//display the results
					while ($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)) {
						echo "
					<li>
						" . $row["Fname"] . " " . $row["Lname"] . "
					</li>";
					}
					sqlsrv_free_stmt($result);
					?>
					</ul></td>
					<td id="links">
					<ul>
					Links
					<hr id="right"/>
					<li></li>
					</ul></td>
					</tr>
					</table>

					<div id="footer">
					[Copyright info] [other junk]<span id="logout">Logout</span>
					</div>
					</body>

					</html>
				