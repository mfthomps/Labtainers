if [ "$#" -ne 1 ]; then
    echo "create_vm.sh <user ID>"
    exit
fi
user_id=$1
vm_name=$user_id-labtainervm
az vm user update -u labtainer --ssh-key-value "$(< ~/.ssh/id_labtainers.pub)" -n $vm_name -g labtainerResources
