Running Labtainers in the Google Cloud Platform

These instructions assume you have a google cloud account.
    https://cloud.google.com/

This requires that the Google Cloud SDK be installed on  the Mac, Windows or Linux:
    https://cloud.google.com/sdk/docs/quickstart

Add the google-cloud-sdk/bin directory to your PATH environment variable.  For example,
if you put the SDK in your home directory, then add this to your 
$HOME/.bash_profile
   PATH=$PATH:$HOME/google-cloud-sdk/bin
and then ru
   source $HOME/.bash_profile
On Windows, just reopen a new PowerShell window after installing the SDK.


Then open a terminal on Mac/Linux, or a PowerShell window on Windows.

Install the local scripts by getting this script (make it executable on Mac or Linux):
    https://raw.githubusercontent.com/mfthomps/Labtainers/master/google/install_labtainers.sh
Or on Windows:
    https://raw.githubusercontent.com/mfthomps/Labtainers/master/google/install_labtainers.ps1

On Mac or Linux:
    curl -L https://raw.githubusercontent.com/mfthomps/Labtainers/master/google/install_labtainers.sh --output install_labtainers.sh
    chmod a+x install_labtainers.sh  (only on Linux or Mac)
On Windows:
    wget https://raw.githubusercontent.com/mfthomps/Labtainers/master/google/install_labtainers.sh -OutFile install_labtainers.ps1

And then run it (Mac/Linux).   
    ./install_labtainers.sh
Windows:
    ./install_labtainers.ps1

That will create a ~/labtainers_google directory.  

Change to the ~/labtainers_google directory 
    cd ~/labtainers_google

Log into your Google Cloud account:
    gcloud auth login

Create a "labtainers" project, your google cloud account:
    ./project.sh

Set your default zone and region (e.g., by editing the set_defaults.sh script) and then use
   gcloud init 
to initialize your client.

In the following command examples, use "ps1" instead of "sh" when using PowerShell.

Once logged into the Google Cloud, run the create_vm.sh (or create_vm.ps1 for windows) script, passing in a user ID.
The ID can be any name without special characters, e.g.,
    ./create_vm.sh myname

One Linux/Mac, you will be prompted for an ssh passphase, leave it blank.  On Windows, ignore the warnings
about ssh keys.

The create_vm script may take a while to run.  The process is complete when you see “Labtainers is up.  
Point a local browser to http://localhost:6901” and perform the labs.
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
   ./stop_vm.sh <user ID> 
to stop incurring processing charges.  Note you may still incur storage charges until the VM is delete.

To restore a VM after you stopped it, use:
    ./start_vm.sh <user ID>

When completely done with the VM, use the delete_vm.sh script to stop incurring all charges:
    ./delete_vm.sh <user ID>

Shutting down the VM without deleting it will not stop all charges, but will stop processing charges.
See the Google Cloud dashboard and pricing for more information.

Questions?   mfthomps at nps.edu
