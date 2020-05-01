Labtainer Headless Mode
==================================

Install steps

1. Build the fresh-nginx:latest
`docker build -t fresh-nginx:latest .`
2. On labtainer vm, build the labtainer.master file and push it to dockerhub, see instructions in labtainer.master.create.
3. Note: when running docker from linux host, you will have to uncomment the following environment variable in nginx section of the docker-compose.yml file, then set a local environment variable to the local IP (real IP, not 127.0.0.1 or localhost).
  Uncomment these lines:
    extra_hosts:
     - "host.docker.internal:$DOCKER_INTERNAL_IP"
then, export the environment variable as follows:
`export DOCKER_INTERNAL_IP=192.168.10.3` (be sure to use your real IP here)
This is tied to this bug in linux docker... https://github.com/docker/for-linux/issues/264
4. Then, on any linux/mac (someday windows), run the containers: `docker-compose up`
5. After about 30 seconds the system should settle, goto http://localhost:3333 to set up realm of "myrealm". 
6. Setup a client called "nginx" with:
* "Access Type" set to "confidential"
* "Direct Access Grants Enabled" to "on"
* "Service Accounts Enabled" to "on"
* "Authorization Enabled" to "on"
* "Root URL" as "http://localhost/"
* "Valid Redirect URIs" as "http://localhost/*"
* "Base URL" as "http://localhost/"
* "Admin URL" as "localhost"
* "Web Origins" as "localhost"
7. Copy client secret to nginx.conf and then restart the system.
8. Create the first user and set password under credentials.
9. Then goto http:\\localhost/vnc_auto.html and authenticate as that user.

