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
directory under the "labs" directory in the project repository.
The first step in creating a new lab within the framework is to create
a directory for the lab and then run the "new_lab_setup.sh" script.
This will create a set of template files that you can then customize
for the new lab.  These template files are referenced in the discussion
below.

After creating the new lab directory, cd to that directory and then run

    $SEED_DIR/scripts/designer/bin/new_lab_setup.sh

where SEED_DIR is set to the top of the svn repo, e.g.,

    export SEED_DIR=/home/mike/svn/seed/trunk


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

### Lab-specific files in the student's home directory ###
Files that are to reside in the student's $HOME directory are placed in the 
new lab directory.  For example, if a lab includes a source code file, that
should be created in the lab directory, and it will appear in the student's
home directory within the container when the container starts.  

### Final lab environment fixup ###
The initial environment encountered by the student is further refined using
the optional bin/fixlocal.sh script.  The framework executes
this script the first time a student starts the lab container.  For example,
this could be used to compile lab-specific programs afer they have been parameterized,
(as described below).  Or this script could be perform final configuration adjustments
that cannot be easily performed by the Dockerfile.

Parameterizing a lab
--------------------
This section describes how to individualize the lab for each student to discourage
sharing of lab solutions.  This is achieved by defining symbols within source 
code or/and data.  The framework will replace these symbols with randomized values
specific to each student.  The config/parameter.config file identifies the files, and
the symbols within those files that are to be modified.  A simple example can be found in 

    labs/formatstring/config/parameter.config

That configuration file causes the string "SECRET2_VALUE" within the file:

     /home/ubuntu/vul_prog.c

to be replaced with a hexidecimal representation of a random value
between 0x41 and 0x5a, inclusive.

This symbolic replacement occurs when the student first starts the lab container,
but before the execution of the bin/fixlocal.sh script.  Thus, in the formatstring
lab, the executable program resulting from the fixlocal.sh script will be specific
to each student (though not necessarily unique).

The following operations can be defined within the config/parameter.config file:


     RAND_REPLACE : <filename> : <symbol> : <LowerBound> : <UpperBound>
       Replace a symbol within the named file with a random value within a given
       range.  The random value generator is initialized with the lab instance
       seed.

         where: <filename> - the file name (file must exist) where <symbol> is to be replaced
               <symbol> - the string to be replaced
               <LowerBound> and <UpperBound> specifies the lower and upper bound
                                           to be used by random generator
       example:

         RAND_REPLACE: /home/ubuntu/stack.c : BUFFER_SIZE : 200 : 2000
         will randomly replace the token string "BUFFER_SIZE" found in
         file stack.c with a number ranging from 200 to 2000
 
     HASH_CREATE : <filename> : <string>
       Create or overwrite a file with a hash of a given string and the lab instance seed.
         where: <filename> - the file name (file will be created if it does not exist)
                <string> -   the input to a MD5 hash operation (after concatenation 
                             with the lab instance seed)
                           
                       
       example:
         HASH_CREATE : /home/ubuntu/myseed : bufferoverflowinstance
         A file named /home/ubuntu/myseed will be created (if it does not exist), 
         containing an MD5 hash of the lab instance seed concatentated with the 
         string 'bufferoverflowinstance'.
 
     HASH_REPLACE : <filename> : <symbol> : <string>
       Replace a symbol in a named file with a MD5 hash of a given string concatenated with the
       lab instance seed.
         where: <filename> - the filename (file must exist) containing the symbol to be replaced.
                <symbol> - a string that will be replaced by the hash
                <string> - a string contatenated with the lab instance seed and hashed

         example:
           HASH_REPLACE : /root/.secret : ROOT_SECRET : mysupersecretrootfile
           The string "ROOT_SECRET" in file /root/.secret will be replaced with an MD5 hash
           of the concatenation of the lab instance seed and "mysupersecretrootfile".

Identify Lab-specifc Artifacts
------------------------------

