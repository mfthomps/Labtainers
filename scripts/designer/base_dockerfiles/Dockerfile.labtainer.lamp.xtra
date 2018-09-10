ARG registry
FROM $registry/labtainer.lamp
ADD system/etc/systemd/system/httpd.service /etc/systemd/system/
# change link to new httpd.service file
RUN systemctl disable httpd.service
RUN systemctl enable httpd.service
ADD system/sbin/waitparam.sh /sbin/waitparam.sh
ADD system/lib/systemd/system/waitparam.service.cfs /lib/systemd/system/waitparam.service
RUN systemctl enable waitparam.service
