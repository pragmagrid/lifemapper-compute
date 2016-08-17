#!/bin/bash

# This script removes :
#    roll-installed RPMs, 
#    created directories
#    group lmwriter

RM="rpm -evl --quiet --nodeps"

del-lifemapper() {
   echo "Removing lifemapper-* and prerequisite RPMS"
   $RM lifemapper-cctools
   $RM lifemapper-gdal
   $RM lifemapper-geos
   $RM lifemapper-lmcompute
   $RM lifemapper-openmodeller
   $RM lifemapper-proj
   $RM lifemapper-seed-data
   $RM lifemapper-spatialindex
   $RM lifemapper-tiff
   $RM rocks-lmcompute
   $RM roll-lifemapper-usersguide
   $RM hdf5-devel hdf5
   $RM hdf4-devel hdf4
   $RM gsl-devel gsl
}

del-opt-python () {
   echo "Removing opt-* RPMS"
   $RM opt-lifemapper-dateutil
   $RM opt-lifemapper-egenix-mx-base
   $RM opt-lifemapper-futures
   $RM opt-lifemapper-matplotlib
   $RM opt-lifemapper-pyparsing
   $RM opt-lifemapper-pysal
   $RM opt-lifemapper-requests
   $RM opt-lifemapper-rtree
   $RM opt-lifemapper-scipy
}

del-directories () {
   echo "Removing /opt/lifemapper"
   rm -rf /opt/lifemapper

   echo "Removing frontend data directories"
   rm -rf /state/partition1/lm
   rm -rf /state/partition1/lmscratch

   echo "Removing node data directories"
   rocks run host compute "rm -rf /state/partition1/lm"
   rocks run host compute "rm -rf /state/partition1/lmscratch"
}

del-user-group () {
   needSync=0
   /bin/egrep -i "^lmwriter" /etc/passwd
   if [ $? -ne 0 ]; then
       echo "Remove group lmwriter"
       groupdel lmwriter
       needSync=1
   fi

   if [ "$needSync" -eq "1" ]; then
       echo "Syncing users info"
       rocks sync users
   fi
}

### main ###
del-opt-python 
del-lifemapper
del-directories
del-user-group
