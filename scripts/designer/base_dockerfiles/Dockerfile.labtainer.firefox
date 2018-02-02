ARG registry
FROM $registry/labtainer.base
LABEL description="This is base Docker image for Labtainer browsers"
RUN apt-get update && apt-get install -y --no-install-recommends nmap libcanberra-gtk3-module firefox sqlite3 && rm -rf /var/cache/apt/
# modified to create new instance
ADD system/bin/firefox /usr/bin/
# the firefox user profile which paramterize.sh will extract and remove.
COPY system/var/tmp/home.tar /var/tmp/
RUN systemd-machine-id-setup

