If ($args.Count -ne 1){
    echo "waitdone.ps1 <user ID>"
    exit
}
$user=$args[0]
./checktunnel.ps1 $user 
if(test-path index.html){
    remove-item index.html
}
Write-Host -NoNewLine "Waiting for remote Labtainers to become available.  Please be patient."
while($true){ 
    try{Invoke-WebRequest -Uri http://localhost:6901 -OutFile index.html}
    catch{Write-Host -NoNewLine "."}
    if (test-path index.html){
        echo "Web server is up."
        break
    }
    Start-Sleep -s 20
}
echo "Labtainers is up.  Point a browser to http://localhost:6901"
