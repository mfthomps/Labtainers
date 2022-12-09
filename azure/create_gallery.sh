location=westus
galleryName=labtainersGallery
resourceGroup=labtainersGalleryResources
publisherUri=https://github.com/mfthomps/Labtainers
publisherEmail=mfthomps@nps.edu
prefix=LabtainersImages
eulaLink=https://github.com/mfthomps/Labtainers

az group create --name $resourceGroup --location $location

az sig create \
   --gallery-name $galleryName \
   --permissions community \
   --resource-group $resourceGroup \
   --publisher-uri $publisherUri \
   --publisher-email $publisherEmail \
   --eula $eulaLink \
   --public-name-prefix $prefix
