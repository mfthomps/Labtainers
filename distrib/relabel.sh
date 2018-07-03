#!/bin/bash
REGISTRY=$1
VERSION=$2
IMAGE=$3
BASE_IMAGE=$4
BASE_ID=$5

cat <<EOT > dfile
ARG registry
FROM \$registry/$IMAGE
ARG version
LABEL version=\$version
LABEL base=$BASE_IMAGE.$BASE_ID
EOT

docker build --build-arg registry=$REGISTRY --build-arg version=$VERSION \
               --pull -f dfile -t $IMAGE .

docker tag $IMAGE $REGISTRY/$IMAGE
docker push $REGISTRY/$IMAGE
docker tag $IMAGE $REGISTRY/$IMAGE:base_image$BASE_ID
docker push $REGISTRY/$IMAGE:base_image$BASE_ID
