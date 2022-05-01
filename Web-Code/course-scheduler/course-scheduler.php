<!DOCTYPE html>
<html>
	<head>
		<script src='jquery.js'> </script>
		<script>
			function ajaxPy(){
				$.ajax('pythoncall.php', { success: function(){
					$("#DisplayButt").html('<iframe style="display: block; margin: 0 auto" src="finaltable.txt" width=1000 height=200 frameborder=0 ></iframe>')
				}})
			}
		</script>
		<meta charset="utf-8">
		<title>Course Scheduler</title>
		<link rel="stylesheet" type="text/css" href="course-scheduler.css" />
		<link rel="icon" href="../images/logo.png">
		<meta name="viewport" content="width=device-width, initial-scale=1">
	</head>

    <body>
        <!-- Redirections to Other Tabs -->
		<div class="header">
			<a href="../homepage.html" class="logo">Course Scheduler</a>
		    <div class="header-right">
				<a href="../homepage.html">Home</a>
				<a class="active" href="course-scheduler.html">Course Scheduler</a>
				<a href="../rate-classes/rate-classes.html">Rate Classes</a>
				<a href="../how-it-works/how-it-works.html">How it Works</a>
				<a href="/#about">About</a>
				<a href="../logout.php">Log Out</a>
			</div>
		</div>

		<br>
		<div style="width: 80%; margin: 0 auto; border:thin solid black" id="DisplayButt"></div>	
		<input type='button' id='submitBtn' class='submitBtn' value='submit' onclick="ajaxPy()"></input>
    </body>
</html> 