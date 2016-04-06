
.. hightlight:: rest

Updating an existing Lifemapper Compute installation
====================================================
.. contents::  

Introduction
------------
After the roll is installed, and the instance has been populated, and new source
code has been released, you will want to update the code and configuration (lifemapper-lmcompute*.rpm) 
and scripts (rocks-lmcompute*.rpm) without losing data.

Update roll
-----------

#. **Copy new Lifemapper roll with updated RPMs to server**, for example::

   # scp lifemapper-compute-6.2-0.x86_64.disk1.iso server.lifemapper.org:

#. **Remove old Lifemapper roll**, for example::

   # rocks remove roll lifemapper-compute
   # (cd /export/rocks/install; rocks create distro)
   # yum clean all

#. **Add a new version of the roll**, ensuring that old rpms/files are deleted::

   # rocks add roll lifemapper-compute-6.2-0.x86_64.disk1.iso clean=1
   # rocks enable roll lifemapper-compute
   # (cd /export/rocks/install; rocks create distro)
   # yum clean all
   # rocks run roll lifemapper-compute > add-compute.sh 
   # bash add-compute.sh > add-compute.out 2>&1
    
#. **Reboot front end** ::  

   # reboot
   
#. **Rebuild the compute nodes** ::  

   # rocks set host boot compute action=install
   # rocks run host compute reboot 

#. **Temporary** On EACH node fix permissions.  Note: this is run on FE by 
   script created by run roll. Commands are in lifemapper-compute-base.xml::

   # /bin/chgrp -R lmwriter /state/partition1/lm
   # /bin/chmod -R g+ws /state/partition1/lm

   # /bin/chgrp -R lmwriter /opt/lifemapper/.java
   # /bin/chmod -R g+ws /opt/lifemapper/.java


