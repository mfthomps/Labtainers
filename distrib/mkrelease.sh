#!/bin/bash
#git tag $1
#git push
#git push --tags

github-release release --security-token $gitpat --user mfthomps --repo Labtainers \
    --tag $1

github-release upload --security-token $gitpat --user mfthomps> --repo Labtainers \
    --tag $1 --name labtainer.tar --file artifacts/labtainer.tar
    --tag $1 --name labtainer_pdf.zip --file artifacts/labtiner_pdf.zip
