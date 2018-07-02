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
FROM $registry/labtainer.base
ARG lab
ARG labdir
ARG imagedir
ARG user_name
ADD $labdir/sys_$lab.tar.gz /
RUN useradd -ms /bin/bash $user_name
RUN echo "$user_name:$user_name" | chpasswd
RUN adduser $user_name sudo

USER $user_name
ENV HOME /home/$user_name
ADD $labdir/$lab.tar.gz $HOME
USER root
CMD ["/bin/bash", "-c", "exec /sbin/init --log-target=journal 3>&1"]
