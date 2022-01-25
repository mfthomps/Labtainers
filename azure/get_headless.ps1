If ($args.Count -ne 1){
    echo "update_user.ps1 <user ID>"
    exit
}
$ErrorActionPreference = "Stop"
$user_id=$args[0]
$vm_name=$user_id+"-labtainervm"
$ip=./getip.ps1 labtainerResources $vm_name
ssh -i "$HOME/.ssh/id_labtainers" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null labtainer@$ip "mkdir headless_labtainers;cd headless_labtainers;wget -P /home/labtainer/headless-labtainers https://raw.githubusercontent.com/mfthomps/Labtainers/master/headless-lite/headless-labtainers.sh;chmod a+x /home/labtainer/headless-labtainers/headless-labtainers.sh;sudo usermod -aG docker labtainer;sudo systemctl restart headless-labtainers.service;"

