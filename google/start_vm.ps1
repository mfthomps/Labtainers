If ($args.Count -ne 1){
    echo "start_vm.ps1 <user ID>"
    exit
}
$user=$args[0]
$vm=$user+"-labtainervm"
gcloud -q compute instances start $vm_name 
./checktunnel.ps1 $user_id
