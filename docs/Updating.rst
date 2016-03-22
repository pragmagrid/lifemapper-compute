
.. hightlight:: rest

Updating an existing Lifemapper Compute installation
====================================================
.. contents::  

Introduction
------------
After the roll is installed, and the instance has been populated, and new source
code has been released, you will want to update the code and configuration (lifemapper-lmcompute*.rpm) 
and scripts (rocks-lmcompute*.rpm) without losing data.

Update code and scripts
-----------------------

#. **Copy new Lifemapper RPMs to server**, for example 
   lifemapper-lmcompute-xxxxx.x86_64.rpm and rocks-lmcompute-6.2-0.x86_64.rpm
     
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

  This script performs 2 functions: 
  
  - runs the updateIP-lmcompute script, which fills in the ``@*_FQDN@`` 
    variables in the LmCompute/config/config.lmcompute.ini.in file with fully 
    qualified domain name or IP address, and moves it to onfig/config.lmcompute.ini 
  - runs the installComputeCronJobs script, which installs and new or modified
    cron jobs present in the source code
  
#. **Rebuild the compute nodes** ::  

   # rocks set host boot compute action=install
   # rocks run host compute reboot 

