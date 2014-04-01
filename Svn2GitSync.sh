#!/bin/bash

## # Initialization
## svn2git svn+ssh://clio.psy.vu.nl/home/r.pool/svn/GWATools --verbose --username r.pool --exclude src/RadialGWA
## git remote add origin git@github.com:rpool/GWATools.git
## git push origin master

# Sync
svn2git --rebase

exit
