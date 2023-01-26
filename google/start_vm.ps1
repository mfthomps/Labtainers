If ($args.Count -ne 1){
    echo "start_vm.ps1 <user ID>"
    exit
}
$user=$args[0]
$vm=$user+"-labtainervm"
$zone=./findzone.ps1
gcloud -q compute instances start $vm --zone=$zone
./waitup.ps1 $user
./waitdone.ps1 $user
