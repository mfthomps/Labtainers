If ($args.Count -ne 1){
    echo "delete_disk.ps1 <user ID>"
    exit
}
$ErrorActionPreference = "Stop"
$user_id=$args[0]
$disk=$user_id+"-labtainervm-disk"
az disk delete --yes -g labtainerResources -n $disk 
