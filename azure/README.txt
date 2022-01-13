Create a Labtainers VM within Azure, assuming the user 
has an Azure account, e.g., https://azure.microsoft.com/en-us/free/students/

Simply run the create_vm.sh script, passing in a user ID.
The ID can be any name.

After the script finishes (it will take several minutes), point a browser
to http://localhost:6901 and perform the labs.

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

When completely done with the VM, use the delete_all.sh script to stop
incurring charges.   Shutting down the VM without deleting it will not stop charges.

Questions?   mfthomps at nps.edu
