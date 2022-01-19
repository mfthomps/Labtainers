If ($args.Count -ne 1){
    echo "restore_vm.ps1 <user ID>"
    exit
}
$user=$args[0]
$vm=$user+"-labtainervm"
az vm start  -g labtainerResources -n $vm
./checktunnel.ps1 $user
echo "VM $vm has been started."
echo "Labtainers is up.  Point browser to localhost:6901"
