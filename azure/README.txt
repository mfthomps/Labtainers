Create a Labtainers VM within Azure, assuming the user 
has an Azure account, e.g., https://azure.microsoft.com/en-us/free/students/

This requires that the Azure CLI be installed, e.g., on Windows, Mac or Linux:
    https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

Then open a terminal on Mac/Linux, or a Windows Powershell.
Install the local scripts by getting this script (make it executable on Mac or Linux):
    https://raw.githubusercontent.com/mfthomps/Labtainers/master/azure/install_latainers.sh
e.g., on Mac or Linux:
    curl -L https://raw.githubusercontent.com/mfthomps/Labtainers/master/azure/install_latainers.sh --output install_labtainers.sh
    chmod a+x install_labtainers.sh  (only on Linux or Mac)

On Windows Powershell:
    wget https://raw.githubusercontent.com/mfthomps/Labtainers/master/azure/install_latainers.sh -O install_labtainers.sh

And then run it.   
    ./install_labtainers.sh

That will create a ~/labtainers_azure directory.  

CD to the ~/labtainers_azure directory and run the create_vm.sh script, passing in a user ID.
The ID can be any name, e.g.,
    cd ~/labtainers_azure
    ./create_vm.sh myname

After the script finishes (it will take several minutes), point a browser
to http://localhost:6901 and perform the labs.
When prompted for a password in the browser, just click submit or OK, i.e., leave the password blank.

When done with labs, run the get_results.sh script: 
    ./get_results <user ID>
This will store your Labtainer results in ~/labtainer_xfer.  Provide those
results to your instructor.

If you become unable to reach the Labtainers via your browser, e.g., after 
shutting down your computer, simple use the restart.sh script:
    ./restart.sh <user ID>

The create_vm.sh script will create an SSH key pair named id_labtainers within your ~/.ssh directory.
The private key in id_labtainers is not passphrase protected, so you must protect it.
You may move the keys to a different computer and access your Labtainers from that computer's
browser.  You must first run the install_labtainers.sh script on that computer, and then run
the restart.sh script.

When completely done with the VM, use the delete_vm.sh script to stop incurring charges:
    ./delete_vm.sh <user ID>
Shutting down the VM without deleting it will not stop charges.

Questions?   mfthomps at nps.edu
