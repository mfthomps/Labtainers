#
# Create a master Labtainer image for use in running Labtainers from a container
# on any system that has Docker installed, withou having to install Labtainers.
# Thanks for Olivier Berger for this contribution.
#
FROM ubuntu:xenial
LABEL description="This is Docker image for the Labtainers master controller"
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
    
# 
ARG DOCKER_GROUP_ID
RUN groupadd -g $DOCKER_GROUP_ID docker

# 
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get install -y --no-install-recommends docker-ce

# Set the locale
RUN  apt-get install -y --no-install-recommends \
    locales
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  
# RUN sudo pip install --upgrade pip
# RUN sudo pip install setuptools
# RUN sudo pip install parse
# RUN pip install inotify_simple
# RUN pip install enum
# ADD system/etc/sudoers /etc/sudoers
# ADD system/etc/rc.local /etc/rc.local
# ADD system/bin/funbuffer /usr/bin/
# # manage default gateways
# ADD system/bin/togglegw.sh /usr/bin/
# ADD system/bin/set_default_gw.sh /usr/bin/

RUN  apt-get install -y --no-install-recommends \
    python \
    python-pip \
    python-setuptools
RUN pip install netaddr parse python-dateutil

RUN  apt-get install -y --no-install-recommends \
     x11-xserver-utils \
     xterm \
     gnome-terminal

RUN  apt-get install -y --no-install-recommends \
     less \
     iputils-ping

# For gnome-terminal
RUN  apt-get install -y --no-install-recommends \
     dbus-x11

RUN useradd -ms /bin/bash labtainer
RUN usermod -aG docker labtainer

USER labtainer
WORKDIR /home/labtainer

COPY --chown=labtainer:labtainer labtainer.tar /home/labtainer
RUN tar xf labtainer.tar
RUN rm labtainer.tar
RUN cd labtainer && ln -s trunk/scripts/labtainer-student
RUN cd labtainer && ln -s trunk/scripts/labtainer-instructor

COPY --chown=labtainer:labtainer bashrc.labtainer.master /home/labtainer
RUN cat bashrc.labtainer.master >>/home/labtainer/.bashrc

COPY --chown=labtainer:labtainer labutils.py /home/labtainer/labtainer/labtainer-student/bin/

ENV DISPLAY :0
