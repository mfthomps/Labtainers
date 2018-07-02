# onewayhash
ARG registry 
FROM $registry/labtainer.base
ARG lab
ARG labdir
ARG imagedir
ARG apt_source
ARG user_name
ARG password
ENV APT_SOURCE $apt_source
RUN /usr/bin/apt-source.sh
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssl \
    openssh-client
RUN apt-get install -y \
    hexedit
ADD $labdir/sys_$lab.tar.gz /

RUN useradd -ms /bin/bash $user_name
RUN echo "$user_name:$password" | chpasswd
RUN adduser $user_name sudo
USER $user_name
ENV HOME /home/$user_name
ADD $labdir/$lab.tar.gz $HOME
#ENTRYPOINT sudo /sbin/faux_init && bash
USER root
CMD ["/bin/bash", "-c", "exec /sbin/init --log-target=journal 3>&1"]
