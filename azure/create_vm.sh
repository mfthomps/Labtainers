if [ "$#" -ne 1 ]; then
    echo "create_vm.sh <user ID>"
    exit
fi
user_id=$1
vm_name=$user_id-labtainervm
disk=$user_id-labtainervm-disk
./create_disk.sh $disk || exit 1
az vm create \
    --resource-group labtainerResources \
    --name $vm_name \
    --os-type linux \
    --attach-os-disk $disk \
    --output none
./update_user.sh $user_id || exit 1
./get_headless.sh $user_id || exit 1
./waitweb.sh $user_id
