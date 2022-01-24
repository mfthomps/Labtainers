If ($args.Count -ne 1){
    echo "delete_vm.ps1 <user ID>"
    exit
}
$user=$args[0]
$vm=$user+"-labtainervm"
az vm delete --yes -g labtainerResources -n $vm
./delete_disk.sh $user
echo "VM $vm has been deleted"
