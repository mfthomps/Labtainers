#
# Create an Azure VM for a student, assuming the user has
# an Azure account and the CLI installed.
#
# This will create an ssh key pair and use it when creating the VM
#
If ($args.Count -ne 1){
    echo "create_vm.ps <user ID>"
    exit
}
$ErrorActionPreference = "Stop"
$user_id=$args[0]
$vm_name=$user_id+"-labtainervm"
gcloud compute instances create $vm_name --image=https://www.googleapis.com/compute/v1/projects/labtainers/global/images/labtainervm `
   --metadata-from-file=user-data=user_config.txt
# instances fail ssh until settled
./waitup.ps1 $user_id 2>/dev/null
echo "Check keys"
gcloud compute ssh labtainer@$vm_name --command="echo VM booted"
cp $HOME/.ssh/google_compute_engine $HOME/.ssh/id_labtainers
cp $HOME/.ssh/google_compute_engine.pub $HOME/.ssh/id_labtainers.pub
./waitdone.sh $user_id
