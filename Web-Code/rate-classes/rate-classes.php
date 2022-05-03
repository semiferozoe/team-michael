<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Course Scheduler</title>
		<link rel="stylesheet" type="text/css" href="rate-classes.css" />
		<link rel="icon" href="https://github.com/semiferozoe/Course-Scheduler/blob/main/website/public_html/images/logo.png?raw=true">
		<meta name="viewport" content="width=device-width, initial-scale=1">
	</head>

    <body>
        <!-- Redirections to Other Tabs -->
		<div class="header">
			<a href="homepage.html" class="logo">Course Scheduler</a>
		    <div class="header-right">
				<a href="../homepage/homepage.html">Home</a>
				<a href="../course-scheduler/course-scheduler.html">Course Scheduler</a>
				<a class="active" href="rate-classes/rate-classes.php">Rate Classes</a>
				<a href="../homepage/homepage.html#news">News</a>
				<a href="../about-us/about">About</a>
				<a href="../login/logout.php">Log Out</a>
			</div>
		</div>
		

		<div class="bg-img">
			<form action="" method="POST" class="container">
				
				<h1>Class Difficulty Ratings</h1>
				
				<h2> Course Selector: </h2>
				<select name="course_name" class="course_name">
					<option value="csc130">CSC-130</option>
					<option value="csc131">CSC-131</option>
					<option value="csc132">CSC-132</option>
					<option>------------------------------</option>
					<option value="math101">MATH-101</option>
					<option value="math240">MATH-240</option>
					<option value="math311">MATH-311</option>
				</select>
				
				<br>
				
				
					<h2> Choose this Course's Difficulty: </h2>
				<div class="rating">
					<input type="radio" name="rating" value="1"/> 1 (Very Easy) <br>
					<input type="radio" name="rating" value="2"/> 2	(Easy) <br>
					<input type="radio" name="rating" value="3"/> 3	(Normal) <br>
					<input type="radio" name="rating" value="4"/> 4 (Hard) <br>
					<input type="radio" name="rating" value="5"/> 5	(Very Hard) <br>
				</div>
				
				<br>
				
				<input type="submit" class="btn" name="insert" value="Submit Rating"/>
				<p> </p>
				<input type="submit" class="btn" name="show-results" value="Show All Ratings"/>
			
			</form>
		</div>

	</body>
</html>


<?php

// Check connection
$DATABASE_HOST = 'poffenroth.iad1-mysql-e2-1a.dreamhost.com';
$DATABASE_USER = 'kota';
$DATABASE_PASS = 'capstone406';
$DATABASE_NAME = 'coursescheduler_users';
// Try and connect using the info above.
$con = mysqli_connect($DATABASE_HOST, $DATABASE_USER, $DATABASE_PASS, $DATABASE_NAME);
if (mysqli_connect_errno()) {
	// If there is an error with the connection, stop the script and display the error.
	exit('Failed to connect to MySQL: ' . mysqli_connect_error());
}


if(isset($_POST['insert'])) {
	
	$course_name = $_POST['course_name'];
	$rating = $_POST['rating'];
	
	$query = "INSERT INTO ratings (course_name,rating) VALUES ('$course_name','$rating')";
    $query_run = mysqli_query($con, $query);
}


?>