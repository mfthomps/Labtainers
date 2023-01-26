$vm=$args[0]
$zone=./findzone.ps1
$result=gcloud compute instances describe $vm --format='get(networkInterfaces[0].accessConfigs[0].natIP)' --zone=$zone
If ($result -eq $null){
    echo "FAIL"
}else{
    echo $result
    echo $result > myip.txt
}
