If ($args.Count -ne 1){
    echo "waitdone.ps1 <user ID>"
    exit
}
$user=$args[0]
# start the tunnel and wait for it to die, reflecting reboot.
echo "start the tunnel"
Start-Sleep -s 5
./checktunnel.ps1 $user  
Start-Sleep -s 5
./wait_tunnel.ps1 $user 
echo "Tunnel gone, wait 20 for reboot"
Start-Sleep -s 20
./waitweb.ps1 $user
