<?php
/* Database credentials. Assuming you are running MySQL
server with default setting (user 'root' with no password) */
define('DB_SERVER', 'poffenroth.iad1-mysql-e2-1a.dreamhost.com');
define('DB_USERNAME', 'kota');
define('DB_PASSWORD', 'capstone406');
define('DB_NAME', 'coursescheduler_users');
 
/* Attempt to connect to MySQL database */
$link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
 
// Check connection
if($link === false){
    die("ERROR: Could not connect. " . mysqli_connect_error());
}
?>