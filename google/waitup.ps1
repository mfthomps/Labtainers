If ($args.Count -ne 1){
    echo "waitup.ps1 <user ID>"
    exit
}
$user=$args[0]
$vm=$user+"-labtainervm"
$ip=./getip.sh $vm_name 
if ($ip -eq "FAIL"){
    echo "Failed to get ip of $vm"
    exit 1
}
Write-Host -NoNewLine "Waiting for ssh port to open on $vm..."
while($true){ 
    $connection = New-Object System.Net.Sockets.TcpClient($ip, 22)
    if ($connection.Connected) {
         Write-Host "SSH port open on $vm" 
         break
    } else { 
         Start-Sleep -s 2
         Write-Host -NoNewLine "."
    }
}
