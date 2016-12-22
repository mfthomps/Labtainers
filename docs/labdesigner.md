Docker Lab Designer User Guide
==============================

This manual is intended for use by lab designers intending
to create or adapt labs to use the Docker Lab framework.
The framework is intended for use with labs designed for Linux
environments, and it is built around standard Linux Docker containers.

Deploying cyber security labs using this framework
provides three primary benefits:

1) The lab execution environment is controlled and consistent
across all student's computers regardless of the Linux distribution,
version, and configuration.  This allows each lab designer to control
which software packages are present, the versions of libraries and
configuration settings, e.g., /etc values, and these may vary between
labs.

2) Assessment of student lab activity can be automated through a
set of configuration files that identify expected results, thus
relieving lab instructors from having to individually review detailed lab
results.

3) Labs may be automatically "parameterized" for each student such that
students cannot easily copy results from another student or from internet
repositories.  

The use of containers provides the benefits of a consistent
execution environment without requiring
an individual VM per lab, and without requiring all labs to be adapted for
a common Linux execution environment.   These benefits can be realized 
whether or not labs are configured for automatic assessment, 
or are parameterized for each student.

Defining New Labs
-----------------
Labs that have been created for the framework each have their own
directory under the "labs" directory in the subversion repository.
The first step in creating a new lab within the framework is to create
a directory for the lab and then run the "new_lab_setup.sh" script.
This will create a set of template files that will then be customized
for the new lab.  These template files are referenced in the discussion
below.


Defining the lab execution environment
--------------------------------------
A given lab typically requires some set of software packages, and some
system configuration, e.g., network settings.  Identifying an expected
environment is not unique to this framework, rather, it is typically part of any
lab design.  The framework captures most configuration details within a standard
Dockerfile.  Templates for two Dockerfiles are placed in the "dockerfiles" 
directory, one for student containers and one for instructor containers.
These use standard Docker file syntax, which is not repeated here.  Lab designers
should reference Docker documentation for the syntax and semantics of these files.
Simple labs should be able to use the default Dockerfiles created by the 
new_lab_setup.sh script.


Files that are to reside in the student's $HOME directory are placed in a 
