If ($args.Count -ne 1){
    echo "checktunnel.ps1 <user ID>"
    exit
}
$user=$args[0]
$suffix = "-labtainervm"
$vm=$user+$suffix
echo "get the IP for $vm"
$ip=./getip.ps1 $vm

if ($ip -eq "FAIL"){
    echo "Failed to get ip of $vm"
    exit 1
}
$result=netstat -an | Select-String -pattern "6901"
If ($result -eq $null){
    echo "No tunnel, create one."
      $fname=$HOME+"\.ssh\id_labtainers"
     ./dotunnel.bat $fname $ip
}else{
       echo "Proper tunnel already exists."
}
