galleryName=labtainersGallery
resourceGroup=labtainersGalleryResources
imageDefinition=labtainersImageDefinition
az sig image-definition create \
   --resource-group $resourceGroup \
   --gallery-name $galleryName \
   --gallery-image-definition $imageDefinition \
   --publisher labtainers \
   --offer myOffer \
   --sku labtainersImage \
   --os-type Linux \
   --os-state generalized
