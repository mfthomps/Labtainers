ARG registry
FROM $registry/labtainer.centos
LABEL description="This is base Docker image for Labtainer CENTOS-hosted LAMP images"
#
RUN wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
RUN rpm -ivh mysql-community-release-el7-5.noarch.rpm
RUN yum -y update
RUN yum install -y httpd mysql-server php php-mcrypt php-mysqlnd php-xml php-gd php-mbstring mod_ssl
RUN systemctl enable httpd.service
#
