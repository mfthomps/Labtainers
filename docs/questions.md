
Questions and to-do
===================


Does the instructor need to create a container environment per-student?  If the instructor container
simply has a directory per student, won't that break some hardcoded paths, e.g., in programs written
by the student?

Package the labtainers lab creation as a container (likely not possible).

What if student changes the name of the program, e.g., from vuln to my_vuln?
A general way to name programs in the results.config? (We now allow wildcards)


Manage instructor containers so not running multiple labs at once, net conflicts?

handle nohup when collecting artifacts

Remove instructor scripts from non-grader machines, less time confused about where I am when debugging.

Validate boolean strings against entire goals.json, by the time of the evaluation, cannot tell if
tokens are defined or not.

Shorter form for a goal that is a boolean.

Extract timestamps from descrete log files.

timestamp on checklocal file might differ from that of the prog.stdout file?

validate count_greater fields (and double-check boolean validation)

Tools for visualizing the network topology, automaticly based on start.conf file?

Tools/api for student to change network topology?

error checks for top level scripts to ensure lab exists (friendlier error message than just log entry).



ignorelocal should look at basename, vice path.

system tar files are owned by first USER, regardless of order
remove "firstlevelzip" from json if not meaningful.

create student-only distribution whose goal is being much smaller by not including
files that go into containers, e.g., password cracking & sys files.  Separate problem from
issue of instructor-only notes.

Define a new results.config field_type of "ORIG_CHECKSUM", which resolves to the checksum of
the original file as it existed right after parameterization.    
This will be compared to a md5 computed in a checklocal.sh script?

Add command completion logic to start.py, and perhaps stop.py (which would rely on settings made
from start.py)?


Do not use xfer directory as a workspace for zip-fu!

Add a "checkme" command to the linux host, it will run scripts to assess selcted properites,
e.g., run scans or attacks.

When running parameterize.sh, run it as root, and then drop privilges so the container user need not be root?

Add setting network interfaces to promisc mode from parmeterize.sh, parse startconfig from linux host and 
pass in list of interfaces to be promisc.
