If ($args.Count -ne 1){
    echo "update_user.ps1 <user ID>"
    exit
}
$ErrorActionPreference = "Stop"
$user_id=$args[0]
$vm_name=$user_id+"-labtainervm"
if (-not(test-path $HOME/.ssh/id_labtainers)){
    ssh-keygen -b 2048 -t rsa -f $HOME/.ssh/id_labtainers -q -N '""'
}
$key = Get-Content $HOME/.ssh/id_labtainers.pub -Raw
echo "key is $key"
az vm user update -u labtainer -n $vm_name -g labtainerResources --output none --ssh-key-value "$key"
