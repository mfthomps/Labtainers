#!/bin/bash
sed -i 's/^.bind-address.*$/bind-address=0.0.0.0/' /etc/my.cnf.d/server.cnf
