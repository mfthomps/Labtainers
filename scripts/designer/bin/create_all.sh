#TEST_ARG=-t
#echo "Using test registry"
docker login
export DOCKER_LOGIN=YES
./create_base_image.sh
./publish_image.sh labtainer.base $TEST_ARG

./create_network_image.sh -f $TEST_ARG
./publish_image.sh labtainer.network $TEST_ARG

./create_wireshark_image.sh -f $TEST_ARG
./publish_image.sh labtainer.wireshark $TEST_ARG

./create_firefox_image.sh -f $TEST_ARG
./publish_image.sh labtainer.firefox $TEST_ARG

./create_java_image.sh -f $TEST_ARG
./publish_image.sh labtainer.java $TEST_ARG

./create_centos_image.sh $TEST_ARG
./publish_image.sh labtainer.centos $TEST_ARG

./create_lamp_images.sh -f $TEST_ARG
./publish_image.sh labtainer.lamp $TEST_ARG

