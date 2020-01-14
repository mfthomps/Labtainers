docker run -d -p 5000:5000 --restart=always -e REGISTRY_HTTP_ADDR=testregistry:5000 --name registry registry:2

docker run -d \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:5001 \
  -p 5001:5001 \
  --name registry-5001 \
  registry:2

docker run -d \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:5002 \
  -p 5002:5002 \
  --name registry-5002 \
  registry:2

docker run -d \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:5003 \
  -p 5003:5003 \
  --name registry-5003 \
  registry:2
docker run -d \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:5004 \
  -p 5004:5004 \
  --name registry-5004 \
  registry:2
docker run -d \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:5005 \
  -p 5005:5005 \
  --name registry-5005 \
  registry:2
