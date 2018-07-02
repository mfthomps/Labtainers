#
# Labtainer Dockerfile
#
# The labtainer.base image includes the following packages:
#    build-essential  expect  file  gcc-multilib  gdb  iputils-ping  less  man  manpages-dev 
#    net-tools  openssh-client  python  sudo  tcl8.6  vim  zip  hexedit  rsyslog
#
# The labtainer.network image adds the following packages:
#   openssl openssh-server openvpn wget tcpdump  update-inetd  xinetd
#
ARG registry 
FROM $registry/labtainer.firefox
ARG lab
ARG labdir
ARG imagedir
ARG user_name 
ARG password 
ARG apt_source

ENV APT_SOURCE $apt_source
RUN /usr/bin/apt-source.sh
RUN apt-get update && apt-get install -y --no-install-recommends telnet wget lynx
ADD $labdir/$imagedir/sys_tar/sys.tar /
ADD $labdir/sys_$lab.tar.gz /

# Need pyModbusTCP to run the Modbus test program
RUN pip install pyModbusTCP

RUN useradd -ms /bin/bash $user_name
RUN echo "$user_name:$password" | chpasswd
RUN adduser $user_name sudo

USER $user_name
ENV HOME /home/$user_name

ADD $labdir/$imagedir/home_tar/home.tar $HOME
# remove after docker fixes problem with empty tars
RUN rm -f $HOME/home.tar

ADD $labdir/$lab.tar.gz $HOME
USER root
CMD ["/bin/bash", "-c", "exec /sbin/init --log-target=journal 3>&1"]
