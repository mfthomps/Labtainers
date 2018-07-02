#
# Labtainer Dockerfile
#
#  This is the default Labtainer Dockerfile template, plesae choose the appropriate
#  base image below.
#
# The labtainer.base image includes the following packages:
#    build-essential  expect  file  gcc-multilib  gdb  iputils-ping  less  man  manpages-dev 
#    net-tools  openssh-client  python  sudo  tcl8.6  vim  zip  hexedit  rsyslog
#
# The labtainer.network image adds the following packages:
#   openssl openssh-server openvpn wget tcpdump  update-inetd  xinetd
#
ARG registry 
FROM $registry/labtainer.base
#
#  lab is the fully qualified image name, e.g., mylab.some_container.student
#  labdir is the name of the lab, e.g., mylab 
#  imagedir is the name of the container
#  user_name is the USER from the start.config, if other than ubuntu,
#            then that user must be added in this dockerfile
#            before the USER command
#
ARG lab
ARG labdir
ARG imagedir
ARG user_name
ARG apt_source
#
# Install the system files found in the _system directory
#
ADD $labdir/$imagedir/sys_tar/sys.tar /
ADD $labdir/sys_$lab.tar.gz /
#
RUN useradd -ms /bin/bash $user_name
RUN echo "$user_name:$user_name" | chpasswd
RUN adduser $user_name sudo

#
#  **** Perform all root operations, e.g.,           ****
#  **** "apt-get install" prior to the USER command. ****
#
USER $user_name
ENV HOME /home/$user_name
#
# Install files in the user home directory
#
ADD $labdir/$imagedir/home_tar/home.tar $HOME
ADD $labdir/$lab.tar.gz $HOME
RUN rm -f $HOME/home.tar
#
#  The first thing that executes on the container.
#
USER root
CMD ["/bin/bash", "-c", "exec /sbin/init --log-target=journal 3>&1"]
