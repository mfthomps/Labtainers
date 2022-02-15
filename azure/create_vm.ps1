#
# Create an Azure VM for a student, assuming the user has
# an Azure account and the CLI installed.
#
# This will create an ssh key pair and use it when creating the VM
#
If ($args.Count -ne 1){
    echo "checktunnel.sh <user ID>"
    exit
}
$ErrorActionPreference = "Stop"
$user_id=$args[0]
$vm_name=$user_id+"-labtainervm"
Remove-Item $HOME/.ssh/id_labtainers*
ssh-keygen -b 2048 -t rsa -f $HOME/.ssh/id_labtainers -q -N '""'
echo "key generated"
copy cloud_init.template cloud_init.txt
./resourcecheck.ps1
echo "Creating Azure VM $vm_name for $user_id"
az vm create `
 --public-ip-sku Standard `
 --resource-group labtainerResources `
 --name $vm_name `
 --image UbuntuLTS `
 --admin-username labtainer `
 --nic-delete-option delete `
 --generate-ssh-keys `
 --ssh-key-values ~/.ssh/id_labtainers.pub `
 --custom-data cloud_init.txt > $user_id.json

./waitdone.ps1 $user_id

