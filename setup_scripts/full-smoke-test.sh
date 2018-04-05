# Assume running from setup_scripts/
#Clear out docker.
#./destroy-docker.sh

# Update baseline and framework
./update-labtainer.sh -t

# Update test sets
./update-testsets.sh
cd ../scripts/labtainer-student
smoketest.py

