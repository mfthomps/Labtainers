Docker Labs Components and Relationships
========================================

This document is intended to provide an overview of the 
origins of, and relationships between, components of the
parameterized labs.  This is supplemental to the 
Docker Labs Development Guide, and is intended for 
those working with the Docker Lab development tools and
software.

Students and Instructors
------------------------
Each lab requires two sets of components, one for
students and one for instructors, and these are
partitioned into two development directories: 

 * MyStudentDocker -- all configuration files and scripts to manage student containers.
 * MyInstructorDocker -- same, but for instructor containers.

The next several sections of this document describe images and containers for 
students.  Management of images and containers for instructors is similar and is
not repeated, though differences are noted.

TBD: Transistion all lab-specific files to a single lab directory, which itself may be
partitioned as needed.  Or, at least move image-related config files and scripts all
to the instructor side?

Docker Images
-------------
Parameterized labs use Docker Containers.  
The containers are built with images defined by
the Dockerfile.<labname>.student file, which 
identifies the specific software packages and configuration
of the container image.  The images are created
using the student.build.sh, which builds images
for all of the student labs.  All images are derived from ubuntu xenial.

Currently, to simplify the development environment, 
images must be built on each host that is to 
run containers.  The future intent is to manage a repository
of images that students & developers would draw from.
Another future plan is to create a baseline image that includes
a common set of packages, and then use that for the lab-specific
images.  It is expected that some labs will simply use the baseline image.

When testing lab development tools and labs, it may be necessary to update the docker
image, e.g., to ensure the proper packages and setup scripts are part of
the lab. Use the student.build.sh script for this, it will recreate the image.

Docker Containers
-----------------
The container for each lab is built for the student when they
first run the "start.sh" script, naming the lab.  Once built, a container
can be stopped, started and paused. 

Parameterization of labs, (e.g., modifying configuration data or source code to reflect
values specific to the student), is controlled by a "parameter.config" configuration file in each lab's
config directory.  The processing is performed by "parameterize.sh" in MyStudentDocker/bin,
which is executed by the Docker exec command that launches a container from the start.sh script.
Each lab has a unique master seed that is combined with the student's email address to create
an instance-specific seed that is then used as the source of randomness to parameterize the lab.
This same seed is available on the instructor side for use in functions that assess the correctness
of student lab results.

When a container first starts, the parameterization occurs.  Subsequently, if a "fixlocal.sh" script
exists in the <labname>/bin directory, it is executed.  These scripts are intended to compile source code
or invoke tools whose configuration data was parameterized.

While a student interacts with the container, stdin and stdout from selected commands are captured 
within timestamped files in the .local/results directory.  This is managed by the capinout.sh and
bash-prexec.sh and bash-precapinout.sh scripts in the bin directory. 

When a container is stopped, e.g., via the stop.sh script, all student files, including the stdin/stout 
files noted above, are packaged into a zip file that is copied to a host OS directory per the start.config
file.  We expect these files will be transferred to a specific directory on the instructor's host 
computer for consumption by the instructor containers.  For ease of development, these are the
same directories relative to $HOME.

For testing purposes, it may be useful to delete and rebuild containers.

Grading
-------
The results transferred from a student container are compared to expected results using rules
captured in the goals.config file.  This comparison employs symbolic names defined within the results.config
file for the lab.  

A notional example of student lab grading is performed by the Grader.sh


