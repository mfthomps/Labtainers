galleryName=labtainersGallery
resourceGroup=labtainersGalleryResources
imageDefinition=labtainersImageDefinition
az sig image-version create \
   --resource-group $resourceGroup \
   --gallery-name $galleryName \
   --gallery-image-definition $imageDefinition \
   --gallery-image-version 1.0.0 \
   --virtual-machine "/subscriptions/4747feb2-6851-42cd-9ccf-e07f7fcb6560/resourceGroups/LABTAINERRESOURCES/providers/Microsoft.Compute/virtualMachines/base-labtainervm"
