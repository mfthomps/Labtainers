
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
