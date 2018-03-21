#
#  create a Metasploitable-2 docker image based on a tar backed up off
#  a Metasploitable-2 VM
#
FROM scratch
ADD system/msf.tar.gz /
RUN set -ex \
    && echo '' > /etc/fstab \
    && cp /sbin/init /sbin/init.real
#
# using old distribution, back in time
#
RUN sed -i.bak -r 's/us.(archive|security).ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
RUN sed -i.bak -r 's/(archive|security).ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
RUN sed -i.bak -r 's/# %sudo /%sudo /' /etc/sudoers
ADD system/etc/rc.local /etc/rc.local
ADD system/bin/funbuffer /usr/bin/
# manage default gateways
ADD system/bin/togglegw.sh /usr/bin/
ADD system/bin/set_default_gw.sh /usr/bin/
