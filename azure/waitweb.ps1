If ($args.Count -ne 1){
    echo "waitweb.ps1 <user ID>"
    exit
}
$ErrorActionPreference = "Stop"
$user_id=$args[0]
$vm_name=$user_id+"-labtainervm"
echo "start the tunnel"
./checktunnel.ps1 $user_id
if(test-path index.html){
    remove-item index.html
}
Write-Host -NoNewLine "Waiting for remote Labtainers to become available..."
while($true){ 
    try{Invoke-WebRequest -Uri http://localhost:6901 -OutFile index.html}
    catch{Write-Host -NoNewLine "."}
    if (test-path index.html){
        echo "Web server is up."
        break
    }
    Start-Sleep -s 20
}
echo "Labtainers is up.  Point browser to localhost:6901"
