$result=az group list | findstr labtainerResources 
If ($result -eq $null){
   az group create -l westus3 -n labtainerResources --output none 
}else{
   echo "Labtainer resource group exists."
}
