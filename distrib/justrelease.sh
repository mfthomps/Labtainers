#!/bin/bash
#
# Create a Labtainers release.  
# --Update the release information in the README file.
# --Tag the current commit and push the release artifacts.
#
# Assumes master repo is up to date.  Will create a distribution
# from the ~/labtainerRelease directory, tag it and push
# the artifacts.
#
#
release_dir=$HOME/labtainerRelease/Labtainers
if [[ ! -d $release_dir ]]; then
    echo "No $release_dir directory found"
    exit 
fi
if [[ -z "$1" ]]; then
    tag=$(git tag | tail -n 1)
    echo "Missing tag, most recent is "$tag" .  Pick the next revision."
    exit
fi
if [[ -z "$gitpat" ]]; then
    echo "gitpat is not defined.  Source the gitpat.sh file"
    exit
fi
if [[ -z "$SSH_AGENT_PID" ]]; then
    echo "No ssh-agent running.  Source ~/agent.sh"
    exit
fi
new_tag=$1
here=`pwd`
#
# Make sure we are up to date with master
#
cd $release_dir
git checkout premaster || exit
git pull
git checkout master || exit
git pull || exit

git tag $new_tag
git push --set-upstream origin master
git push --tags

revision=$new_tag
commit=`git describe --always`
sed -i "s/^Distribution created:.*$/Distribution created: $(date '+%m\/%d\/%Y %H:%M') <\/br>/" README.md
sed -i "s/^Revision:.*$/Revision: $revision <\/br>/" README.md
sed -i "s/^Previous revision:.*$/Revision: $revision <\/br>/" README.md
sed -i "s/^Commit:.*$/Commit: $commit <\/br>/" README.md
sed -i "s/^Branch:.*$/Branch: master <\/br>/" README.md
git commit README.md -m "Update readme date/rev"
git push --set-upstream origin master

# create the end-user distibution
# First return to starting directory so we use
# possibly modified mkdist.sh
#
cd $here
./mkdist.sh -r || exit 1
#
# above mkdist occurred in a temporary directory, and the artificts were copied to the release directory
# artifacts directory
#
cd $release_dir

echo "Build GUI Jar"
cd UI/bin
./buildUI2.sh -n || exit
cp MainUI.jar $release_dir/distrib/artifacts/

echo "Build MakepackUI Jar"
cd $release_dir
cd MakepackUI/bin
./buildUI2.sh -n || exit
cp makepackui.jar $release_dir/distrib/artifacts/

echo "Build Azure tar"
cd $release_dir
cd azure
rm -f azure.tar
tar -cf azure.tar *
mv azure.tar $release_dir/distrib/artifacts

echo "Build Google tar"
cd $release_dir
cd google
rm -f google.tar
tar -cf google.tar *
mv google.tar $release_dir/distrib/artifacts

cd $release_dir/distrib
echo "Now generate release"

github-release release --security-token $gitpat --user mfthomps --repo Labtainers --tag $new_tag
echo "wait for github"
while [ -z "$(github-release info --security-token $gitpat --user mfthomps --repo Labtainers --tag $new_tag | grep releases:)" ]; do
    echo "release not yet created, sleep 2"
    sleep 2
done
echo "Upload tar"
github-release upload --security-token $gitpat --user mfthomps --repo Labtainers --tag $new_tag --name labtainer.tar --file artifacts/labtainer.tar
echo "Upload PDF zip"
github-release upload --security-token $gitpat --user mfthomps --repo Labtainers --tag $new_tag --name labtainer_pdf.zip --file artifacts/labtainer_pdf.zip
echo "Upload UI"
github-release upload --security-token $gitpat --user mfthomps --repo Labtainers --tag $new_tag --name MainUI.jar --file artifacts/MainUI.jar
github-release upload --security-token $gitpat --user mfthomps --repo Labtainers --tag $new_tag --name makepackui.jar --file artifacts/makepackui.jar
echo "Upload Azure"
github-release upload --security-token $gitpat --user mfthomps --repo Labtainers --tag $new_tag --name azure.tar --file artifacts/azure.tar
echo "Upload Google"
github-release upload --security-token $gitpat --user mfthomps --repo Labtainers --tag $new_tag --name google.tar --file artifacts/google.tar
git checkout premaster
git fetch --tags
