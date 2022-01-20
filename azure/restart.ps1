If ($args.Count -ne 1){
    echo "delete_vm.ps1 <user ID>"
    exit
}
$ErrorActionPreference = "Stop"
$user=$args[0]
./checktunnel.sh $user
echo "Point your browser to http://localhost:6901"
