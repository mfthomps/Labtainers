Create a Labtainers VM within Azure, assuming the user 
has an Azure account, e.g., https://azure.microsoft.com/en-us/free/students/

** Only for Mac and Linux systems.  Working with Windows computers and command **
** lines is too painful for the moment.                                        **

This requires that the Azure CLI be installed, e.g., Mac or Linux:
    https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

Then open a terminal on Mac/Linux
Install the local scripts by getting this script (make it executable on Mac or Linux):
    https://raw.githubusercontent.com/mfthomps/Labtainers/master/azure/install_latainers.sh

On Mac or Linux:
    curl -L https://raw.githubusercontent.com/mfthomps/Labtainers/master/azure/install_latainers.sh --output install_labtainers.sh
    chmod a+x install_labtainers.sh  (only on Linux or Mac)


And then run it.   
    ./install_labtainers.sh

That will create a ~/labtainers_azure directory.  

CD to the ~/labtainers_azure directory 
    cd ~/labtainers_azure

Log into your Azure account:
    az login
NOTE:  If your account has access to more than one Azure Subscription, you need to change these parameters to 
specify the student subscription before running the install_labtainers script:
    1.  Change the  ~/.azure/clouds.config to show your student subscription number
    2. Change the entries in ~/.azureProfile.json so that only your student subscription shows 
       “isDefault”= true, the rest being set to ‘false’.

Once logged into Azure, run the create_vm.sh script, passing in a user ID.
The ID can be any name, e.g.,
    ./create_vm.sh myname

The create_vm.sh script may take a while to run.  The process is complete when you see “Labtainers is up.  
Point a local browser to localhost:6901” and perform the labs.
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

When done with a lab, use
   ./deallocate_vm <user ID> 
to stop incurring most charges.  Note however that any work you've performed on the Labtainers 
might be lost (unless you've retrieved your results with get_results.sh.

To restore a VM after you deallocated it, use:
    ./restore_vm.sh <user ID>

When completely done with the VM, use the delete_vm.sh script to stop incurring all charges:
    ./delete_vm.sh <user ID>

Shutting down the VM without deleting it will not stop charges.

Questions?   mfthomps at nps.edu

