
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

#. **Add a new version of the roll**, ensuring that old rpms/files are deleted::

   # rocks add roll lifemapper-compute-6.2-0.x86_64.disk1.iso clean=1
   # rocks enable roll lifemapper-compute
   # (cd /export/rocks/install; rocks create distro)
   # yum clean all
   # rocks run roll lifemapper-compute > add-compute.sh 
   # bash add-compute.sh > add-compute.out 2>&1
    
#. **Rebuild the compute nodes** ::  

   # rocks set host boot compute action=install
   # rocks run host compute reboot 

Update code and scripts (not working)
-------------------------------------

#. **Copy new Lifemapper RPMs to server**, for example::

   # scp *.rpm  server.lifemapper.org:
     
#. **Remove the old RPMs** as user root::   

   # rpm -el lifemapper-lmcompute
   # rpm -el rocks-lmcompute
   
#. **Install the RPMs** as user root, then double-check that they are there: ::   

   # rpm -i --force path-to-new-lifemapper-lmcompute.rpm
   # rpm -i --force path-to-new-rocks-lmcompute.rpm
   # rpm -qa | grep lmcompute

#. **Temporary** (pre 1.0.9.lw; this has been added to the rocks-lmcompute "make install").
   Read the new profile file to update any environment variables::
   
     # source /etc/profile.d/lmcompute.sh
      
#. **Update your configuration** (only if you are installing the 
   lifemapper-lmcompute (Lifemapper source code) rpm), with:::
   
   # /opt/lifemapper/rocks/bin/initLMcompute

   **TODO:** Move to command **lm update config lmcompute** 

  * This script performs 3 functions: 
  
    - runs the updateIP-lmcompute script, which 
       
       * fills in the ``@*_FQDN@`` variables in the 
         LmCompute/config/config.lmcompute.ini.in file with fully 
         qualified domain name or IP address, and moves it to 
         config/config.lmcompute.ini 
       * adds system configuration info to the config.lmcompute.ini file
       * reads/sources the config.lmcompute.ini file
       
    - runs the installComputeCronJobs script, which installs and new or modified
      cron jobs present in the source code
      
#. **Update the distribution** ::

   # (cd /export/rocks/install; rocks create distro)
   # yum clean all
  
#. **Rebuild the compute nodes** ::  

   # rocks set host boot compute action=install
   # rocks run host compute reboot 

