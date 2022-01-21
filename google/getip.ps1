$vm=$args[0]
$result=gcloud compute instances describe $vm --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
If ($result -eq $null){
    echo "FAIL"
}else{
    echo $result
    echo $result > myip.txt
}
