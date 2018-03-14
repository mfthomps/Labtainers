docker run -d -p 5000:5000 --restart=always -e REGISTRY_HTTP_ADDR=testregistry:5000 --name registry registry:2
