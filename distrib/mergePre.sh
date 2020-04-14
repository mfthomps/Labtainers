#!/bin/bash
git push --set-upstream origin premaster || exit 1
git checkout master || exit 1
git merge premaster || exit 1
git push --set-upstream origin master || exit 1
git checkout premaster || exit 1
