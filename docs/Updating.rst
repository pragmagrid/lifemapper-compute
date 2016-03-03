
.. hightlight:: rest

Updating an existing Lifemapper Compute installation
====================================================
.. contents::  

Introduction
------------
After the roll is installed, and the instance has been populated, you may want
to update the code and configuration (in lifemapper-lmcompute*.rpm) 
and applying those changes with scripts (from rocks-lmcompute*.rpm) 
without losing data.

Update code and scripts
-----------------------

#. **Copy new Lifemapper RPMs to server**, for example lifemapper-lmcompute-xxxxx.x86_64.rpm 
     # rocks-lmcompute-6.2-0.x86_64.rpm
     
#. **Install the RPMs** as user root, then double-check that they are there: ::   

   # rpm -el lifemapper-lmcompute
   # rpm -i --force path-to-new-lifemapper-lmcompute.rpm
   # rpm -qa | grep lifemapper-lmcompute
   
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

