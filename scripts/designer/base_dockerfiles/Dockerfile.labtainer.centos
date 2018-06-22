FROM centos/systemd
LABEL description="This is base Docker image for Labtainer CENTOS images"
#
# Labtainer base image for CENTOS builds
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  
RUN sed -i '/tsflags=nodocs/d' /etc/yum.conf
RUN mkdir /var/tmp/yum.repos.d
RUN mv /etc/yum.repos.d/* /var/tmp/yum.repos.d
ADD system/etc/nps.repo /etc/yum.repos.d/CentOS-Base.repo
ADD system/bin/yum-source.sh /usr/bin/yum-source.sh
RUN yum install -y sudo rsyslog which less openssh-server openssh-clients man man-pages nano gdb file net-tools \
    python hexedit wget tcpdump nc xinetd expect tcl ghex epel-release leafpad iptables-services bind-utils dnsmasq nmap vim
RUN yum install -y python-pip
RUN sudo pip install --upgrade pip
RUN sudo pip install setuptools
RUN sudo pip install parse
RUN pip install inotify_simple
RUN pip install enum
RUN systemctl enable rsyslog
ADD system/etc/sudoers /etc/sudoers
ADD system/bin/funbuffer-8.5 /usr/bin/funbuffer
# put in /sbin so last in path search
# this is the ubuntu version, which seems to work on /dev/pts.
ADD system/bin/login /sbin/login
# manage default gateways
ADD system/bin/togglegw.sh /usr/bin/
ADD system/bin/set_default_gw.sh /usr/bin/

#
