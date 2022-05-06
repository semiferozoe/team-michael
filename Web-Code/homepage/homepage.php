<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Course Scheduler</title>
		<link rel="stylesheet" type="text/css" href="homepage.css" />
		<link rel="icon" href="https://github.com/semiferozoe/Course-Scheduler/blob/main/website/public_html/images/logo.png?raw=true">
		<meta name="viewport" content="width=device-width, initial-scale=1">
	</head>

    <body>
        <!-- Redirections to Other Tabs -->
		<div class="header">
			<a href="../homepage/homepage.php" class="logo">Course Scheduler</a>
		    <div class="header-right">
				<a class="active" href="/homepage.php">Home</a>
				<a href="../course-scheduler/course-scheduler.php">Course Scheduler</a>
				<a href="../rate-classes/rate-classes.php">Rate Classes</a>
				<a href="../login/logout.php">Log Out</a>
			</div>
		</div>


<!-- Front Building Background with M logo overlay -->
<div class="bgimg-1">
	<div class="bgimg-0"> </div>
  <span class="border" style="background-color:transparent;font-size:25px;color: #f7f7f7;"></span>
  </div>
</div>


<!-- Contact Us -->
<div class="footer"style="color:#ddd;background-color:#54626F;padding:20px 100px;text-align: justify;">
	<h3 style="text-align:center; color:white; line-height:90%;">▼ Contact Us! ▼</h3>
    <br>
    <p style="line-height:20%; text-align:center;">The team members affiliated with this project with their respective roles:</p>
	<p style="line-height:20%; text-align:center;">Python Developer: Broady Rivet</p>
    <p style="line-height:20%; text-align:center;">Website Developers: Dakota Hollis and Zoe Semifero</p>
    <br style="line-height:20%;">
    <p style="line-height:20%; text-align:center;">If you have any questions or feedback, please do not hesistate to send us an email!</p>
    <p style="line-height:20%; text-align:center;">Course.Scheduler406@gmail.com</p>
</div>

</body>
</html>


<?php
// This will check to ensure user has logged in before being able to access the page.
$DATABASE_HOST = 'brahney.iad1-mysql-e2-7a.dreamhost.com';
$DATABASE_USER = 'kota';
$DATABASE_PASS = 'capstone406';
$DATABASE_NAME = 'coursescheduler_users';
// Try and connect using the info above.
$con = mysqli_connect($DATABASE_HOST, $DATABASE_USER, $DATABASE_PASS, $DATABASE_NAME);
if (mysqli_connect_errno()) {
	// If there is an error with the connection, stop the script and display the error.
	exit('Failed to connect to MySQL: ' . mysqli_connect_error());
}

// Needs work
?>

