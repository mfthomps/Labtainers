
storageAccountName=labtainersblob

#Name of the storage container where the downloaded VHD will be stored
storageContainerName=labtainersblobcontainer
destinationVHDFileName=labtainersbase.vhd
az storage blob delete -c $storageContainerName -n $destinationVHDFileName 
