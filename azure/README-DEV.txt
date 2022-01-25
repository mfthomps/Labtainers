README for creating Azure Labtainer VHD image and storing in Azure blob storage for use by Labtainers VMs

Use the base_create_vm.sh script to create a base VM, provide the user name "base"

Use generalize.sh to generalize and stop the VM

Delete the existing blob if it exists with delete_blob.sh
Copy the base disk image to the blob using copy_to_blob.sh (after sourcing account_env.sh)
Remove the vm using delete_vm.sh



