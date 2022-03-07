#!/bin/bash
#
# Query docker hub regarding your current rate limit on pulling docker images.
#
json=$(curl -s "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull")
line=$(echo $json | grep -m1 token | awk '{print $3}')
token="${line:1}"
token="${token::-2}"
echo "The following describes the Docker Hub rate limits within a window defined in seconds."
echo ""
curl -s --head -H "Authorization: Bearer $token" https://registry-1.docker.io/v2/ratelimitpreview/test/manifests/latest | grep "^rate"
echo ""
echo "If your remaining ratelimit is zero, your institution has made too many docker hub pulls.  Please see https://docs.docker.com/docker-hub/download-rate-limit/ and consider requesting your institution be provided with a higher rate limit."

