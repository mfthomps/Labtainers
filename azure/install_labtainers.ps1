$azdir = "$HOME\labtainers_azure"
if(-Not test-path $azdir){
   mkdir -p "$azdir"
}
cd "$azdir"
wget  https://github.com/mfthomps/Labtainers/releases/latest/download/azure.tar -OutFile $env:TEMP\azure.tar
tar -xf $env:TEMP\azure.tar
echo ""
echo "Labtainers for Azure scripts installed in $azdir"
echo "cd to that directory and run ./create_vm.ps1, passsing in a user name, e.g., "
echo "  ./create_vm.ps1 myname"
echo ""

