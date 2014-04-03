#!/bin/bash

EXCLUDE=src/RadialGWA

## # Initialization
## svn2git svn+ssh://clio.psy.vu.nl/home/r.pool/svn/GWATools --verbose --username r.pool --exclude $EXCLUDE
## git remote add origin git@github.com:rpool/GWATools.git
## git push origin master

# Sync
# git push origin master
git svn fetch
# svn2git --rebase
if [ "`grep "$EXCLUDE" .git/info/exclude`" == "" ]; then
    echo $EXCLUDE >> .git/info/exclude
fi
git add `git ls-files --others --exclude-standard`
git commit
git push origin master


exit
