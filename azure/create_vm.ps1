#
# Create an Azure VM for a student, assuming the user has
# an Azure account and the CLI installed.
#
# This will create an ssh key pair named ~/.ssh/id_labtainers and use it when creating the VM
#
If ($args.Count -ne 1){
    echo "create_vm.ps1 <user ID>"
    exit
}
$ErrorActionPreference = "Stop"
$user_id=$args[0]
$vm_name=$user_id+"-labtainervm"
$disk=$user_id+"-labtainervm-disk"
./create_disk.ps1 $disk 
az vm create `
    --resource-group labtainerResources `
    --name $vm_name `
    --os-type linux `
    --attach-os-disk $disk `
    --output none
./update_user.ps1 $user_id
./get_headless.ps1 $user_id
./waitweb.ps1 $user_id
