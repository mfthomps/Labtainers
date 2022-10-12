# Create a base labtainer image.
# First:
#    delete_vm.sh base
#    base_create.sh base
#
# Then use 
#    gcloud compute instances describe base-labtainervm | grep disks
# to find the disk name, it is a url.
#
# Then 
#     (NO, cycle through images!)    gcloud compute images delete labtainervm2
#    gcloud compute images create labtainervm2 --source-disk=https://www.googleapis.com/compute/v1/projects/labtainers/zones/us-west1-a/disks/base-labtainervm
#
# Only then run this script
#
#
gcloud compute images add-iam-policy-binding labtainervm4 \
    --member='allAuthenticatedUsers' \
    --role='roles/compute.imageUser'
