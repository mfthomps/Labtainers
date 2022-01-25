# First use create_base.sh to create an vm instance named base-labtainervm
#
# The use 
#    gclooud compute instances describe base-labtainervm
# to find the disk name, it is a url.
#
# Then 
#     gcloud compute images delete labtainervm
#    gcloud compute images create labtainervm --source-disk=https://www.googleapis.com/compute/v1/projects/labtainers/zones/us-west1-a/disks/base-labtainervm

#
#
gcloud compute images add-iam-policy-binding labtainervm \
    --member='allAuthenticatedUsers' \
    --role='roles/compute.imageUser'
