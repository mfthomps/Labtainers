If ($args.Count -ne 1){
    echo "create_disk.ps1 <Disk name>"
    exit
}
$disk=$args[0]
az disk create -g labtainerResources -n $disk --source https://labtainersblob.blob.core.windows.net/labtainersblobcontainer/labtainersbase.vhd --output none
