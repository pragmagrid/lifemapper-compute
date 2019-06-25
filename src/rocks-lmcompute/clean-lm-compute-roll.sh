#!/bin/bash

# This script removes :
#    roll-installed RPMs, 
#    created directories
#    group lmwriter

RM="rpm -evl --quiet --nodeps"
LMROLL_COUNT=`rocks list roll | grep lifemapper | wc -l`
LMUSER_COUNT=`/bin/egrep -i "^lmwriter" /etc/passwd | wc -l`

TimeStamp () {
    echo $1 `/bin/date` >> $LOG
}

set_defaults() {
    THISNAME=`/bin/basename $0`
    LOG=/tmp/$THISNAME.log
    rm -f $LOG
    touch $LOG
}

del-possible-shared-dependencies() {
   if [ $LMROLL_COUNT = 1 ]; then
      echo "Removing SHARED hdf rpms" >> $LOG
      $RM hdf4-devel hdf4
      $RM hdf5-devel hdf5
   fi
}

del-lifemapper-shared() {
   if [ $LMROLL_COUNT = 1 ]; then
      echo "Removing SHARED lifemapper-* and prerequisite RPMS" >> $LOG
      $RM lifemapper-cctools
      $RM lifemapper-gdal
      $RM lifemapper-geos
      $RM lifemapper-proj
      $RM lifemapper-tiff
      $RM lifemapper-env-data
      echo "Removing SHARED opt-* RPMS" >> $LOG
      $RM opt-lifemapper-egenix-mx-base
      $RM opt-lifemapper-requests
      $RM opt-lifemapper-dendropy
   fi
}

del-lifemapper() {
   echo "Removing lifemapper-* and prerequisite RPMS" >> $LOG
   $RM lifemapper-lmcompute
   $RM lifemapper-openmodeller
   $RM rocks-lmcompute
   $RM roll-lifemapper-usersguide
   $RM gsl-devel gsl
}

del-opt-python () {
   echo "Removing opt-* RPMS" >> $LOG
   $RM opt-lifemapper-dateutil
   $RM opt-lifemapper-futures
   $RM opt-lifemapper-matplotlib
   $RM opt-lifemapper-pyparsing
   $RM opt-lifemapper-pysal
   $RM opt-lifemapper-scipy
}

del-directories () {
   if [ $LMROLL_COUNT = 1 ]; then
      echo "Removing shared /opt/lifemapper" >> $LOG
      rm -rf /opt/lifemapper
      echo "Removing shared data directories" >> $LOG
      rm -rf /state/partition1/lmscratch
      rm -rf /state/partition1/lm
      echo "Removing shared PID directory" >> $LOG
      rm -rf /var/run/lifemapper
   fi

   echo "Removing node code, data and PID directories" >> $LOG
   rocks run host compute "rm -rf /opt/lifemapper"
   rocks run host compute "rm -rf /state/partition1/lm"
   rocks run host compute "rm -rf /state/partition1/lmscratch"
   rocks run host compute "rm -rf /var/run/lifemapper"
}

del-user-group () {
   needSync=0
   if [ $LMUSER_COUNT = 1 ] && [ $LMROLL_COUNT = 1 ]; then
       echo "Remove lmwriter user/group/dirs" >> $LOG
       userdel lmwriter
       groupdel lmwriter
       /bin/rm -f /var/spool/mail/lmwriter
       /bin/rm -rf /export/home/lmwriter
       needSync=1
   fi

   if [ "$needSync" -eq "1" ]; then
       echo "Syncing users info" >> $LOG
       rocks sync users
   fi
}

# remove obsolete Lifemapper cron jobs
del-cron-jobs () {
    # only on frontend
    name1=`hostname`
    name2=`/opt/rocks/bin/rocks list host attr localhost | grep Kickstart_PublicHostname | awk '{print $3}'`
    if [ "$name1" == "$name2" ] ; then
        echo "Remove old cron jobs in /etc/cron.daily and /etc/cron.monthly on frontend ..." >> $LOG
        rm -vf  /etc/cron.hourly/lmcompute_*
        rm -vf  /etc/cron.daily/lmcompute_*
        rm -vf  /etc/cron.monthly/lmcompute_*
    fi
}


del-automount-entry () {
    cat /etc/auto.share  | grep -v "^lm " > /tmp/auto.share.nolmcompute
    /bin/cp /tmp/auto.share.nolmcompute /etc/auto.share
}

del-roll () {
    echo
    echo "Removing roll lifemapper-compute"
    /opt/rocks/bin/rocks remove roll lifemapper-compute
    echo "Rebuilding the distro"
    (cd /export/rocks/install; rocks create distro; yum clean all)
    echo
}

check_lm_processes () {
    LMUSER_PROCESSES=`ps -Alf | grep lmwriter | grep -v grep | wc -l`
    if [ $LMUSER_PROCESSES -ne 0 ]; then
        echo "Stop all lmwriter processes before running this script"
        exit 0
    fi 
}

### main ###

check_lm_processes

set_defaults
TimeStamp "# Start"
del-lifemapper-shared
del-possible-shared-dependencies
del-opt-python 
del-lifemapper
del-directories
del-user-group
del-cron-jobs
del-automount-entry
del-roll
TimeStamp "# End"
