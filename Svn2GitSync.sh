#!/bin/bash

## # Initialization
## svn2git svn+ssh://clio.psy.vu.nl/home/r.pool/svn/GWATools --verbose --username r.pool --exclude src/RadialGWA
## git remote add origin git@github.com:rpool/GWATools.git
## git push origin master

# Sync
# git push origin master
svn2git --rebase

exit
