#!/bin/bash
if [[ -z "$1" ]]; then
    tag=$(git tag | tail -n 1)
    echo "Missing tag, most recent is "$tag" .  Pick the next revision."
    exit
fi
echo "gitpat is " $gitpat
dog=$gitpat
echo "dog " $dog
if [[ -z "$gitpat" ]]; then
    echo "gitpat is not defined.  Source the gitpat.sh file"
    exit
fi
agent=$(ps | grep ssh-agent)
if [[ -z "$agent" ]]; then
    echo "No ssh-agent running.  Source ~/agent.sh"
    exit
fi
here=`pwd`
revision=$1
commit=`git describe --always`
branch=$(git rev-parse --abbrev-ref HEAD)
sed -i "s/^Distribution created:.*$/$(date '+%m\/%d\/%Y %H:%M')/" ../README.md
sed -i "s/^Revision:.*$/Revision: $revision/" ../README.md
sed -i "s/^Commit:.*$/Commit: $commit/" ../README.md
sed -i "s/^Branch:.*$/Branch: $branch/" ../README.md
git commit ../README.md -m "Update readme date/rev"
git tag $1
git push --set-upstream origin master
git push --tags

echo "Build GUI Jar"
cd $LABTAINER_DIR/UI/bin
./buildUI2.sh || exit
cp MainUI.jar $LABTAINER_DIR/distrib/artifacts/
cd $here
echo "Now generate release"
github-release release --security-token $gitpat --user mfthomps --repo Labtainers --tag $1

echo "Upload tar"
github-release upload --security-token $gitpat --user mfthomps --repo Labtainers --tag $1 --name labtainer.tar --file artifacts/labtainer.tar
echo "Upload PDF zip"
github-release upload --security-token $gitpat --user mfthomps --repo Labtainers --tag $1 --name labtainer_pdf.zip --file artifacts/labtainer_pdf.zip
echo "Upload UI"
github-release upload --security-token $gitpat --user mfthomps --repo Labtainers --tag $1 --name MainUI.jar --file artifacts/MainUI.jar
