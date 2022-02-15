If ($args.Count -ne 1){
    echo "wait_tunnel.ps1 <user ID>"
    exit
}
$user=$args[0]
$vm=$user+"-labtainervm"
Write-Host -NoNewLine "Waiting for VM to provision and reboot.  This may take a few minutes..."
while($true){
    $result=netstat -an | findstr 6901
    If ($result -eq $null){
        echo "gone"
        exit
    }else{
        Write-Host -NoNewLine "."
        Start-Sleep -s 5
    }
}
