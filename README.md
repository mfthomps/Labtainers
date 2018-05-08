Labtainers: A Docker-based cyber lab framework
==============================================

Labtainers include more than 35 cyber lab exercises and tools to build your own. Import a single VM appliance or install on a Linux system and your students are done with provisioning and administrative setup, for these and future lab exercises.

* Consistent lab execution environments and automated provisioning via Docker containers
* Multi-component network topologies on a modestly performing laptop computer 
* Automated assessment of student lab activity and progress
* Individualized lab exercises to discourage sharing solutions

Labtainers provide controlled and consistent execution environments in which students perform labs entirely within the confines of their computer, regardless of the Linux distribution and packages installed on the student's computer.  The only requirement is that the Linux system supports Docker.  See the [Papers][Papers] for additional information about the framework.

The Labtainers website, and the downloads are at <https://my.nps.edu/web/c3o/labtainers>.

Distribution created: mm/dd/yyyy
Revision: 

## Content
[Distribution and Use](#distribution-and-use)

[Guide to directories](#guide-to-directories)

[Support](#support)

[Release notes](#release-notes)

## Distribution and Use
Labtainers was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 

However, several of the labs are derived from SEED labs from 
Syracuse University, and include copyrighted and licensed elements
as set forth in their respective Lab Manuals.  These labs include:
bufoverflow, capabilities, formatstring, local-dns, onewayhash,
retlibc, setuid-env, sql-inject, tcpip, webtrack, xforge and xsite.

## Guide to directories

* scripts/labtainers-student -- the work directory for running and 
   testing student labs.  You must be in that directory to run 
   student labs.
   
* scripts/labtainers-instructor -- the work directory for 
   running and testing automated assessment and viewing student
   results.
  
* labs -- Files specific to each of the labs
   
* setup_scripts -- scripts for installing Labtainers and Docker and updating Labtainers
   
* docs -- latex source for the labdesigner.pdf, and other documentation.
   
* config -- system-wide configuration settings (these are not the 
   lab-specific configuration settings.
 
* distrib -- distribution support scripts, e.g., for publishing labs to the Docker hub.

* testsets -- Test procedures and expected results. (Per-lab drivers for SimSec are not 
distributed).

* pkg-mirrors -- utility scripts for internal NPS package mirroring to reduce external 
package pulling during tests and distribution.

## Support
Use the GitHub issue reports, or email me at mfthomps@nps.edu

Also see <https://my.nps.edu/web/c3o/support1> 


## Release notes

The standard Labtainers distribution does not include files required for development
of new labs.  For those, run ./update-designer.sh from the labtainer directory.

The installation script and the update-designer.sh script set environment variables,
so you may want to logout/login, or start a new bash shell before using Labtainers the
first time.

May 7, 2018
- Use C-based capinout program instead of the old capinout.sh to capture stdin and
stdout. See trunk/src-tool/capinout.  Removes limitations associated with use ctrl-C 
to break monitored programs and the display of passwords in telnet and ssh.
- Include support for saki bulk\_download zip processing to extract seperatly submitted
reports, and summarizes missing submits.
- Add checks to user-provided email to ensure they are printable characters.
- While grading, if user-supplied email does not match zip file name, proceed to grade
the results, but include note in the table reflecting *cheating*.  Require to recover from
cases where student enters garbage for an email address.
- Change telnetlab grading to not look at tcpdump output for passwords -- capinout fix
leads to correct character-at-a-time transmission to server.
- Fix typo in install-docker.sh and use sudo to alter docker dns setting in that script.

April 26, 2018
- Transition to use of "labtainer" to start lab, and "stoplab" to stop it.
- Add --version option to labtainer command.
- Add log\_ts and log\_range result types, and time\_not\_during goal operators.
Revamp the centos-log and sys-log grading to use these features.
- Put labsys.tar into /var/tmp instead of /tmp, sometimes would get deleted before expanded
- Running X applications as root fails after reboot of VM.
- Add "User Command" man pages to CentOS based labs
- Fix recent bug that prevented collection of docs files from students
- Modify smoke-tests to only compare student-specific result line, void of whitespace

April 20, 2018
- The denyhosts service fails to start the first time, moved start to student\_startup.sh.
- Move all faux\_init services until after parameterization -- rsyslog was failing to start
on second boot of container.
April 19, 2018
- The acl lab failed to properly assess performance of the trojan horse step.
- Collect student documents by default. 
- The denyhost lab changed to reflect that denyhosts (or tcp wrappers?) now
modifies iptables.  Also, the denyhosts service was failing to start on some occasions.
- When updating Labtainers, do not overwrite files that are newer than those
  in the archive -- preserve student lab reports.

April 12, 2018

- Add documentation for the purpose of lab goals, and display this for the instructor
   when the instructor starts a lab.
- Correct use of the precheck function when the program is in treataslocal, pass capintout.sh
   the full program path.
- Copy instr_config files at run time rather than during image build.
- Add Designer Guide section on debugging automated assessment.
- Incorrect case in lab report file names.
- Unncessary chown function caused instructor.py to sometimes crash.
- Support for automated testing of labs (see SimLab and smoketest).
- Move testsets and distrib under trunk
  
April 5, 2018

- Revise Firefox profile to remove "you've not use firefox in a while..." message.
- Remove unnessary pulls from registry -- get image dates via docker hub API instead.

March 28, 2018

- Use explicit tar instead of "docker cp" for system files (Docker does
   not follow links.) 
- Fix backups lab use separate file system and update the manual.

March 26, 2018

-  Support for multi-user modes (see Lab Designer User Guide).
-  Removed build dependency on the lab_bin and lab_sys files. Those are now copied
   during parameterization of the lab.
-  Move capinout.sh to /sbin so it can be found when running as root.

March 21, 2018

-  Add CLONE to permit multiple instances of the same container, e.g., for 
   labs shared by multiple concurrent students.
-  Adapt kali-test lab to provide example of macvlan and CLONE
-  Copy the capinout.sh script to /sbin so root can find it after a sudo su.

March 15, 2018

-  Support macvlan networks for communications with external hosts
-  Add a Kali linux base, and a Metasploitable 2 image (see kali-test)

March 8, 2018

-  Do not require labname when using stop.py
-  Catch errors caused by stray networks and advise user on a fix
-  Add support for use of local apt & yum repos at NPS

February 21, 2018

-  Add dmz-lab
-  Change "checklocal" to "precheck", reflecting it runs prior to the command.
-  Decouple inotify event reporting from use of precheck.sh, allow inotify
   event lists to include optional outputfile name.
-  Extend bash hook to root operations, flush that bash_history.
-  Allow parameterization of start.config fields, e.g., for random IP addresses
-  Support monitoring of services started via systemctl or /etc/init.d
-  Introduce time delimeter qualifiers to organize a timestamped log file into
   ranges delimited by some configuration change of interest (see dmz-lab)

February 5, 2018

-  Boolean values from results.config files are now treated as goal values
-  Add regular expression support for identifying artifact results.
-  Support for alternate Docker registries, including a local test registry for testing
-  Msc fixes to labs and lab manuals
-  The capinout monitoring hook was not killing child processes on exit.
-  Kill monitored processes before collecting artifacts
-  Add labtainer.wireshark as a baseline container, clean up dockerfiles

January 30, 2018

-  Add snort lab
-  Integrate log file timestamps, e.g., from syslogs, into timestamped results.
-  Remove undefined result values from intermediate timestamped json result files.
-  Alter the time_during goal assessment operation to associate timestamps with 
   the resulting goal value.

January 24, 2018

-  Use of tabbed windows caused instructor side to fail, use of double quotes.
-  Ignore files in \_tar directories (other than .tar) when determining build
   dependencies.

[Papers]: https://my.nps.edu/web/c3o/labtainers#papers
