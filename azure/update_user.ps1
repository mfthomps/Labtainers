If ($args.Count -ne 1){
    echo "update_user.ps1 <user ID>"
    exit
}
$ErrorActionPreference = "Stop"
$user_id=$args[0]
$vm_name=$user_id+"-labtainervm"
if (-Not test-path $HOME/.ssh/id_labtainers){
    ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_labtainers -q -N ""
}
$key = Get-Content $HOME/.ssh/id_labtainers.pub -Raw
az vm user update -u labtainer --ssh-key-value "$key" -n $vm_name -g labtainerResources --output none
