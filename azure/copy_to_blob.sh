#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "copy_to_blob.sh <user ID>"
    exit
fi
user=$1
#
#  Assumes AZURE account env variables set using account_env.sh
#
#Provide the name of your resource group where managed disk is created
resourceGroupName=labtainerResources

#Provide the managed disk name 
# source name from snapshot
#diskName=base-labtainervm_OsDisk_1_462b1f978221433e86c2e82b98d1a076
diskName=$(./get_disk_id.sh $user)

#Provide Shared Access Signature (SAS) expiry duration in seconds e.g. 3600.
#Know more about SAS here: https://docs.microsoft.com/en-us/azure/storage/storage-dotnet-shared-access-signature-part-1
sasExpiryDuration=3600

#Provide storage account name where you want to copy the underlying VHD file of the managed disk. 
storageAccountName=labtainersblob

#Name of the storage container where the downloaded VHD will be stored
storageContainerName=labtainersblobcontainer


#Provide the name of the destination VHD file to which the VHD of the managed disk will be copied.
destinationVHDFileName=labtainersbase.vhd

#Generate the SAS for the managed disk 
sas=$(az disk grant-access --resource-group $resourceGroupName --name $diskName --duration-in-seconds $sasExpiryDuration --query [accessSas] -o tsv)

#Copy the VHD of the managed disk to the storage account
az storage blob copy start --destination-blob $destinationVHDFileName --destination-container $storageContainerName --source-uri $sas

# check copy status
az storage blob show -n $destinationVHDFileName -c $storageContainerName 
