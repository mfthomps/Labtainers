FROM mfthomps/labtainer.firefox
LABEL description="This is base Docker image for Labtainer containers with browser and a JDK"
RUN apt-get install -y default-jdk
