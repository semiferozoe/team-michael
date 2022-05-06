<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Course Scheduler</title>
		<link rel="stylesheet" type="text/css" href="course-scheduler.css" />
		<link rel="icon" href="../images/logo.png">
		<meta name="viewport" content="width=device-width, initial-scale=1">
	</head>

    <body>
        <!-- Redirections to Other Tabs -->
		<div class="header">
			<a href="../homepage/homepage.php" class="logo">Course Scheduler</a>
		    <div class="header-right">
				<a href="../homepage/homepage.php">Home</a>
				<a class="active" href="course-scheduler.php">Course Scheduler</a>
				<a href="../rate-classes/rate-classes.php">Rate Classes</a>
				<a href="../login/logout.php">Log Out</a>
			</div>
		</div>

		<br>
		<div class="bg-img">
			<form action="" method="POST" class="container">
				<h3>Your advisor has uploaded your schedule.</h3>
				<div style="width: 100%; margin: 0 auto" id="DisplayButt"></div>
				
				<script src='jquery.js'> </script>
				<script>
					function ajaxPy(){
						$.ajax('pythoncall.php', { success: function(){
						$("#DisplayButt").html('<iframe style="display: block; margin: 0 auto" src="finaltable.txt" width=935 height=200 frameborder=0 ></iframe>')
						}})
					}
				</script>
				<br>
				<input type='button' id='submitBtn' class='submitBtn' value='Click to View' onclick="ajaxPy()"></input>
			</form>
		</div>
    </body>
</html> 