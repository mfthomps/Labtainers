Labtainer Headless Mode
==================================

NOTE: this is a work in progress and will be refined over the next few months(summer 2020).  This is not for production, but for dev environments only at this time.

Install steps

1. Optional: rebuild the fresh-nginx:latest

`docker build -t fresh-nginx:latest .`

2. Optional: rebuild the labtainer.master. On labtainer vm, build the labtainer.master file and push it to docker hub, see instructions in labtainer.master.create.txt

3. When running docker from linux host: you will have to uncomment the following environment variable in nginx section of the docker-compose.yml file, then set a local environment variable to the local IP (real IP, not 127.0.0.1 or localhost).
  Uncomment these lines:
  
    `extra_hosts:`
    
    ` - "host.docker.internal:$DOCKER_INTERNAL_IP"`
    
then, export the environment variable as follows:

`export DOCKER_INTERNAL_IP=192.168.10.3` (be sure to use your real IP here)

This is tied to this bug in linux docker... https://github.com/docker/for-linux/issues/264

4. Then, on any linux/mac (someday windows), run the containers: 

`docker-compose up`

5. After about 30 seconds the system should settle, goto http://localhost:3333 and select "Administration Console", login (using initial credentials of admin/password). 

6. Set up realm of "myrealm". On Realm page, hover over Master realm icon in upper left corner, select "Add New" popup. Name the new realm "myrealm".  
7. From Client section on left, setup a client called "nginx" with:
* "Access Type" set to "confidential"
* "Direct Access Grants Enabled" to "on"
* "Service Accounts Enabled" to "on"
* "Authorization Enabled" to "on"
* "Root URL" as "http://localhost/"
* "Valid Redirect URIs" as "http://localhost/*"
* "Base URL" as "http://localhost/"
* "Admin URL" as "localhost"
* "Web Origins" as "localhost"

8. After saving client, using the credentials tab, copy client secret to nginx.conf (2 places) and then restart the system.

In the running shell, hit `CTRL-C` to stop the containers, then `docker-compose up` to restart them.

9. Back in Administration Console, under users section on left, create the first user and set password under credentials.

10. While you are at it, be sure to change the admin credentials of the main console.

11. Then goto http://localhost/vnc_auto.html and authenticate as that user you created in step 9.

