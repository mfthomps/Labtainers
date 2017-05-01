
Questions and to-do
===================

Test Docker installation on fedora as a host, and use of student scripts in that environment.
Docker installation instructions, bullet proof.

Does the instructor need to create a container environment per-student?  If the instructor container
simply has a directory per student, won't that break some hardcoded paths, e.g., in programs written
by the student?

Strategy for fetching images from either a repository, or from distribution-specific base images.
Repo name in the host /etc/hosts file?  If missing, go to base and build from there.
Student should only have to run "start <lab>", and the image is fetched or built as needed.


Package the labtainers lab creation as a container (likely not possible).

What if student changes the name of the program, e.g., from vuln to my_vuln?
A general way to name programs in the results.config?

Record "grades" in a json file.
Alter start of instructor to allow full automation (no need to start container just to type "Instructor.py"

Automate testing.  suite of results files that should all grade a specific way?

Manage instructor containers so not running multiple labs at once, net conflicts?

Artifact gathering mostly assumes user is "ubuntu".  need to generalize that.  Same with instructor
scripts -- do not rely on user ubuntu outside of a dockerfile.

moreterm, pause etc redundant between student and instructor.  fix that

handle nohup when collecting artifacts

Remove instructor scripts from non-grader machines, less time confused about where I am when debugging.

Validate boolean strings against entire goals.json, by the time of the evaluation, cannot tell if
tokens are defined or not.

Shorter form for a goal that is a boolean.

Error check on redo so that if a image build fails, the container is not started -- delete the container first?

Extract timestamps from descrete log files.

timestamp on checklocal file might differ from that of the prog.stdout file?
