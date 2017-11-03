<!-- 
SEED Lab: SQL Injection Education Web plateform
Author: Kailiang Ying
Email: kying@syr.edu
-->
<html>
<body>

<!-- link to ccs-->
<link href="style_home.css" type="text/css" rel="stylesheet">

<div class=wrapperR>
<p>
<button onclick="location.href = 'logoff.php';" id="logoffBtn" >LOG OFF</button>
</p>
</div>

<?php
   session_start(); 
   echo "Hi,".$_SESSION["name"];
?>

<br>
<br>
<div class=wrapper>
<h3> Edit Profile Information</h3>
</div>
<form action="unsafe_edit.php" method="get">
<div class="buttonHolder">
<label>Nick Name:</label> <input type="text" name="NickName" ><br>
<label>Email :</label> <input type="text" name="Email"><br>
<label>Address:</label> <input type="text" name="Address"><br>
<label>Phone Number:</label> <input type="text" name="PhoneNumber"><br>
<label>Password:</label> <input type="password" name="Password"><br>
<button type="edit">Edit</button>
</div>
</form>

<div id="page_footer" class="green">
<p>
Copyright &copy; SEED LABs
</p>
</div>
</body>
</html>

