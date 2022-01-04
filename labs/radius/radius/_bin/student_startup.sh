id | grep root >>/dev/null
result=$?
if [[ $result -ne 0 ]]; then
cat << EOF
Use this command:
   radiusd -fX
to start the radius server in foreground and debug mode.
Use ctrl-C to stop the server.

Radius configuration files are in /etc/raddb
EOF
sudo su -
fi
