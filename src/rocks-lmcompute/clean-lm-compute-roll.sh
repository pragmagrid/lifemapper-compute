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


del-lifemapper-shared() {
   echo "Removing shared geos, proj, tiff, and gdal dependencies RPMS" >> $LOG
   $RM libaec libaec-devel
   $RM hdf5 hdf5-devel
   
   echo "Removing SHARED lifemapper-* and prerequisite RPMS" >> $LOG	
   $RM lifemapper-cctools
   $RM lifemapper-gdal
   $RM lifemapper-geos
   $RM lifemapper-proj
   
   echo "Removing SHARED data RPMS" >> $LOG
   $RM lifemapper-env-data
   
   echo "Removing SHARED opt-* RPMS" >> $LOG
   $RM opt-lifemapper-cython
   $RM opt-lifemapper-dendropy
   $RM opt-lifemapper-egenix-mx-base
   $RM opt-lifemapper-requests
}

del-shared-directories() {
   echo "Removing lifemapper installation directory" >> $LOG
   rm -rf /opt/lifemapper
   echo "Removing shared lifemapper temp and data directories" >> $LOG
   rm -rf /state/partition1/lmscratch
   rm -rf /state/partition1/lm
   echo "Removing shared lifemapper PID directory" >> $LOG
   rm -rf /var/run/lifemapper
}

del-shared-user-group () {
   if [ $LMUSER_COUNT = 1 ] ; then
       echo "Remove lmwriter user/group/dirs" >> $LOG
       userdel lmwriter
       groupdel lmwriter
       /bin/rm -f /var/spool/mail/lmwriter
       /bin/rm -rf /export/home/lmwriter
       echo "Syncing users info" >> $LOG
       rocks sync users
   fi
}

del-lifemapper() {
   echo "Removing lifemapper prerequisite RPMS" >> $LOG
   $RM atlas atlas-devel
   $RM blas blas-devel
   $RM lapack lapack-devel
   echo "Removing lifemapper-*, opt-lifemapper-* RPMS" >> $LOG
   $RM lifemapper-lmcompute
   $RM lifemapper-openmodeller
   $RM opt-lifemapper-scipy
   $RM rocks-lmcompute
   $RM roll-lifemapper-usersguide
   $RM roll-lifemapper-compute-kickstart
}

del-node-directories () {
   echo "Removing node code, data and PID directories" >> $LOG
   rocks run host compute "rm -rf /opt/lifemapper"
   rocks run host compute "rm -rf /state/partition1/lm"
   rocks run host compute "rm -rf /state/partition1/lmscratch"
   rocks run host compute "rm -rf /var/run/lifemapper"
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

if [ $LMROLL_COUNT = 1 ]; then
	del-lifemapper-shared
	del-shared-directories
	del-shared-user-group
fi

del-lifemapper
del-node-directories
del-user-group
del-cron-jobs
del-automount-entry
del-roll

TimeStamp "# End"
