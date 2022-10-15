Create a Labtainers VM within Azure, assuming the user 
has an Azure account. Note that Azure Student accounts
(https://azure.microsoft.com/en-us/free/students/) are not
recommended for use at this time because they are subject to
unpredictable resource limitations.


This requires that the Azure CLI be installed on  the Mac, Windows or Linux:
    https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

Then open a terminal on Mac/Linux, or a PowerShell window on Windows.
Install the local scripts by getting this script (make it executable on Mac or Linux):
    https://raw.githubusercontent.com/mfthomps/Labtainers/master/azure/install_labtainers.sh
Or on Windows:
    https://raw.githubusercontent.com/mfthomps/Labtainers/master/azure/install_labtainers.ps1

On Mac or Linux:
    curl -L https://raw.githubusercontent.com/mfthomps/Labtainers/master/azure/install_labtainers.sh --output install_labtainers.sh
    chmod a+x install_labtainers.sh  (only on Linux or Mac)
On Windows:
    wget https://raw.githubusercontent.com/mfthomps/Labtainers/master/azure/install_labtainers.sh -OutFile install_labtainers.ps1

And then run it (Mac/Linux).   
    ./install_labtainers.sh
Windows:
    ./install_labtainers.ps1

That will create a ~/labtainers_azure directory.  

Change to the ~/labtainers_azure directory 
    cd ~/labtainers_azure

Log into your Azure account:
    az login
NOTE:  If your account has access to more than one Azure Subscription, you need to change these parameters to 
specify the student subscription before running the install_labtainers script:
    1.  Change the  ~/.azure/clouds.config to show your student subscription number
    2. Change the entries in ~/.azureProfile.json so that only your student subscription shows 
       “isDefault”= true, the rest being set to ‘false’.

In the following command examples, use "ps1" instead of "sh" when using PowerShell.

Once logged into Azure, run the create_vm.sh (or create_vm.ps1 for windows) script, passing in a user ID.
The ID can be any name, e.g.,
    ./create_vm.sh myname

The create_vm script may take a while to run.  The process is complete when you see “Labtainers is up.  
Point a local browser to localhost:6901” and perform the labs.
When prompted for a password in the browser, just click submit or OK, i.e., leave the password blank.
The password for the labtainer user in the VM is labtainer.  

When done with labs, run the get_results.sh (or get_results.ps1) script: 
    ./get_results.sh <user ID>
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
might be lost (unless you've retrieved your results with get_results.sh), depending on how
long the VM is dormant.

To restore a VM after you deallocated it, use:
    ./restore_vm.sh <user ID>

When completely done with the VM, use the delete_vm.sh script to stop incurring all charges:
    ./delete_vm.sh <user ID>

Shutting down the VM without deallocating or deleting it will not stop charges.

Questions?   mfthomps at nps.edu

