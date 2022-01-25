if [ "$#" -ne 1 ]; then
    echo "create_vm.sh <user ID>"
    exit
fi
user_id=$1
vm_name=$user_id-labtainervm
if [ ! -f ~/.ssh/id_labtainers ]; then
    ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_labtainers -q -N ""
fi
az vm user update -u labtainer --ssh-key-value "$(< ~/.ssh/id_labtainers.pub)" -n $vm_name -g labtainerResources --output none
