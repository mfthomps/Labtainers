$gdir = "$HOME\labtainers_google"
if(-Not (test-path $gdir)){
   mkdir -p "$gdir"
}
cd "$gdir"
wget  https://github.com/mfthomps/Labtainers/releases/latest/download/google.tar -OutFile $env:TEMP\google.tar
tar -xf $env:TEMP\google.tar
echo ""
echo "Labtainers for Google scripts installed in $gdir"
echo "cd to that directory and run ./create_vm.ps1, passsing in a user name, e.g., "
echo "  ./create_vm.ps1 myname"
echo ""

