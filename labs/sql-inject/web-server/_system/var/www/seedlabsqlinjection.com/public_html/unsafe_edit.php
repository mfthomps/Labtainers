<!-- 
SEED Lab: SQL Injection Education Web plateform
Author: Kailiang Ying
Email: kying@syr.edu
-->

<!DOCTYPE html>
<html>
<body>


<?php
   session_start(); 
   $input_email = $_GET['Email'];
   $input_nickname = $_GET['NickName'];
   $input_address= $_GET['Address'];
   $input_pwd = $_GET['Password']; 
   $input_phonenumber = $_GET['PhoneNumber']; 
   $input_id = $_SESSION['id'];
   $conn = getDB();
  
   // Don't do this, this is not safe against SQL injection attack
   $sql="";
   if($input_pwd!=''){
   	$input_pwd = sha1($input_pwd);
   	$sql = "UPDATE credential SET nickname='$input_nickname',email='$input_email',address='$input_address',Password='$input_pwd',PhoneNumber='$input_phonenumber' where ID=$input_id;";
   }else{
   	$sql = "UPDATE credential SET nickname='$input_nickname',email='$input_email',address='$input_address',PhoneNumber='$input_phonenumber' where ID=$input_id;";
   }
   $conn->query($sql);
   $conn->close();	
   header("Location: unsafe_credential.php");
   exit();

function getDB() {
   $dbhost="localhost";
   $dbuser="root";
   $dbpass="seedubuntu";
   $dbname="Users";


   // Create a DB connection
   $conn = new mysqli($dbhost, $dbuser, $dbpass, $dbname);
   if ($conn->connect_error) {
         die("Connection failed: " . $conn->connect_error . "\n");
   }
return $conn;
}
 
?>

</body>
</html> 
