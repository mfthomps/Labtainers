Labtainer Lab Designer User Guide
=================================

This manual is intended for use by lab designers wanting
to create or adapt cyber security labs to use the Docker lab framework known
as "Labtainers".

Benefits of Labtainers
----------------------
The Labtainer framework is designed for use with computer and network security
laboratory exercises targeting Linux
environments, and it is built around standard Linux Docker containers.

Deploying cyber security labs using this framework
provides three primary benefits:

1) The lab execution environment is controlled and consistent
across all student computers regardless of the Linux distribution
and configuration present on individual student computers.  
This allows each lab designer to control
which software packages are present, the versions of libraries and
specific configuration settings, e.g., /etc file values. These configurations
may vary between labs, and they may vary between multiple containers in
a single lab.

2) Assessment of student lab activity can be automated through a
set of configuration files that identify expected results, thus
relieving lab instructors from having to individually review detailed lab
results.

3) Labs may be automatically "parameterized" for each student such that
students cannot easily copy results from another student or from internet
repositories.  

Labtainers have the advantages of a consistent
execution environment without requiring
an individual Virtual Machine (VM) per lab, and without requiring all labs to be adapted for
a common Linux execution environment.   These benefits can be realized 
whether or not labs are configured for automatic assessment, 
or are parameterized for each student.

Exercises that include multiple networked computers illustrate another advantage 
of using containers over VMs, namely, containers require significantly less resources
than do VMs.  A student laptop that struggles to run two or more VMs can readily 
run multiple containers simultaneously.

Overview of the Student Environment and Workflow
------------------------------------------------
Labtainers support laboratory exercises designed for Linux environments,
ranging from interaction with individual programs to labs that include
what appear to be multiple components and networks.  Students see and interact with Linux
environments, primarily via bash shell commands. In general, the Labtainer 
framework implementation is not visible to the student, and the Linux 
environment as seen by the student is not augmented to support the framework.
The Linux execution environments presented by Docker containers do not readily
include GUIs.  As a result, Labtainer should not be used for exercises requiring
GUIs.

Labtainers are intended for use on individual student computers.  
The computer utilized by a student must include the Linux operating system, e.g.,
as a single VM.  This Linux operating system, referred to herein
as the "host", can be any distribution and version
which supports Dockers, and it must have Dockers installed.  
In addition to installing Dockers on their Linux host, the student must
obtain and expand a tarball, which contains the Labtainer workspace utilities.
(This tarball may someday be replaced by standard Linux distribution packages,
e.g., Debian and/or RPM packages.)  Students initiate any and all labs from a
single workspace directory on the Linux host.

To perform a specific Labtainer exercise, the student runs a *start* command from
the Labtainer workspace, naming the lab exercise.  This results in one or more
containers starting up along with corresponding virtual terminals via which the 
student will interact with the containers.  These virtual terminals typically
present a bash shell.  Each container appears to the student as a separate
computer, and these computers may appear to be connected via one or more networks.  

When a student starts a given exercise for the first time, the framework fetches
Docker images from a centralized repository named in the host system's /etc/hosts
file.  If no such repository exists, the framework will build the Docker images
on the student's host as needed.

After the student performs the lab exercise, artifacts from the container
environments are automatically collected into a zip file that appears on
the student's Linux host.  The student forwards this zip file to the instructor,
e.g., via email or a Learning Management System (LMS).  The instructor collects student zip files into a common
directory on his or her own Linux host, and then issues a command that starts
the instructor container(s) for that lab.  This results in automated assessment of student lab
activity, (if the lab is designed for that), and creation of an environment
in which the instructor can review the work of each student.

Many cyber security lab exercises are assessed through use of reports in which students
describe their activities and answer specific questions posed by the instructor.  Labtainers
are intended to augment, rather than supplant this type of reporting.  The framework does not
prescribe mechanisms for managing such reporting.  If a given lab exercise was not designed
to support automated assessment, then zip files from the students need not be collected.  On
the other hand, instructors may still wish to collect the zip files to manually review selected
student activity, e.g., student-developed programs, output files, or even bash history records.  

Obtaining the Labtainer Development Kit
---------------------------------------
The Labtainer Development Kit (LDK) is available as an subversion repository at
[https://tor.ern.nps.edu/svn/proj/seed](https://tor.ern.nps.edu/svn/proj/seed).

(Our intent is release versions to a Github repository for access beyond NPS.)

Defining New Labs
-----------------
The most challenging and critical part of designing a new cyber security lab
is the design of the lab itself, i.e., identifying learning objectives and
organizing exercises to achieve those objectives.  The Labtainer framework
does not specifically address any of that.  Rather, the framework is intended
to allow you to focus more time on the design of the lab and less time on mitigating and
explaining system administration burdens you are placing on students and instructors.  
The framework does not require lab designers to program or create scripts.  The
lab designer primarily interacts with the framework by editing configuration files,
which the affect the student's execution environment and the optional automated
assessment of student activity.

Labtainer exercises each have their own
directory under the "labs" directory in the project repository.
The first step in creating a new lab within the framework is to create
a directory for the lab and then run the "new\_lab\_setup.sh" script.
This will create a set of template files that you can then customize
for the new lab.  These template files are referenced in the discussion
below.

After creating the new lab directory, cd to that directory and then run

    $SEED_DIR/scripts/designer/bin/new_lab_setup.py

where SEED\_DIR is set to the top of the svn repo, e.g.,

    export SEED_DIR=/home/mike/svn/seed/trunk

## Testing the new lab ##
Once a new lab is created, its container image must be created.  The default container configuration
is simply a bash shell in linux.  Later sections of this manual describe modifications that will
change the container image, but for now you can create a default image as follows:

    cd scripts/MyStudentDocker

Then run:

    ./buildImage.sh [labname]

where labname is the name of your new lab.

To start a student container, use the 

    ./redo.sh [labname] 

command, where labname is the name of the lab you just created.  Students would typically
use the "start.sh" command.  The redo.sh command will remove and recreate the container
each time the script is run.  This is often necessary when building new labs, to ensure the
new envrioment does not contain artifacts from previous runs.

The above script should result in creation of three windows, two of which have
running bash shells, and the third displays instructions.

Defining the lab execution environment
--------------------------------------
A given lab typically requires some set of software packages, and some
system configuration, e.g., network settings.  Identifying an expected
environment is not unique to this framework, rather, it is typically part of any
lab design.  The framework captures most configuration details within a standard
Dockerfile.  Templates for two Dockerfiles are placed in the "dockerfiles" 
directory, one for student containers and one for instructor containers.
These use standard Docker file syntax, which is described at:

    https://docs.docker.com/engine/reference/builder/

Lab designers should reference that Docker documentation for the 
syntax and semantics of these files.
Simple labs should be able to use the default Dockerfile created by the 
new\_lab\_setup.py script.  That Dockerfile includes the minimal set
of Linux packages necessary to host a lab within the framework.  The default
execution environment builds off of a recent Ubuntu image.
[MFT: Note alternate mimimal images as developed, e.g., Fedora.]


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
(as described below).  Or this script could perform final configuration adjustments
that cannot be easily performed by the Dockerfile.

Parameterizing a lab
--------------------
This section describes how to individualize the lab for each student to discourage
sharing of lab solutions.  This is achieved by defining symbols within source 
code or/and data.  The framework will replace these symbols with randomized values
specific to each student.  The config/parameter.config file identifies the files, and
the symbols within those files that are to be modified.  A simple example can be found in 

    labs/formatstring/config/parameter.config

That configuration file causes the string "SECRET2\_VALUE" within the file:

     /home/ubuntu/vul_prog.c

to be replaced with a hexidecimal representation of a random value
between 0x41 and 0x5a, inclusive.

This symbolic replacement occurs when the student first starts the lab container,
but before the execution of the bin/fixlocal.sh script.  Thus, in the formatstring
lab, the executable program resulting from the fixlocal.sh script will be specific
to each student (though not necessarily unique).

Symbolic parameter replacement operations are defined within the config/parameter.config file.
Each line of that file must start with a "<parameter\_id> : ", which is any unique string, and
is followed by one of the following operations:


     RAND_REPLACE : <filename> : <symbol> : <LowerBound> : <UpperBound>
       Replace a symbol within the named file with a random value within a given
       range.  The random value generator is initialized with the lab instance
       seed.

         where: <filename> - the file name (file must exist) where <symbol> is to be replaced
               <symbol> - the string to be replaced
               <LowerBound> and <UpperBound> specifies the lower and upper bound
                                           to be used by random generator
       example:

         <parameter_id> : RAND_REPLACE: /home/ubuntu/stack.c : BUFFER_SIZE : 200 : 2000
         will randomly replace the token string "BUFFER_SIZE" found in
         file stack.c with a number ranging from 200 to 2000
 
     HASH_CREATE : <filename> : <string>
       Create or overwrite a file with a hash of a given string and the lab instance seed.
         where: <filename> - the file name (file will be created if it does not exist)
                <string> -   the input to a MD5 hash operation (after concatenation 
                             with the lab instance seed)
                           
                       
       example:
         <parameter_id> : HASH_CREATE : /home/ubuntu/myseed : bufferoverflowinstance
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
           <parameter_id> HASH_REPLACE : /root/.secret : ROOT_SECRET : mysupersecretrootfile
           The string "ROOT_SECRET" in file /root/.secret will be replaced with an MD5 hash
           of the concatenation of the lab instance seed and "mysupersecretrootfile".

The parameter\_id fields may be referenced during the automated grading function, described below. 


Automated assessment of student labs
------------------------------------
This section describes how to configure a lab for automated assessment of student work.
Note the framework does not require that labs include automated assessment, e.g., the
"results" of a lab may consist entirely of a written report submitted by the student.

The goal of automated assessment is to provide instructors with some confidence that 
students performed the lab, and to give instructors insight into which parts
of a lab students may be having difficulty with.  The automated assessment functions are
not intended to standardize each student's approach to a lab, rather the goal is to permit
ad-hock exploration by students.  Therefore, lab designer should consider ways to identify
evidence that steps of a lab were performed rather than trying to identfy everything a student
may have done in the course of the lab.

The framework's automated assessment functions generally assume the student will interact with one or
more programs or system utilities.  Each time the student invokes a selected program or utility, the 
framework captures copies of standard input and standard output, (stdin and stdout) into timestamped file sets.
This is transparent to the student.  These timestamped file sets, and everything else relative to
the student's home directory, are automatically packaged when the student completes the lab.
These packages of artifacts are then transfered to the instructor, (e.g., via email or a CLE), and 
ingested into the instructor's system where lab assessment occurs.

### Identify Lab-specifc Artifacts ###
The automated assessement fuctions encourage labs to be organized into a set of distinct "goals".
For each goal, the lab designer should identify specific fields within stdin and/or stdout that
could be compared to "expected" values.  These lab-specific artifacts are identified within the
"instr\_config/results.config file".  Artifacts are identified in terms of:

  1) the program that was invoked;
  2) whether the artifict is in stdin or stdout
  3) the line containing the artifact
  4) a token within that line.

Each identified artifact is given a symbolic name, which is then referenced in the goals.config
file to assess whether it is an expected value.

Consider the labs/formatstring/instr\_config/results.config file.  The first non-comment line
defines an artifact that will have the symbolic name "crashStringCanary".  This artifact is
found by looking at stdout from the "vul\_prog" program, finding the first line that starts with:
"\*\*\* stack smashing detected".  The symbol is assigned the value of the third space-delimited 
token in that line.

Entries within the results.config file have the following format:

Format type 1:
     <nametag> = <file_id> : <field_type> : <field_id> : <line_type> : <line_id>
         where:
                   nametag - The symbolic name of the artifact, which will be referenced in the
                             goals configuration file.  It must be alphanumeric, underscores permitted.
                   file_id -- identifies the set of files to be parsed.  The format of this id is:
                       <prog>.[stdin | stdout]
                          where <prog> is the program or utility name.
                   field_type - Optional, defaults to "TOKEN", values include:
                       TOKEN -- Treat the line as space-delimited tokens
                       PARENS -- The desired value is contained in parenthesis
                       QUOTES -- The desired value is contained in parenthesis
                   field_id - An integer identifying the nth occurance of the field type.
                              Alternately may be "LAST" for the last occurance of the field type,
                              or "ALL" for the entire line (which causes the field type to be ignored).
                   line_type - Identifies how the line is to be identified, values include:
                       LINE -- The line_id will be an integer line number (starting at one).
                       STARTSWITH -- the line_id will be a string.  This names the first occurrence of a line
                               that starts with this string. 
                   line_id - See line_type above.

Format type 2:
     <nametag> = [ logfile ] : <line_type> : <line_id>
         where:
                   nametag - The symbolic name of the artifact, which will be referenced in the
                             goals configuration file.  It must be alphanumeric, underscores permitted.
                   logfile - The field is in the logfile result file
                   line_type - Identifies how the line is to be identified, values include:
                       CONTAINS -- the line_id will be a string. nametag will be set to true if logfile
                                   contains the string identified by line_id
                   line_id - See line_type above.

### Assessing the student results ###
Artifacts resulting from student lab activity are assigned symbolic names by the results.config file
as described above.  These symbolic names are then referenced in the goals.config to assess whether
the student obtained expected results.  Each lab goal defined in the goals.config file
will evaluate to TRUE or FALSE, with TRUE reflecting that the student obtained the desired result.
The lab designer can also define "subgoals", some number of which are intended to be evaluated
within a boolen expression representing an actual goal.

As noted earlier, student results may derive from multiple invocations of the same program or system utility.  
To account for cases where students continue
to experiment with programs after they have obtained the desired results, the framework includes
a goal "type" of "matchany", which evaluates as TRUE if the student obtained the expected
result during any invocation of the program or system utility.  In those cases where the student is required
to obtain the expected result during the last invocation of a program, the "matchlast" goal type 
may be specified.

The following syntax defines each goal or subgoal within the goals.config file:


     <id> = <type> : [<operator> : <resulttag> : <answertag> | <boolean_expression>]
       Where: 
         <id> - And identifer for the goal.  It must be alphanumeric (underscores permitted).
         <type> - must be one of the following:
              'matchany' - if the answertag matches any resulttag
                         - note: 'matchany' will NOT be used as sub-goal for goal of type 'boolean' below
              'matchlast' - if the answertag matches the last resulttag
                          - note: 'matchlast' can also be used as sub-goal for goal of type 'boolean' below
              'matchacross' - if the answertag matches resulttag (across different timestamp)
                            - note: 'matchacross' will NOT be used as sub-goal for goal of type 'boolean' below
              'boolean_set' - this is sub-goal to be used with goal of type 'boolean' below
              'boolean' - goal based on boolean operation
                          string that follows will be evaluated for boolean value
    
     <operator> - the following operators evaluate to TRUE as described below:
        'string_equal' -  The strings derived from <answertag> and <resulttag>
                          are equal.
        'string_diff' -   The strings derived from <answertag> and <resulttag>
                          are not equal.
        'string_start' -  The string derived from <answertag> is at the start of 
                          the string derived from <resulttag>.
                example:  answertag value = 'MySecret'
                          resulttag value = 'MySecretSauceIsSriracha'
        'string_end' -    The string derived from <answertag> is at the end of
                          the string derived from <resulttag>.
                example:  answertag value = 'Sriracha'
                          resulttag value = 'EatMoreFoodWithSriracha'
        'integer_equal' - Integers derived from <answertag> and <resulttag>
                          are equal.
        'integer_greater' - The integer derived from <answertag> is greater than
                            that derived from <resulttag>.
        'integer_lessthan'- The integer derived from <answertag> is less than
                            that derived from <resulttag>
                  
     <resulttag>  -- One of the symbolic names defined in the results.config file.
                     The value is interpreted as either a string or an integer,
                     depending on the operator as defined above. 
                     An alternate syntax is to add "result." as a prefix to the
                     symbolic name.
            
     <answertag>  -- Either a literal value (string, integer or hexidecimal), or a symolic name 
                     defined in the results.confg file or the parameters.config file:
 
                     answer=<literal>    -- literal string, integer or hex value (leading with 0x),
                                            interpretation depending on the operator as described above.
                     result.<symbol>     -- symbol from the results.config file
                     parameter.<symbol>  -- symbol from the parameters.config file
                     parameter_ascii.<symbol> -- same as above, but the value parsed as an integer
                                            or hexidecimal and converted to an ascii character.

         Note that values derived from the parameters.config file are assigned the same values as
         were assigned when the lab was parameterized for the student.
