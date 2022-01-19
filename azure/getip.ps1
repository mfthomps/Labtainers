$resource=$args[0]
$vm=$args[1]
$result=az vm show -d -g $resource -n $vm --query publicIps -o tsv
If ($result -eq $null){
    echo "FAIL"
}else{
    echo $result
    echo $result > myip.txt
}
