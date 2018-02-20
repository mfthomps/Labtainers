#!/bin/bash
#
# Prepare a test system to use the testregistry for pulling
# labtainer images.
#
echo "10.20.200.41 testregistry" >> /etc/hosts
cat >/etc/docker/daemon.json <<EOL
{
  "insecure-registries" : ["testregistry:5000"]
}
EOL
systemctl restart docker

