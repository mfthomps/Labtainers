<!-- 
SEED Lab: SQL Injection Education Web plateform
Author: Kailiang Ying
Email: kying@syr.edu
-->

<!DOCTYPE html>
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
   $input_eid = $_GET['EID'];
   $input_pwd = $_GET['Password']; 
   $input_pwd = sha1($input_pwd);

   // check if it has exist login session
   session_start(); 
   if($input_eid=="" and $input_pwd==sha1("") and $_SESSION['name']!="" and $_SESSION['pwd']!=""){
      $input_eid = $_SESSION['eid'];
      $input_pwd = $_SESSION['pwd']; 
   } 
   
   $conn = getDB();

   /* start make change for prepared statement */
   $sql = "SELECT id, name, eid, salary, birth, ssn, phoneNumber, address, email,nickname,Password 
           FROM credential 
           WHERE eid= '$input_eid' and Password='$input_pwd'";
   if (!$result = $conn->query($sql)) {
       die('There was an error running the query [' . $conn->error . ']\n');
   }

   /* convert the select return result into array type */ 
   $return_arr = array();
   while($row = $result->fetch_assoc()){
       array_push($return_arr,$row);
   }

   /* convert the array type to json format and read out*/ 
   $json_str = json_encode($return_arr);
   $json_a = json_decode($json_str,true);
   $id = $json_a[0]['id'];
   $name = $json_a[0]['name'];
   $eid = $json_a[0]['eid'];
   $salary = $json_a[0]['salary'];
   $birth = $json_a[0]['birth'];
   $ssn = $json_a[0]['ssn'];
   $phoneNumber = $json_a[0]['phoneNumber'];
   $address = $json_a[0]['address'];
   $email = $json_a[0]['email'];
   $pwd = $json_a[0]['Password'];
   $nickname = $json_a[0]['nickname'];
   if($id!=""){
   	drawLayout($id,$name,$eid,$salary,$birth,$ssn,$pwd,$nickname,$email,$address,$phoneNumber); 
   }else{
	echo "The account information your provide does not exist\n"; 
	return;
   }
   /* end change for prepared statement */ 

   $conn->close();	

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

function   drawLayout($id,$name,$eid,$salary,$birth,$ssn,$pwd,$nickname,$email,$address,$phoneNumber){ 
   if($id!=""){
   	   session_start(); 
           $_SESSION['id'] = $id;	
	   $_SESSION['eid'] = $eid;
           $_SESSION['name'] = $name;	
	   $_SESSION['pwd'] = $pwd;
   }else{
	echo "can not assign session";
   }
   if ($name !="Admin") {
   	echo "<br><h3> $name Profile</h3>";
	echo "<table>"; echo "<tr>"; echo "<td>Employee ID</td>";
  	echo "<td>$eid</td>";
	echo "</tr>";
	echo "<tr>";
	echo "<td>Salary</td>";
  	echo "<td>$salary</td>";
	echo "</tr>";
	echo "<tr>";
	echo "<td>Birth</td>";
  	echo "<td>$birth</td>";
	echo "</tr>";
	echo "<tr>";
	echo "<td>SSN</td>";
  	echo "<td>$ssn</td>";
	echo "</tr>";
	echo "<tr>";
	echo "<td>NickName</td>";
  	echo "<td>$nickname</td>";
	echo "</tr>";
	echo "<tr>";
	echo "<td>Email</td>";
  	echo "<td>$email</td>";
	echo "</tr>";
	echo "<tr>";
	echo "<td>Address</td>";
  	echo "<td>$address</td>";
	echo "</tr>";
	echo "<tr>";
	echo "<td>Phone Number</td>";
  	echo "<td>$phoneNumber</td>";
	echo "</tr>";
	echo "</table>";
   }
   else {
        $conn = getDB();
   	$sql = "SELECT id, name, eid, salary, birth, ssn, password, nickname, email, address, phoneNumber 
           FROM credential"; 
   	if (!$result = $conn->query($sql)) {
       		die('There was an error running the query [' . $conn->error . ']\n');
   	}
   	$return_arr = array();
   	while($row = $result->fetch_assoc()){
       		array_push($return_arr,$row);
   	}
   	$json_str = json_encode($return_arr);
   	$json_aa = json_decode($json_str,true);
        $conn->close();	
        $max = sizeof($json_aa);  	
        for($i=0; $i< $max;$i++){
	   //TODO: printout all the data for that users. 		
  	   $i_id = $json_aa[$i]['id']; 
  	   $i_name= $json_aa[$i]['name']; 
  	   $i_eid= $json_aa[$i]['eid']; 
  	   $i_salary= $json_aa[$i]['salary']; 
  	   $i_birth= $json_aa[$i]['birth']; 
  	   $i_ssn= $json_aa[$i]['ssn']; 
           $i_pwd = $json_aa[$i]['Password'];
  	   $i_nickname= $json_aa[$i]['nickname']; 
  	   $i_email= $json_aa[$i]['email']; 
  	   $i_address= $json_aa[$i]['address']; 
  	   $i_phoneNumber= $json_aa[$i]['phoneNumber']; 
   	   echo "<br><h4> $i_name Profile</h4>";
  	   echo "Employee ID: $i_eid     ";
   	   echo "salary: $i_salary     ";
   	   echo "birth: $i_birth    ";
   	   echo "ssn: $i_ssn    ";
   	   echo "nickname: $i_nickname";
   	   echo "email: $i_email";
   	   echo "address: $i_address";
   	   echo "phone number: $i_phoneNumber";
	}
   }
}
?>

<div class=wrapperL>
<p>
<button onclick="location.href = 'edit.php';" id="editBtn" >Edit Profile</button>
</p>
</div>


<div id="page_footer" class="green">
<p>
Copyright &copy; SEED LABs
</p>
</div>
</body>
</html> 
