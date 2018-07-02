ARG registry 
FROM $registry/labtainer.wireshark
ARG lab
ARG labdir
ARG imagedir
ARG apt_source
ARG user_name

#
# Give them telnetd - just in case students need to experiment
ENV APT_SOURCE $apt_source
RUN /usr/bin/apt-source.sh
RUN apt-get update && apt-get install -y --no-install-recommends tshark telnetd

ADD $labdir/sys_$lab.tar.gz /

RUN useradd -ms /bin/bash $user_name
RUN echo "$user_name:$user_name" | chpasswd
RUN adduser $user_name sudo
RUN adduser $user_name wireshark

USER $user_name
ENV HOME /home/$user_name
ADD $labdir/$lab.tar.gz $HOME

#
# the faux_init script starts the rsyslog daemon & the xinetd
#
USER root
CMD ["/bin/bash", "-c", "exec /sbin/init --log-target=journal 3>&1"]
