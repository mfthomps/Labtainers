FROM mfthomps/labtainer.firefox
LABEL description="This is base Docker image for Labtainer containers with browser and a JDK"
RUN apt-get update && apt-get install -y --no-install-recommends default-jdk
