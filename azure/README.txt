Create a Labtainers VM within Azure, assuming the user 
has an Azure account, e.g., https://azure.microsoft.com/en-us/free/students/

Simply run the create_vm.sh script, passing in a user ID.
After that script finishes (it will take several minutes), point a browser
to http://localhost:6901

When completely done with the VM, use the delete_all.sh script to stop
incurring charges.   Shutting down the VM without deleting it will not stop charges.

This script will create an SSH key pair named id_labtainers within your ~/.ssh directory.

