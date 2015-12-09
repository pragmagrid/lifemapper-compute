#!/bin/bash

# This script removes :
#    roll-installed RPMs, 
#    created directories
#    group lmwriter

RM="rpm -evl --quiet --nodeps"

del-lifemapper() {
   echo "Removing lifemapper-* and prerequisite RPMS"
   $RM roll-lifemapper-usersguide
   $RM lifemapper-proj
   $RM lifemapper-geos
   $RM rocks-lmcompute
   $RM hdf5-devel hdf5
   $RM hdf4-devel hdf4
   $RM gsl-devel gsl
   $RM lifemapper-tiff
   $RM lifemapper-spatialindex
   $RM lifemapper-openmodeller
   $RM lifemapper-gdal
   $RM lifemapper-geos
   $RM lifemapper-lmcompute
   $RM lifemapper-seed-data
}

del-opt-python () {
   echo "Removing opt-* RPMS"
   $RM opt-lifemapper-matplotlib
   $RM opt-lifemapper-pyparsing
   $RM opt-lifemapper-dateutil
   $RM opt-lifemapper-futures
   $RM opt-lifemapper-scipy
   $RM opt-lifemapper-rtree
   $RM opt-lifemapper-pysal
}

del-directories () {
   echo "Removing /opt/lifemapper"
   rm -rf /opt/lifemapper

   echo "Removing data directories"
   rm -rf /state/partition1/lm
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
