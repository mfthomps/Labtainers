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
Installation of an Ubunut VM and the Docker system is described
in [Appendix A](#AppendixA).
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
which affect the student's execution environment and the optional automated
assessment of student activity.

Labtainer exercises each have their own
directory under the "labs" directory in the project repository.
The first step in creating a new lab within the framework is to create
a directory for the lab, cd to it, and then run the "new\_lab\_setup.sh" script.
This will create a set of template files that you can then customize
for the new lab.  These template files are referenced in the discussion
below.  After creating the new lab directory, cd to that directory and then run

    $LABTAINER_DIR/scripts/designer/bin/new_lab_setup.py

where LABTAINER\_DIR is set to the top of the svn repo, e.g.,

    export LABTAINER_DIR=/home/mike/seed/trunk

The result is a new labtainer lab that can be run.  While this new
lab will initially only present you with a bash shell to an
empty directory, it is worth testing the lab to understand the workflow.

## Testing the new lab ##
Once a new lab directory is created, and the new\_lab\_setup.py has been run, then 
you can test the new, (currently empty) lab.  All student labs are launched from the
MyStudentDocker directory.  Lab development workflow is easiest if at least two
terminals or tabs are used, one in the new lab directory, and one in the MyStudentDocker
directory.  So, open a new tab or window and:

    cd $LABTAINER_DIR/scripts/MyStudentDocker

Then start the container using the:

    ./redo.py [labname] 

command, where labname is the name of the lab you just created.  
The very first time you run this, it may take a bit of time because it fetches the 
base Labtainer Docker image from the Docker registry.  Subsequent builds
should be faster because your local Docker system will cache portions of the build.  

The redo.py command will remove and recreate the container
each time the script is run.  And it will rebuild the container image if any of its configuration 
information has changed.  This is often necessary when building and testing new labs, to ensure the
new envriroment does not contain artifacts from previous runs.

Note the "redo.py" command is not intended for use by students, they would use the "start.py" command.  

Stop the containers with 

    ./stop.py [labname]

Note that when you stop the container, a path to saved results is displayed.
This is the zip file that the student will forward to the instructor.

To test adding a "hello world" program to the new labtainer, perform the following steps:

 * From the new lab directory window, cd $LABTAINER\_DIR/labs/[labname]/[labname]

 * Create a "hello world" program, e.g., in python or compiled C.

 * From the MyStudentDocker window, run redo.py [labname]
    
You should see the new program in the container's
home directory.  If you run the program from the container, and then stop the container
with stop.py, you will see the stdin and stdout results of the program within the
saved zip file.

Note how the "hello world" program was placed in $LABTAINER\_DIR/labs/[labname]/[labname].
The seemingly redundant "labname" directories are a naming convention in which the
second directory names one of potentially many containers.  In this simple example,
the lab has but one container, whose name defaults to the lab name.

The following sections describe how to futher alter the lab execution environment seen by 
the student.

Defining the lab execution environment
--------------------------------------
A given lab typically requires some set of software packages, and some
system configuration, e.g., network settings.  
The framework captures most configuration details within a standard
Dockerfile.  Templates for two Dockerfiles are placed in the new lab's "dockerfiles" 
directory, one for student containers and one for instructor containers.
These use standard Docker file syntax, which is described at:

    https://docs.docker.com/engine/reference/builder/

Lab designers should reference that Docker documentation for the 
syntax and semantics of these files.
Simple labs should be able to use the default Dockerfile copied by the 
new\_lab\_setup.py script.  That Dockerfile refers to a base Labtainer
image that contains the minimum set of Linux packages necessary to 
host a lab within the framework.  The default
execution environment builds off of a recent Ubuntu image.
[MFT: Note alternate mimimal images as developed, e.g., Fedora.]

A given lab can include multiple containers, each appearing as distinct
computers connected via networks.  The execution environment seen by a
student when interacting with one of these "computers" is therefore defined
by the configuration of the associated container.  

### Container Isolation ###
Docker provides namespace isolation between different containers, and
between the containers and the host platform.  Note however, that all
containers and the host share the same operating system kernel.  Kernel
configuration changes will affect all containers and the host.  For example,
use of sysctl to modify Address Space Layout Randomization (ASLR) will effect
all containers and the effects will persist in the host after the containers
are stopped.

### Naming Containers ###
If a lab is to include only one container, you can
skip ahead to the subsection titled *Lab-specific files in the student's home directory*.

You must assign a name to each container within the new lab.  Each new lab
starts with a single container, whose name matches the lab name.  You are free
to change that name. The names of containers should reflect their role in the lab,
e.g., "client" and "server".  Once you have picked container names, you must create
Dockerfiles and update the *$LABTAINER_DIR/labs/[labname]/config/start.config* file.

Each container must have its own Dockerfile within the *$LABTAINER_DIR/labs/[labname]/dockerfiles*
directory.  The naming convention for dockerfiles is

    Dockerfile.[labname].[container_name].[role]

where role is either "student" or "instructor".  The system automatically creates one Dockerfile
per role.  You are responsible for creating (copying to) additional Dockerfiles for other containers,
and changing the name of the initial Dockerfile if its container name changes.

You must also describe your containers within the *start.config* file as described below.

### Container definitions in start.config ###
Most single container labs can use the automatically generated start.config file file
without modification.  Labs consisting of multiple containers, or requiring custom users
must modify the start.config file.  The following describes the major sections of that configuration
file.

  * GLOBAL\_SETTINGS Beneath this keyword, the following values must be defined:

    * GRADE\_CONTAINER [container name] All lab containers are available the instructor while assessing student labs.
This setting identifies which of the lab containers will host automated grading functions.
    * HOST\_HOME\_XFER [dir name]   Identifies the host directory via which to transfer student artifacts, relative to 
the home directory.  For students, this is where the zip files of their results end up.  For instructors, this is
where zip files should be gathered for assessment.
    * LAB\_MASTER\_SEED [seed]  The master seed string for this lab.  It is combined with the student email
address to create an instance seed that controls parameterization of individual student labs.

  * NETWORK [network name]  One of these sections is require for each network within the lab.  In addition to
providing a name for the network, the following values are defined:

    * MASK [network address mask] The network mask, e.g., 172.25.0.0./24
    * GATEWAY [gateway address] The IP address of the network gateway

  * CONTAINER [container name]  One of these sections is reqired for each container in the lab.
In addition to naming the container, the following values are defined: 

    * TERMINALS [quantity] The number of virtual terminals to open and attach to this container when a lab starts.
If missing, it defaults to 2.
    * USER [user name] The user name whose account will be accessed via the virtual terminals.
    * [network name] [ip address] Network address assignments for each network (defined via a NETWORK section), 
that is to be connected to this container.  A separate line should be entered for each network.
  
A simple example of a two-container lab can be found in $SEED\_DIR/labs/telnetlab. 


### Lab-specific files in the student's home directory ###
Files that are to reside in the student's $HOME directory are placed in the 
new lab container directory.  For example, if a lab includes a source code file, that
should be created in the lab container directory, and it will appear in the student's
home directory within the container when the container starts.  The lab container
directory is at:  

    $LABTAINER_DIR/labs/[labname]/[container name]

Note the name of the container name in labs with a single container matches the labname by default.

### Final lab environment fixup ###
The initial environment encountered by the student is further refined using
the optional bin/fixlocal.sh script.  The framework executes
this script the first time a student starts the lab container.  For example,
this could be used to compile lab-specific programs afer they have been parameterized,
(as described below).  Or this script could perform final configuration adjustments
that cannot be easily performed by the Dockerfile.  These scripts are per-container
and reside at:

    $LABTAINER_DIR/labs/[labname]/[container name]/bin

Parameterizing a lab
--------------------
This section describes how to individualize the lab for each student to discourage
sharing of lab solutions.  This is achieved by defining symbols within source 
code or/and data.  The framework will replace these symbols with randomized values
specific to each student.  The config/parameter.config file identifies the files, and
the symbols within those files that are to be modified.  A simple example can be found in 

    $LABTAINER_DIR/labs/formatstring/formatstring/config/parameter.config

That configuration file causes the string "SECRET2\_VALUE" within the file:

     /home/ubuntu/vul_prog.c

to be replaced with a hexidecimal representation of a random value
between 0x41 and 0x5a, inclusive.

This symbolic replacement occurs when the student first starts the lab container,
but before the execution of the bin/fixlocal.sh script.  Thus, in the formatstring
lab, the executable program resulting from the fixlocal.sh script will be specific
to each student (though not necessarily unique).

Symbolic parameter replacement operations are defined within the config/parameter.config file.
Each line of that file must start with a "`<parameter_id>` : ", which is any unique string, and
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

         some_parameter_id : RAND_REPLACE: /home/ubuntu/stack.c : BUFFER_SIZE : 200 : 2000
         will randomly replace the token string "BUFFER_SIZE" found in
         file stack.c with a number ranging from 200 to 2000
 
     HASH_CREATE : <filename> : <string>
       Create or overwrite a file with a hash of a given string and the lab instance seed.
         where: <filename> - the file name (file will be created if it does not exist)
                <string> -   the input to a MD5 hash operation (after concatenation 
                             with the lab instance seed)
                           
                       
       example:
         some_parameter_id : HASH_CREATE : /home/ubuntu/myseed : bufferoverflowinstance
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
           some_parameter_id HASH_REPLACE : /root/.secret : ROOT_SECRET : mysupersecretrootfile
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
  3) the line containing the artifact, and a token within that line.
  4) ad-hoc properties, such as the quantity of lines in the stdin file.

Each identified artifact is given a symbolic name. A named artifact is referred to herein as a *result*, which 
is then referenced in the goals.config file to assess whether it is an expected value.

Consider the labs/formatstring/instr\_config/results.config file.  The first non-comment line
defines a result having the symbolic name "crashStringCanary".  This result is
found by looking at stdout from the "vul\_prog" program, finding the first line that starts with:
"\*\*\* stack smashing detected".  The result is assigned the value of the third space-delimited 
token in that line.

Entries within the results.config file each have one of the two following formats:

Format type 1:
     <nametag> = <file_id> : <field_type> : <field_id> : <line_type> : <line_id>
         where:
                   nametag - The symbolic name of the result, which will be referenced in the
                             goals configuration file.  It must be alphanumeric, underscores permitted.
                   file_id -- identifies the set of files to be parsed.  The format of this id is:
                       <prog>.[stdin | stdout]
                          where <prog> is the program or utility name.
                   field_type - Optional, defaults to "TOKEN", values include:
                       TOKEN -- Treat the line as space-delimited tokens
                       PARENS -- The desired value is contained in parenthesis
                       QUOTES -- The desired value is contained in parenthesis
                       SLASH -- The desired value is contained within slashes, e.g., /foo/
                       LINE_COUNT -- The quantity of lines in the file. Remaining fields are ignored.
                   field_id - An integer identifying the nth occurance of the field type.
                              Alternately may be "LAST" for the last occurance of the field type,
                              or "ALL" for the entire line (which causes the field type to be ignored).
                   line_type - Identifies how the line is to be identified, values include:
                       LINE -- The line_id will be an integer line number (starting at one). Use of this
                               to identify lines is discouraged since minor lab changes might alter the count.
                       STARTSWITH -- the line_id will be a string.  This names the first occurrence of a line
                               that starts with this string. 
                       NEXTSTARTSWITH -- the line_id will be a string.  This names the line preceeding the 
                               first occurrence of a line that starts with this string. 
                   line_id - See line_type above.

Format type 2:
     <nametag> = [ logfile ] : <line_type> : <line_id>
         where:
                   nametag - The symbolic name of the result, which will be referenced in the
                             goals configuration file.  It must be alphanumeric, underscores permitted.
                   logfile - The field is in the logfile result file
                   line_type - Identifies how the line is to be identified, values include:
                       CONTAINS -- the line_id will be a string. nametag will be set to true if logfile
                                   contains the string identified by line_id
                   line_id - See line_type above.

#### Capturing information about the environment ####
Some labs require the student to alter system configuration settings,
e.g., using the sysctl command to effect ASLR. A *checklocal.sh* script in:

    $LABTAINER_DIR/labs/[labname]/[container name]/bin

is intended to contain whatever commands are necessary to record the 
state of the system at the time a program was invoked.  The stdout of
the checklocal.sh script is recorded at the beginning of the stdout artifact. 

### Assessing the student results ###
Results of student lab activity are assigned symbolic names by the results.config file
as described above.  These results are then referenced in the goals.config to assess whether
the student obtained expected results.  Each lab goal defined in the goals.config file
will evaluate to TRUE or FALSE, with TRUE reflecting that the student met the defined goal.
Once evaluated, a goal may determine the state of subsequent goals within the goals.config file, 
i.e., through use of boolean expressions and temporal comparisons between goals.  The evaluated
state of each goal can then contribte to a student grade.

As noted earlier, student results may derive from multiple invocations of the same program or system utility.  
The framework does not discourage students from continuing to experiment and explore aspects of the 
exercise subsequent to obtiaining the desired results.  In general, the assessment determines if the student
obtained expected results during any invocation of a program or system utility.  In those cases 
where the student is required to obtain the expected results during the *last* invocation of a program, 
the *matchlast* goal type may be specified as described below.

To facilitate grading multiple attempts or explorations of a lab exercise, the framework associates
timestamps with the results of processing the results.config file.  A single timestamp will
include results from a stdin file and a stdout file.  In general, there will be a distinct, 
timestamped set of results for each occurance of a student invoking a targeted program.

The following syntax defines each goal or subgoal within the goals.config file:


     <goal_id> = <type> : [<operator> : <resulttag> : <answertag> | <boolean_expression> | goal1 : goal2 
                           | count_greater : value : subgoal_list ]
       Where: 
         <goal_id> - An identifer for the goal.  It must be alphanumeric (underscores permitted).
         <type> - must be one of the following:
              'matchany'    - Results from all timestamped sets are evaluated.
                              If the answertag names a result, then both that result and
                              the resulttag must occur in the same timestamped set.
                              The 'matchany' goals are treated as a set of values, each 
                              timestamped based on the timestamp of the reference resulttag.
                           
              'matchlast'   - only results from the latest timestamped set are evaluated.
              'matchacross' - The answertag must name a result, and that result must occur
                              in a timestamped set that differs from the set in which the resulttag occurs.
                            - note: 'matchacross' cannot be used within the boolean expression defined below.
              'boolean'     - The goal value is computed from a boolean expression consisting of 
                              goal_id's and boolean operators, ("and", "or", "and_not", "or_not", and "not"), 
                              and parenthisis for precedence.
                              The goal_id's must be from goals defined earlier in the goals.config file. 
                              The goal evalutes to TRUE if the boolen expression evaluates to TRUE for any
                              of the timestamped sets of goal_ids, (see the 'matchany' discussion above).
                              The goal_id's cannot include any "matchacross" goals.
              'count_greater' The goal is true if the count of true subgoals in the list exceeds the given value.
                              The subgoal list is comma-separated within parenthesis.
              'time_before' - Both goal1 and goal2 must be goal_ids from previous *matchany* goal types.
                              Evaluates to TRUE if any TRUE goal1 has a timestamp that is before than any
                              TRUE goal2
              'time_during' - Both goal1 and goal2 must be goal_ids from previous *matchany* goal types.
                              Timestamps include a start and end time, reflecting when the program starts
                              and when it terminates.
                              Evaluates to TRUE if any TRUE goal1 has a start timestamp within the start
                              and end tmes of any TRUE goal2.
    
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



<a name="AppendixA"/>
Appendix A: Installing Ubuntu & Docker
=======================================
</a>
The instructions below describe installation of an Ubuntu Linux VM 
to serve as the Labtainer host.

Install Virutal Box: https://www.virtualbox.org/wiki/Downloads
Download the latest Ubuntu LTS distribution .iso image.
Use VirtualBox to create a new VM, allocate at least 10GB of disk storage.
Select the Ubuntu iso image in the VirtualBox storage settings, and select "Live CD/DVD"
Power on the virtual machine and install Ubuntu.
Install subversion on Ubuntu:
sudo apt-get install subversion

Retrieve the labtainer repository.

    svn co https://tor.ern.nps.edu/svn/proj/seed

Define the LABTAINER\_DIR environment variable (and consider
placing the definition in your ~/.bashrc file), e.g., 

    export LABTAINER_DIR=/home/mike/seed/trunk

Install Docker on Ubuntu (this will lead to a reboot of the VM).

    cd $LABTAINER_DIR/setup_scripts
    ./installDocker.sh

Edit the $LABTAINER\_DIR/setup\_scripts/fixresolve.sh script to help Docker resolve
host names.  The fixresolve.sh script is configured for use within the NPS network.
