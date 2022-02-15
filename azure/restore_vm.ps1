If ($args.Count -ne 1){
    echo "restore_vm.ps1 <user ID>"
    exit
}
$user=$args[0]
$vm=$user+"-labtainervm"
az vm start  -g labtainerResources -n $vm
Start-Sleep -s 2
./waitdone.ps1 $user_id
