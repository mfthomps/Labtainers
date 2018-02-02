ARG registry
FROM $registry/labtainer.network
LABEL description="This is base Docker image for Labtainer network components with wireshark"
RUN echo 'wireshark-common        wireshark-common/install-setuid boolean true' | debconf-set-selections
RUN apt-get update && apt-get install -y --no-install-recommends wireshark
RUN chmod a+x /usr/bin/dumpcap
# modified to create new instance
RUN systemd-machine-id-setup

