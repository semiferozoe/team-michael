<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Course Scheduler</title>
		<link rel="stylesheet" type="text/css" href="rate-classes.css" />
		<link rel="icon" href="https://github.com/semiferozoe/Course-Scheduler/blob/main/website/public_html/images/logo.png?raw=true">
		<link href="table-styling.css" rel="stylesheet"/>
		<meta name="viewport" content="width=device-width, initial-scale=1">
	</head>

    <body>
        <!-- Redirections to Other Tabs -->
		<div class="header">
			<a href="../homepage/homepage.php" class="logo">Course Scheduler</a>
		    <div class="header-right">
				<a href="../homepage/homepage.php">Home</a>
				<a href="../course-scheduler/course-scheduler.php">Course Scheduler</a>
				<a class="active" href="rate-classes.php">Rate Classes</a>
				<a href="../login/logout.php">Log Out</a>
			</div>
		</div>
		

		<div class="bg-img">
			<form action="" method="POST" class="container">
				
				<h1>Class Difficulty Ratings</h1>
				
				<h2> Course Selector: </h2>
				<select name="course_name" class="course_name">
					<option disabled> -- Computer Science -- </option>
					<option selected value="CSC-130">CSC-130</option>
					<option value="CSC-131">CSC-131</option>
					<option value="CSC-132">CSC-132</option>
					<option value="CSC-220">CSC-220</option>
					<option value="CSC-222">CSC-222</option>
					<option value="CSC-265">CSC-265</option>
					<option value="CSC-310">CSC-310</option>
					<option value="CSC-325">CSC-325</option>
					<option value="CSC-330">CSC-330</option>
					<option value="CSC-345">CSC-345</option>
					<option value="CSC-364">CSC-364</option>
					<option value="CSC-405">CSC-405</option>
					<option value="CSC-406">CSC-406</option>
					<option disabled> -- English -- </option>
					<option value="ENGL-101">ENGL-101</option>
					<option value="ENGL-102">ENGL-102</option>
					<option value="ENGL-303">ENGL-303</option>
					<option value="ENGL-363">ENGL-363</option>
					<option disabled> -- Engineering -- </option>
					<option value="ENGR-308">ENGR-308</option>
					<option value="ENGR-315">ENGR-315</option>
					<option disabled> -- Math -- </option>
					<option value="MATH-100">MATH-100</option>
					<option value="MATH-101">MATH-101</option>
					<option value="MATH-103">MATH-103</option>
					<option value="MATH-240">MATH-240</option>
					<option value="MATH-241">MATH-241</option>
					<option value="MATH-242">MATH-242</option>
					<option value="MATH-311">MATH-311</option>
					<option disabled> -- Statistics -- </option>
					<option value="STAT-205">STAT-205</option>
					<option value="STAT-315">STAT-315</option>
					<option value="STAT-409">STAT-409</option>
					<option disabled> -- Accounting -- </option>
					<option value="ACCT-240">ACCT-240</option>
					<option value="ACCT-411">ACCT-411</option>
					<option disabled> -- Biology -- </option>
					<option value="BISC-102">BISC-102</option>
					<option value="BISC-130">BISC-130</option>
					<option value="BISC-131">BISC-131</option>
					<option value="BISC-132">BISC-132</option>
				</select>
				
				<br>
				
					<h2> Choose this Course's Difficulty: </h2>
				<div class="rating">
					<input type="radio" name="rating" value="1"/> 1 (Very Easy) <br>
					<input type="radio" name="rating" value="2"/> 2	(Easy) <br>
					<input type="radio" name="rating" value="3"/ checked> 3	(Normal) <br>
					<input type="radio" name="rating" value="4"/> 4 (Hard) <br>
					<input type="radio" name="rating" value="5"/> 5	(Very Hard) <br>
				</div>
				
				<br>
				
				<input type="submit" class="btn" name="insert" value="Submit Rating"/>
				<p> </p>
				<input type="submit" class="btn" name="show-results" value="Show All Ratings"/>
				<br>
				
			</form>
		</div>

	</body>
</html>


<?php

// Check connection
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

if(isset($_POST['insert'])) {
	
	$course_name = $_POST['course_name'];
	$rating = $_POST['rating'];
	
	$query = "INSERT INTO ratings (course_name,rating) VALUES ('$course_name','$rating')";
    $query_run = mysqli_query($con, $query);
	
	echo "<center style=font-size:30px;color:green;font-family: Arial;font-weight=bold>Thank you for rating $course_name! </center>";
}

if(isset($_POST['show-results'])){


	$query2 = "select course_name,round(avg(rating),2),count(course_name) from ratings group by course_name order by round(avg(rating),2) DESC;";
	$query_run2 = mysqli_query($con, $query2);

	echo "<table border='1'>";
	echo"<tr><th>Course Name</th><th>Average Rating</th><th>Total Ratings</th><tr>\n";
	while($row = mysqli_fetch_assoc($query_run2)) {
		echo"<tr><td>{$row['course_name']}</td><td>{$row['round(avg(rating),2)']}</td><td>{$row['count(course_name)']}</td><tr>\n";
	}
	echo"<center </table> </center>";
	echo "";

}
	
?>
