If ($args.Count -ne 1){
    echo "delete_vm.ps1 <user ID>"
    exit
}
$user=$args[0]
$vm=$user+"-labtainervm"
$zone=./findzone.ps1
gcloud -q compute instances delete $vm --zone=$zone
echo "VM $vm has been deleted"
