If ($args.Count -ne 1){
    echo "deallocate_vm.ps1 <user ID>"
    exit
}
$user=$args[0]
$vm=$user+"-labtainervm"
az vm deallocate -g labtainerResources -n $vm
echo "VM $vm has been deallocated"
