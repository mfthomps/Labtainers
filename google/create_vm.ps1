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
$zone=./findzone.ps1
gcloud compute instances create $vm_name --image=https://www.googleapis.com/compute/v1/projects/labtainers/global/images/labtainervm5 `
   --metadata-from-file=user-data=user_config.txt
gcloud compute disks resize $vm_name --size 30G --zone=$zone -q
# instances fail ssh until settled
#
./waitup.ps1 $user_id 2>$null
echo "Check keys"
gcloud compute ssh labtainer@$vm_name --command="echo VM booted"  --strict-host-key-checking=no  
#gcloud compute ssh labtainer@$vm_name --dry-run
echo "Back from ssh"
cp $HOME/.ssh/google_compute_engine $HOME/.ssh/id_labtainers
cp $HOME/.ssh/google_compute_engine.pub $HOME/.ssh/id_labtainers.pub
./waitdone.ps1 $user_id
