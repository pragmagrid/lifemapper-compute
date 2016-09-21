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
   rm -rf /state/partition1/lmcompute
   LMEXISTS=`rocks list roll | grep lifemapper | head -n1 | awk '{print $1}'
   if [ ! $LMEXISTS ]; then
      echo "Removing common data directories"
      rm -rf /state/partition1/lmscratch
      rm -rf /state/partition1/lm
   fi

   echo "Removing apache and process directories"
   rm -rf /var/run/lifemapper
  
   echo "Removing node data directories"
   rocks run host compute "rm -rf /state/partition1/lmcompute"
   rocks run host compute "rm -rf /state/partition1/lm"
   rocks run host compute "rm -rf /state/partition1/lmscratch"
   rocks run host compute "rm -rf /var/run/lifemapper"
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

# remove obsolete Lifemapper cron jobs
del-cron-jobs () {
    # only on frontend
    name1=`hostname`
    name2=`/opt/rocks/bin/rocks list host attr localhost | grep Kickstart_PublicHostname | awk '{print $3}'`
    if [ "$name1" == "$name2" ] ; then
        rm -vf  /etc/cron.daily/lm_*.cron
        rm -vf  /etc/cron.monthly/lm_*.cron
        rm -vf  /etc/cron.daily/lmcompute_*
        rm -vf  /etc/cron.monthly/lmcompute_*
        echo "Removed old cron jobs in /etc/cron.daily and /etc/cron.monthly on frontend ..." | tee -a $LOG
    fi
}

### main ###
del-opt-python 
del-lifemapper
del-directories
del-user-group
del-cron-jobs