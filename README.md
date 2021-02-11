Labtainers: A Docker-based cyber lab framework
==============================================

Labtainers include more than 50 cyber lab exercises and tools to build your own. Import a single [VM appliance][vm-appliance] or install on a Linux system and your students are done with provisioning and administrative setup, for these and future lab exercises.  

* Consistent lab execution environments and automated provisioning via Docker containers
* Multi-component network topologies on a modestly performing laptop computer 
* Automated assessment of student lab activity and progress
* Individualized lab exercises to discourage sharing solutions

Labtainers provide controlled and consistent execution environments in which students perform labs entirely within the confines of their computer, regardless of the Linux distribution and packages installed on the student's computer.  Labtainers run on our [VM appliance][vm-appliancee], or on any Linux
with Dockers installed, and on Docker Workstation running on Mac or Windows computers.  

See the [Student Guide][student-guide] for installation and use, and the [Instructor Guide][instructor-guide] for student assessment.  Developing and customizing
lab exercises is described in the [Designer Guide][designer-guide].
See the [Papers][Papers] for additional information about the framework.
The Labtainers website, and downloads (including VM appliances with Labtainers pre-installed) are at <https://nps.edu/web/c3o/labtainers>.

[vm-appliance]: https://nps.edu/web/c3o/virtual-machine-images
[student-guide]: docs/student/labtainer-student.pdf
[instructor-guide]: docs/instructor/labtainer-instructor.pdf
[designer-guide]: docs/labdesigner/labdesigner.pdf
[Papers]: https://nps.edu/web/c3o/labtainers#papers

Distribution created: 02/09/2021 13:44 </br>
Previous revision: v1.3.3s </br>
Commit: 8ffe4864 </br>
Branch: master </br>

## Content
[Distribution and Use](#distribution-and-use)

[Guide to directories](#guide-to-directories)

[Support](#support)

[Release notes](#release-notes)

## Distribution and Use
Please see the licensing and distribution information
in the [docs/license.md file](docs/license.md).

## Guide to directories

* scripts/labtainers-student -- the work directory for running and 
   testing student labs.  You must be in that directory to run 
   student labs.
   
* scripts/labtainers-instructor -- the work directory for 
   running and testing automated assessment and viewing student
   results.
  
* labs -- Files specific to each of the labs
   
* setup\_scripts -- scripts for installing Labtainers and Docker and updating Labtainers
   
* docs -- latex source for the labdesigner.pdf, and other documentation.

* UI -- Labtainers lab editor source code (Java).

* headless-lite -- scripts for managing Docker Workstation and cloud instances of Labtainers (systems
that do not have native X11 servers.)
   
* scripts/designer -- Tools for building new labs and managing base Docker images.

* config -- system-wide configuration settings (these are not the 
   lab-specific configuration settings.
 
* distrib -- distribution support scripts, e.g., for publishing labs to the Docker hub.

* testsets -- Test procedures and expected results. (Per-lab drivers for SimLab are not 
distributed).

* pkg-mirrors -- utility scripts for internal NPS package mirroring to reduce external 
package pulling during tests and distribution.

## Support
Use the GitHub issue reports, or email me at mfthomps@nps.edu

Also see <https://my.nps.edu/web/c3o/support1> 


## Release notes

The standard Labtainers distribution does not include files required for development
of new labs.  For those, run ./update-designer.sh from the labtainer/trunk/setup\_scripts directory.

The installation script and the update-designer.sh script set environment variables,
so you may want to logout/login, or start a new bash shell before using Labtainers the
first time.

February 11, 2021
- Fix UI handling of editing files.  Revise layout and eliminate unused fields.
- Add ubuntu20 base2 base configuration along with ssh2, network2 and wireshark2
- The new wireshark solves the prolem of black/noise windows.
- Map /tmp/.X11-unix to /var/tmp and create a link.  Needed for ubuntu20 (was deleting /tmp?) and may fix others.

February 4, 2021
- Add SIZE option to results artifacts
- Simplify wireshark-intro assessment and parameterization and add PDF lab manual.
- Provide parameter list values to pregrade.sh script as environment variables
- enable X11 on the grader
- put update-designer.sh into users path.

January 19, 2021
- Change management of README date/rev to update file in source repo.
- Introduce GUI for creating/editing labs -- see labedit command.

December 21, 2020
- The gradelab function failed when zip files were copied from a VirtualBox shared folder.
- Update Instructor Guide to describe management of student zip files on host computers.

December 4, 2020
- Transition distribution of tar to GitHub releaese artifacts
- Eliminate seperate designer tar file, use git repo tarball.
- Testing of grader web functions for analysis of student lab artifacts
- Clear logs from full smoketest and delete grader container in removelab command.

December 1, 2020
- The iptables2 lab assessment relied on random ports being "unknown" to nmap.
- Use a sync diretory to delay smoketests from starting prior to lab startup.
- Begin integrating Lab designer UI elements.

October 13, 2020
- Headless configuraions for running on Docker Desktop on Macs & Windows
- Headless server support, cloud-config file for cloud deployments
- Testing support for headless configurations
- Force mynotify to wait until rc.local runs on boot
- Improve mynotify service ability to merge output into single timestamp
- Python3 for stopgrade script
- SimLab now uses docker top rather than system ps

September 26, 2020
- Clean up the stoplab scripts to ignore non-lab containers
- Add db-access database access control lab for controlles sharing of a mysql db.

September 17, 2020
- The macs-hash lab was unable to run Leafpad due to the X11 setting.
- Grader logging was being redirected to the wrong log file, now captures errors from instructor.py
- Copy instructor.log from grader to the host logs directory if there is an error.

August 28, 2020
- Fix install script to use python3-pip and fix broken scripts: getinfo.py and pull-all.py
- Registry logic was broken, test systems were not using the test registry, add development documentation.
- Add juiceshop and owasp base files for OWASP-based web security labs
- Remove unnecessary sudos from check\_nets
- Add CHECK\_OK documentation directive for automated assessment
- Change check\_nets to fix iptables and routing issues if so directed.

August 12, 2020
- Add timeout to prestop scripts
- Add quiz and checkwork to dmz-lab
- Restarting the dmz-lab without -r option broke routing out of the ISP.
- Allow multiple files for time\_delim results.

August 6, 2020
- Bug in error handling when X11 socket is missing
- Commas in quiz questions led to parse errors
- Add quiz and checkwork to iptables2 lab

July 28, 2020
- Add quiz support -- these are guidance quizzes, not assessment quizzes.  See the designer guide.
- Add current-state assessment for use with the checkwork command.

July 21, 2020
- Add testsets/bin to designer's path
- Designer guide corrections and explainations for IModule steps.
- Add RANGE\_REGEX result type for defining time ranges using regular expressions on log entries.
- Check that X11 socket exists if it is needed when starting a lab.
- Add base image for mysql
- Handle mysql log timestamp formats in results parsing. 

June 15, 2020
- New base image contianing the Bird open source router
- Add bird-bgp Border Gateway Protocol lab.
- Add bird-ospf Open Shortest Path First routing protocol.
- Improve handling of DNS changes, external access from some containers was blocked in some sites.
- Add section to Instructor Guide on using Labtainers in environments lacking Internet access.

May 21, 2020
- Move all repositories to the Docker Hub labtainers registry
- Support mounts defined in the start.config to allow persistent software installs
- Change ida lab to use persistent installation of IDA -- new name is ida2
- Add cgc lab for exploration of over 200 vulnerable services from the DARPA Cyber Grand Challenge
- Add type\_string command to SimLab
- Add netflow lab for use of NetFlow network traffic analysis
- Add 64-bit versions of the bufoverflow and the formatstring labs

April 9, 2020
- Grader failed assessment of CONTAINS and FILE\_REGX conditions when wildcards were used for file selection.
- Include hints for using hexedit in the symlab lab.
- Add hash\_equal operator and hash-goals.py to automated assessment to avoid publishing expected answers in configuration files.
- Automated assessment for the pcap-lib lab.

April 7, 2020
- Logs have been moved to $LABTAINER\_DIR/logs
- Other cleanup to permit rebuilds and tests using Jenkins, including use of unique temporary directories for builds
- Move build support functions out of labutils into build.py
- Add pcap-lib lab for PCAP library based development of traffic analysis programs

March 13, 2020
- Add plc-traffic lab for use of GrassMarlin with traffic generated during the lab.
- Introduce ability to add "tap" containers to collect PCAPs from selected networks.
- Update GNS3 documentation for external access to containers, and use of dummy\_hcd to 
  simulate USB drives.
- Change kali template to use faux\_init rather than attempting to use systemd.
- Moving distributions (tar files) to box.com
- Change SimLab use of netstat to not do a dns lookup.

February 26, 2020
- If labtainer command does not find lab, suggest that user run update-labtainer.sh
- Add support preliminary support for a network tap component to view all network traffic.
- Script to fetch lab images to prep VMs that will be used without internet.
- Provide username and password for nmap-discovery lab.

February 18, 2020
- Inherit the DISPLAY environment variable from the host (e.g., VM) instead of assuming :0

February 14, 2020
- Add Ghidra software reverse engineering introduction exercise.

February 11, 2020
- Update guides to describe remote access to containers withing GNS3 environments
- Hide selected components and links within GNS3.
- Figures in the webtrack lab guide were not visible; typos in this and nmap-ssh

February 6, 2020
- Introduce function to remotely manage containers, e.g., push files.
- Add GNS3 environment function to simulate insertion of a USB drive.
- Improve handling of Docker build errors.

February 3, 2020
- On the metasploit lab, the postgresql service was not running on the victim.
- Merge the IModule manual content into the Lab Designer guide.
- More IModule support.

January 27, 2020
- Introduce initial support for IModules (instructor-developed labs).  See docs/imodules.pdf.
- Fix broken LABTAINER\_DIR env variable within update-labtainer
- Fix access mode on accounting.txt file in ACL lab (had become rw-r-r).  Use explicit chmod in fixlocal.sh.

January 14, 2020
- Port framework and gradelab to Python3 (existing Python2 labs will not change)
  - Use backward compatible random.seed options
  - Hack non-compatable randint to return old values
  - Continue to support python2 for platforms that lack python3 (or those such as the
    older VM appliance that include python 3.5.2, which breaks random.seed compatability).
  - Add rebuild alias for rebuild.py that will select python2 if needed.
- Centos-based labs manpages were failing; use mandb within base docker file
- dmz-lab netmask for DMZ network was wrong (caught by python3); as was IP address of inner gateway in lab manual
- ghex removed from centos labs -- no longer easily supported by centos 7
- file-deletion lab must be completed without rebooting the VM, note this in the Lab Manual.
- Add NO\_GW switch to start.config to disable default gateways on containers.
- Metasploit lab, crashes host VM if runs as privileged; long delays on su if systemd enabled; so run without systemd.
  Remove use of database from lab manual, configure to use new no\_gw switch
- Update file headers for licensing/terms; add consolidated license file.
- Modify publish.py to default to use of test registry, use -d to force use of default\_registry
- Revise source control procedures to use different test registry for each branch, and use a premaster
branch for final testing of a release.

October 9, 2019
- Remove dnsmasq from dns component in the dmz-lab.  Was causing bind to fail on some installations.

October 8, 2019
- Syntax error in test registry setup; lab designer info on large files; fetch bigexternal.txt files

September 30, 2019
- DockerHub registry retrieval again failing for some users.  Ignore html prefix to json.

September 20, 2019
- Assessment of onewayhash should allow hmac operations on file of student's choosing.

September 5, 2019
- Rebuild metasploit lab, metasploit-framework exhibited a bug.  And the labs "treataslocal" file
was left out of the move from svn.  Fix type in metasploit lab manual.

August 30, 2019
- Revert test for existence of container directories, they do not always exist.

August 29, 2019
- Lab image pulls from docker hub failed due to change in github or curl?  Catch rediret to cloudflare.
Addition of GNS3 support.  Fix to dmz-lab dnssec.

July 11, 2019
- Automated assessment for CentOS6 containers, fix for firefox memory issue, support arbitrary docker 
create arguments in the start.config file.

June 6, 2019
- Introduce a Centos6 base, but not support for automated assessment yet

May 23, 2019
- Automated assessment of setuid-env failed due to typos in field seperators.

May 8, 2019
- Corrections to Capabilities lab manual

May 2, 2019
- Acl lab fix to bobstuff.txt permissions.  Use explicit chmod in fixlocal.sh
- Revise student guide to clarify use of stop and -r option in body of the manual.

March 9, 2019
- The checkwork function was reusing containers, thereby preventing students from eliminating artifacts
from previous lab work.  
- Add appendix to the symkey lab to describe the BMP image format.

February 22, 2019
- The http server failed to start in the vpn and vpn2 labs.  Automated assessment removed from those labs until reworked.

January 7, 2019
- Fix gdblesson automated assessment to at least be operational.

January 27, 2019
- Fix lab manual for routing-basics2 and fix routing to enable external access to internal web server.

December 29, 2018
- Fix routing-basics2, same issues as routing-basics, plus an incorret ip address in the gateway resolv.conf

December 5, 2018
- Fix routing-basics lab, dns resolution at isp and gatway components was broken.

November 14, 2018
- Remove /run/nologin from archive machine in backups2 -- need general solution for this nologin issue

November, 5, 2018
- Change file-integrity lab default aid.conf to track metadata changes rather than file modification times

October 22, 2018
- macs-hash lab resolution verydodgy.com failed on lab restart
- Notify function failed if notify_cb.sh is missing

October 12, 2018
- Set ulimit on file size, limit to 1G

October 10, 2018
- Force collection of parameterized files
- Explicitly include leafpad and ghex in centos-xtra baseline and rebuild dependent images.

September 28, 2018
- Fix access modes of shared file in ACL lab
- Clarify question in pass-crack
- Modify artifact collection to ignore files older than start of lab.
- Add quantum computing algorithms lab

September 12, 2018
- Fix setuid-env grading syntax errors
- Fix syntax error in iptables2 example firewall rules
- Rebuild centos labs, move lamp derivatives to use lamp.xtr for waitparam and force
httpd to wait for that to finish.

September 7, 2018
- Add CyberCIEGE as a lab
- read\_pre.txt information display prior to pull of images, and chance to bail.

September 5, 2018
- Restore sakai bulk download processing to gradelab function.
- Remove unused instructor scripts.

September 4, 2018
- Allow multiple IP addresses per network interface
- Add base image for Wine
- Add GRFICS virtual ICS simulation

August 23, 2018
- Add GrassMarlin lab (ICS network discovery)

August 23, 2018
- Add GrassMarlin lab (ICS network discovery)

August 21, 2018
- Another fix around AWS authentication issues (DockerHub uses AWS).
- Fix new\_lab\_setup.py to use git instead of svn.
- Split plc-forensics lab into a basic lab and and advanced lab (plc-forensics-adv)

August 17, 2018
- Transition to git & GitHub as authoritative repo.

August 15, 2018
- Modify plc-forensics lab assessment to be more general; revise lab manual to reflect wireshark on the Labtainer.
 
August 15, 2018
- Add "checkwork" command allowing students to view automated assessment  results for their lab work.
- Include logging of iptables packet drops in the iptables2 and the iptables-ics lab.
- Remove obsolete instances of is\_true and is\_false from goal.config
- Fix boolean evaluation to handle "NOT foo", it had expected more operands.

August 9, 2018
- Support parameter replacement in results.config files
- Add TIME\_DELIM result type for results.config
- Rework the iptables lab, remove hidden nmap commands, introduce custom service

August 7, 2018
- Add link to student guide in labtainer-student directory
- Add link to student guide on VM desktops
- Fixes to iptables-ics to avoid long delay on shutdown; and fixes to regression tests
- Add note to guides suggesting student use of VM browser to transfer artifact zip file to instructor.

August 1, 2018
- Use a generic Docker image for automated assessment; stop creating "instructor" images per lab.

July 30, 2018
- Document need to unblock the waitparam.service (by creating flag directory)
if a fixlocal.sh script is to start a service for which waitparam is a
prerequisite.
- Add plc-app lab for PLC application firewall and whitelisting exercise.

July 25, 2018
- Add string\_contains operator to goals processing
- Modify assessment of formatstring lab to account for leaked secret not always being
at the end of the displayed string.

July 24, 2018
- Add SSH Agent lab (ssh-agent)

July 20, 2018
- Support offline building, optionally skip all image pulling
- Restore apt/yum repo restoration to Dockerfile templates.
- Handle redirect URL's from Docker registry blob retrieval to avoid 
authentication errors (Do not rely on curl --location).

July 12, 2018
- Add prestop feature to allow execution of designer-specified scripts on
selected components prior to lab shutdown.  
- Correct host naming in the ssl lab, it was breaking automated assessment.
- Fix dmz-lab initial state to permit DNS resolutions from inner network.
- FILE\REGEX processing was not properly handling multiline searches.
- Framework version derived from newly rebuilt images had incorrect default value.
 
July 10, 2018
- Add an LDAP lab
- Complete transition to systemd based Ubuntu images, remove unused files
- Move lab\_sys tar file to per-container tmp directory for concurrency.

July 6, 2018
- All Ubuntu base images replaced with versions based on systemd
- Labtainer container images in registry now tagged with base image ID & have labels reflecting 
the base image.
- A given installation will pull and use images that are consistent with the base images it possesses.
- If you are using a VM image,  you may want to replace that with a newer VM image from our website.
- New labs will not run without downloading newer base images; which can lead to your VM storing multiple
versions of large base images (> 500 MB each).
- Was losing artifacts from processes that were running when lab was stopped -- was not properly killing capinout
processes.

June 27, 2018
- Add support for Ubuntu systemd images
- Remove old copy of SimLab.py from labtainer-student/bin
- Move apt and yum sources to /var/tmp
- Clarify differences between use of "boolean" and "count\_greater" in assessments
- Extend Add-HOST in start.config to include all components on a network.
- Add option to new\_lab\_setup.py to add a container based on a copy of an existing container.

June 21, 2018
- Set DISPLAY env for root
- Fix to build dependency handling of svn status output
- Add radius lab
- Bug in SimLab append corrected
- Use svn, where appropriate, to change file names with new\_lab\_setup.py

June 19, 2018
- Retain order of containers defined in start.conf when creating terminal with multiple tabs
- Clarify designer manual to identify path to assessment configuration files.
- Remove prompt for instructor to provide email
- Botched error checking when testing for version number
- Include timestamps of lab starts and redos in the assessment json
- Add an SSL lab that includes bi-directional authentication and creation of certificates.

June 14, 2018
- Add diagnostics to parameterizing, track down why some install seem to fail on that.
- If a container is already created, make sure it is parameterized, otherwise bail to avoid corrupt or half-baked containers.
- Fix program version number to use svn HEAD

June 15, 2018
- Convert plain text instructions that appeared in xterms into pdf file.
- Fix bug in version handling of images that have not yet been pulled.
- Detect occurance of a container that was created, but not parameterized,
and prompt the user to restart the lab with the "-r" option.
- Add designer utility: rm\_svn.py so that removed files trigger an image rebuild.

June 13, 2018
- Install xterm on Ubuntu 18 systems
- Work around breakage in new versions of gnome-terminal tab handling

June 11, 2018
- Add version checking to compare images to the framework.
- Clarify various lab manuals

June 2, 2018
- When installing on Ubuntu 18, use docker.io instead of docker-ce
- The capinout caused a crash when a "sudo su" monitored command is followed by
a non-elevated user command.
- Move routing and resolv.conf settings into /etc/rc.local instead of fixlocal.sh
so they persist across start/stop of the containers.

May 31, 2018
- Work around Docker bug that caused text to wrap in a terminal without a line feed.
- Extend COMMAND\_COUNT to account for pipes
- Create new version of backups lab that includes backups to a remote server and 
backs up an entire partition.
- Alter sshlab instructions to use ssh-copy-id utility
- Delte /run/nologin file from parameterize.sh to permit ssh login on CentOS

May 30, 2018
- Extended new\_lab\_setup.py to permit identification of the base image to use
- Create new version of centos-log that includes centralized logging.
- Assessment validation was not accepting "time\_not\_during" option.
- Begin to integrate Labtainer Master for managing Labtainers from a Docker container.

May 25, 2018
- Remove 10 second sleeps from various services.  Was delaying xinetd responses, breaking
automated tests.
- Fix snort lab grading to only require "CONFIDENTIAL" in the alarm.  Remove unused
files from lab.
- Program finish times were not recorded if the program was running when the lab
was stopped.

May 21, 2018
- Fix retlibc grading to remove duplicate goal, was failing automated assessment
- Remove copies of mynotify.py from individual labs and lab template, it is 
has been part of lab\_sys/sbin, but had not been updated to reflect fixes made
for acl lab.

May 18, 2018
- Mask signal message from exec\_wrap so that segv error message looks right.
- The capinout was sometimes losing stdout, check command stdout on death of cmd.
- Fix grading of formatstring to catch segmentation fault message.
- Add type\_function feature to SimLab to type stdout of a script (see formatstring simlab). 
- Remove SimLab limitation on combining single/double quotes.
- Add window\_wait directive to SimLab to pause until window with given title
can be found.
- Modify plc lab to alter titles on physical world terminal to reflect status,
this also makes testing easier.
- Fix bufoverflow lab manual link.

May 15, 2018
- Add appendix on use of the SimLab tool to simulate user performance of labs for
regression testing and lab development.
- Add wait\_net function to SimLab to pause until selected network connections terminate.
- Change acl automated assessment to use FILE\_REGEX for multiline matching.
- SimLab test for xsite lab.

May 11, 2018
- Add "noskip" file to force collection of files otherwise found in home.tar, needed
for retrieving Firefox places.sqlite.
- Merge sqlite database with write ahead buffer before extracting.
- Corrections to lab manual for the symkeylab
- Grading additions for symkeylab and pubkey
- Improvements to simlab tool: support include, fix window naming.

May 9, 2018
- Fix parameterization of the file-deletion lab.  Correct error its lab manual.
- Replace use of shell=True in python scripts to reduce processes and allow tracking PIDs
- Clean up manuals for backups, pass-crack and macs-hash.

May 8, 2018
- Handle race condition to prevent gnome-terminal from executing its docker command
before an xterm instruction terminal runs its command.  
- Don't display errors when instuctor stops a lab started with "-d".
- Change grading of nmap-ssh to better reflect intent of the lab.
- Several document and script fixes suggested by olberger on github.

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

