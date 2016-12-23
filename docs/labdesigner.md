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
a directory for the lab and then run the "new\_lab\_setup.sh" script.
This will create a set of template files that you can then customize
for the new lab.  These template files are referenced in the discussion
below.

After creating the new lab directory, cd to that directory and then run

    $SEED_DIR/scripts/designer/bin/new_lab_setup.sh

where SEED\_DIR is set to the top of the svn repo, e.g.,

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
new\_lab\_setup.sh script.

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
Note the framework does not require that labs include automated assessment, e.g., a
lab "results" may consist entirely of a written report submitted by the student.

The goals of automated assessment is to provide instructors with some confidence that 
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
The automated assessement fuctions permit labs to be organized into a set of distinct "goals".
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
a goal "type" of "matchanyany", which evaluates as TRUE if the student obtained the expected
result during any invocation of the program or system utility.  In those cases where the student is required
to obtain the expected result during the last invocation of a program, the "matchonelast" goal type 
may be specified.

The following syntax defines each goal or subgoal within the goals.config file:


     <id> = <type> : [<operator> : <resulttag> : <answertag> | <boolean_expression>]
       Where: 
         <id> - And identifer for the goal.  It must be alphanumeric (underscores permitted).
         <type> - must be one of the following:
              'matchanyany' - if any answertag matches any resulttag
              'matchoneany' - if the first answertag matches any resulttag
                            - note: 'matchanyany' and 'matchoneany' will NOT be used 
                                    as sub-goal for goal of type 'boolean' below
              'matchonelast' - if the first answertag matches the last resulttag
                             - note: 'matchonelast' can also be used as sub-goal for
                                     goal of type 'boolean' below
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
