ARG registry 
FROM $registry/labtainer.wireshark
ARG lab
ARG labdir
ARG imagedir
ARG user_name
ARG apt_source

ENV APT_SOURCE $apt_source
RUN /usr/bin/apt-source.sh
RUN apt-get update && apt-get install -y --no-install-recommends tshark ftp

ADD $labdir/sys_$lab.tar.gz /

RUN useradd -ms /bin/bash $user_name
RUN echo "$user_name:$user_name" | chpasswd
RUN adduser $user_name sudo
USER $user_name
ENV HOME /home/$user_name
ADD $labdir/$lab.tar.gz $HOME
#
#
USER root
CMD ["/bin/bash", "-c", "exec /sbin/init --log-target=journal 3>&1"]
