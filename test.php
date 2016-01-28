<!DOCTYPE HTML>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>VirtualCamp</title>
		<link href="styles.css" type="text/css" rel="stylesheet" />
	</head>

	<body id="index">
		<div id="header">Virtual<span id="title">Camp</span></div>
		<div id="login">
			<h2>Welcome to My<span id="title">Camp</span></h2>
			Username: <input type="text" name="user"><br>
  			Password: <input type="text" name="password"><br>
  			<a id="loginbtn" href="homepage.php">Login</a>
		</div>
		<div>
			<?php
					$server = "titan.csse.rose-hulman.edu";
					$user = "smithij";
					$pass = "qwer";
					$db = array("Database"=>"FBGM3000", "UID"=>$user, "PWD"=>$pass);
					$conn = sqlsrv_connect($server, $db) or die("Couldn't connect to $server");
			?>
		</div>
	</body>
	
</html>