ARG registry
FROM $registry/labtainer.centos
LABEL description="This is the extended base Docker image for Labtainer CentOS images"
RUN yum install -y liberation-sans-fonts xcb-util 
RUN yum install -y http://dl.fedoraproject.org/pub/epel/6/x86_64/Packages/l/leafpad-0.8.18.1-1.el6.x86_64.rpm
RUN wget https://forensics.cert.org/cert-forensics-tools-release-el7.rpm -P /tmp
RUN  rpm -Uvh /tmp/cert-forensics-tools-release*rpm
RUN yum --enablerepo=forensics install -y ghex
ADD system/usr/share/man/man1.tar /usr/share/man
# CFS: it will end up in /usr/sbin anyway.  no idea why.  so hack up a unique waitparam.service
ADD system/sbin/waitparam.sh /usr/sbin/waitparam.sh
ADD system/lib/systemd/system/waitparam.service.cfs /lib/systemd/system/waitparam.service
RUN systemctl enable waitparam.service
