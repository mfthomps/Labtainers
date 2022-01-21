If ($args.Count -ne 1){
    echo "get_results.ps1 <user ID>"
    exit
}
$user=$args[0]
$vm=$user+"-labtainervm"
echo "Retrieving Labtainer results from $vm"
if (-not(test-path $HOME/labtainer_xfer)){
    mkdir -p $HOME/labtainer_xfer
}
$ip=./getip.ps1 labtainerResources $vm
if ($ip -eq "FAIL" ){
    echo "Failed to get ip of $vm"
    exit 1
}
echo "ip is $ip"
scp -i "$HOME/.ssh/id_labtainers" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -r labtainer@"$ip":/home/labtainer/headless-labtainers/labtainer_xfer/* $HOME/labtainer_xfer/
echo "Results stored in $HOME/labtainer_xfer"
