export TEST_REGISTRY=NO
./create_base_image.sh
./publish_image.sh labtainer.base

./create_network_image.sh
./publish_image.sh labtainer.network

./create_wireshark_image.sh
./publish_image.sh labtainer.wireshark

./create_firefox_image.sh
./publish_image.sh labtainer.firefox

./create_java_image.sh
./publish_image.sh labtainer.java

#./create_centos_image.sh
#./publish_image.sh labtainer.centos

#./create_lamp_images.sh
#./publish_image.sh labtainer.lamp

