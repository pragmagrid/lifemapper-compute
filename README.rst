.. highlight:: rest

Lifemapper roll
===============
.. contents::

Introduction
------------
This roll installs lmcompute part of Lifemapper on a cluster. 

Installing lmCompute
--------------------

Prerequisites
~~~~~~~~~~~~~
This section lists all the prerequisites for lifemapper code dependencies.
The dependencies are either build from source or installed from RPMs
during the roll build.

#. RPMs from standard yum repos:

   :base:     atlas, atlas_devel, blas, blas_devel, 
   :rpmforge: hdf5, hdf5-devel, proj


#. Source distributions:

   :non-python: cctools, gdal, geos, openmodeller, proj, tiff
   :python modules: dendropy, pyparsing, requests, scipy

Downloads
~~~~~~~~~
This section lists all the packages that were downloaded and used in the roll.
The packages are a part of the roll source (or downloaded by bootstrap.sh).

#. **sources**  ::   

    wget http://download.osgeo.org/proj/proj-4.8.0.tar.gz    
    wget http://download.osgeo.org/libtiff/tiff-4.0.3.tar.gz   
    wget http://sourceforge.net/projects/openmodeller/files/openModeller/1.3.0/libopenmodeller-src-1.3.0.tar.gz/download   
    wget http://download.osgeo.org/gdal/gdal-1.9.2.tar.gz   

#. **lmcompute source**   ::

   The lmcompute source id checked out from lifemapper SVN. Valid user/pass is required.
   
Individual package dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section is for information on some packages build dependencies. These dependencies are handled
by the bootstrap.sh

:**rtree**: setuptools, setuptools
:**pysal**: setuptools, scipy, numpy
:**gdal**:  hdf5, hdf5-devel

Required Rolls
~~~~~~~~~~~~~~

These rolls must be installed for lifemapper roll to work  properly.

:**python**:    Python roll provides python2.7 and numpy
:**sge**:    SGE roll provides batch-queuing system for distributed resource management. 


Building a roll
---------------

Checkout roll distribution from git repo :: 

   # git clone https://github.com/pragmagrid/lifemapper.git 
   # cd lifemapper/

To build a roll, first execute a script that downloads and installs some packages
and RPMS that are prerequisites for other packages during the roll build stage: ::

   # ./bootstrap.sh  

When the script finishes, it prints the next step instruction to get the 
lifemapper source and default climate data ::  

   # cd src/lmcompute/
   # make prep
   # cd src/lmdata-seed/
   # make prep

The first two instructions will produce lifemapper-X.tar.gz.  The X is the 
git tag in the lifemapper github repo. The X is recorded in version.mk.in
Assumption: X is production ready revision and is a working code.
The roll will be using the X revision of lifemapper code.

To build individual packages ::

   # cd src/pkgname 
   # make rpm 

When all individual packages are building without errors build a roll via
executing the command at the top level of the roll source tree ::

   # make roll

The resulting ISO file lifemapper-*.iso is the roll that can be added to the
frontend.

Debugging a roll
----------------

When need to update only a few packages that have changed one can rebuild only the RPMs
for changed packages and use the rest of the RPMS from the previous build. 
For example, only  rebuilding lmserver RPM will involve: ::   
  
   # cd src/lmcompute
   # make clean
   # update version.mk.in with new revision number to check out from SVN
   # make prep
   # make rpm

Install the resulting RPM with: ::   

   # rpm -el lifemapper
   # rpm -i  path-to-new-lifemapper.rpm
   # /opt/lifemapper/rocks/bin/updateCfg-lmcompute

The ``updateCfg-lmcompute`` is needed for this specfic RPM because  a newly 
installed config.lmcompute.ini file needs template IP addressees updated. 


Adding a roll
-------------
The roll (ISO file) can be added (1) during the initial installation of the cluster (frontend)
or (2) to the existing frontend.


New server pre-Lifemapper setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#. If necessary, add the updated python roll that Nadya prepared to the frontend: ::

       # rocks add roll python*iso clean=1
       # (cd /export/rocks/install; rocks create distro)

#. To upgrade your frontend
       # rpm --nodeps -ev opt-python-27 opt-python-3
       # yum install opt-python-27 opt-python-3

#. and then re-install compute nodes or run the previous 2 commands on all compute nodes 

#. Add roll ISO to your existing frontend that is configured to be
   a central server. This procedure is documented in the section ``Frontend 
   Central Server`` of `Rocks Users Guide <http://central6.rocksclusters.org/roll-documentation/base/6.2/>`_.

#. During the frontend install choose the lifemapper roll from the list of available rolls
   when you see ``Select Your Rolls`` screen. 

#. During the frontend install choose python and sge rolls, they are a prerequisite for lifemapper roll.

#. Install compute nodes 

Adding LmCompute roll to a live frontend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A roll can be added to the existing frontend.
Make sure that the python roll is installed (can be downloaded from
`Rocks Downloads <http://www.rocksclusters.org/wordpress/?page_id=80>`_ )

#. **Stop the jobMediator** as lmwriter: ::

   lmwriter$ $PYTHON /opt/lifemapper/LmCompute/tools/jobMediator.py stop

#. Execute following commands from the location of the ISO ::

   # rocks add roll lifemapper-compute-6.2-0.x86_64.disk1.iso  clean=1
   # rocks enable roll lifemapper-compute
   # (cd /export/rocks/install; rocks create distro)  
   # yum clean all
   # rocks run roll lifemapper-compute > add-compute.sh  
   # bash add-compute.sh  > add-compute.out 2>&1

#. After the  last command  is finished, examine the add-roll.out file for errors
   Set the attributes to point to LmWebserver and LmDbServer, either FQDN or IP 
   can be used. If this frontend is being shared with LmServer, set these 
   attributes to true.: ::  

   # /opt/rocks/bin/rocks add host attr localhost LM_webserver value=111.222.333.444
   # /opt/rocks/bin/rocks add host attr localhost LM_dbserver value=my.host.domain 

#. Check with  : :: 

       # /opt/rocks/bin/rocks list host attr | grep LM_ 

#. and then reboot your frontend to run a few initialization commands 
   (/etc/rc.d/rocksconfig.d/post-99-lmcompute, created by add-compute.sh): ::

   # reboot

#. After the frontend boots up, check the success of initialization commands in 
   log files in /tmp:
  * initLMcompute.log
  * installComputeCronJobs.log
  * post-99-lifemapper-lmcompute.debug 

Add input layers to the frontend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Seed the data on the frontend::

   # /opt/lifemapper/rocks/bin/transformData
   
   
Rebuild the nodes
~~~~~~~~~~~~~~~~~

#. After the frontend boots up you can rebuild the compute nodes ::  

   # rocks set host boot compute action=install
   # rocks run host compute reboot 
   
Check possible errors
~~~~~~~~~~~~~~~~~~~~~

#. **FIXME** This should work now.  If incorrect, set file permissions for  
   node scratch space and java preferences ::

   # rocks run host compute "chgrp -R lmwriter /state/partition1/lm"
   # rocks run host compute "chmod -R g+ws /state/partition1/lm" 

#. **NOTE** java preferences have moved from /opt/lifemapper/ to 
   /state/partition1/lm/.  Make sure this .java directory (and its parent) 
   has group=lmwriter and group + ws permission.

Where installed roll components are
-----------------------------------

#. Created user and group ``lmwriter``

#. **/opt/lifemapper** - prerequisites and lifemapper code

#. **/etc/ld.so.conf.d/lifemapper.conf** - dynamic linker bindings

#. **/opt/python/lib/python2.7/site-packages** - python prerequisites

#. **cmake, subversion, screen, fribidi, hdf4*, hdf5*, gsl, gsl-devel, 
   sqlite-devel** - in  usual system directories /usr/bin, /usr/lib, 
   /usr/include, etc. as required  by each RPM.  Use ``rpm -ql X`` to find all files for a package X.

#. **/state/partition1/lm/** -  mounted as /share/lm/

   /share/lm/ - jobs/,metrics/,temp/,logs/,layers/,test/


Using a Roll
------------

After the roll is installed, the cluster is ready to run lifemapper jobs.  

#. Test the installation. **This may be obsolete, CJ?**

   As 'lmwriter' user on the frontend, execute the following command to run the 
   test script on each node.  Since the nodes are currently using a shared directory,
   conflicts will arise if they try to access the same jobs at the same time. This
   will not happen during normal operations when they work on different jobs.  To
   avoid this conflict during testing, run the job on one or more nodes individually.
   Make sure to name log files uniquely if writing to the shared log directory::

        $ ssh compute-0-0
        $ $PYTHON /opt/lifemapper/LmCompute/tests/scripts/testJobsOnNode.py 2>&1 > /share/lm/logs/testJobsOnNode-0-0.log
   
   **TODO:** Move to command **lm test jobcalcs** 
            
#. **Optional** Register a different LmServer get jobs from. The default 
   configuration assumes that LmServer has been installed on this 
   same cluster.  
   
   To change this default, copy the configured values (detailed 
   below) into the site.ini file. Leave the default ``JOB_RETRIEVER_KEYS`` value,
   ``myJobServer`` and the section head ``[LmCompute - Job Retrievers - myJobServer]`` 
   in the example below, and modify the URL value for ``JOB_SERVER``.
   
   To add an additional key, add another value to the ``JOB_RETRIEVER_KEYS``
   variable, for example ``aNewJobServer``.  This will now be a comma-delimited 
   list, without spaces), then add a matching section, for example, 
   ``[LmCompute - Job Retrievers - aNewJobServer]``, filling in ``JOB_SERVER``
   with the appropriate URL.
   
   * Add a key to the [LmCompute - Job Retrievers] section::

        [LmCompute - Job Retrievers]
        JOB_RETRIEVER_KEYS: myJobServer

   * Add a section for the new key::

        [LmCompute - Job Retrievers - myJobServer]
        RETRIEVER_TYPE: server
        JOB_SERVER: http://myserver.pragma.org/jobs
        
#. Run lmcompute jobs.  **Note**: WorkQueue will replace jobMediator.

   The jobs are run on the frontend via a job submitter script.  The script 
   requests the jobs from the LM server and sends them to the compute nodes of 
   the cluster.  Execute the following commands as ``lmwriter`` user:

   * Start lm jobs via the following script: ::  

        lmwriter$ $PYTHON /opt/lifemapper/LmCompute/tools/jobMediator.py start
        
   * Test that jobs are being created and submitted with the following command. 
     Check several times to see that jobs are moving out of the queue and new
     ones are replacing them: ::
     
        lmwriter$ qstat -u lmwriter

   **TODO:** Add command **lm list worker** (to check active workers)

   **TODO:** Add command **lm test worker** (to test pre-prepared jobs, and 
   their status and movement over a short period of time)

   * Stop jobs via the following script: :: 

        lmwriter$ $PYTHON /opt/lifemapper/LmCompute/tools/jobMediator.py stop
   
   **TODO:** Move to command **lm start/stop worker** 

TODO
----
   
#. establish QUEUE_SIZE on the server frontend

#. Vine - needed for mounting satellite data using overlay network. This is a temp workaround.
   Vine is created as a package:  :: 

      wget http://vine.acis.ufl.edu/vine/lib/vine2.tgz -P /tmp
      tar ozxf /tmp/vine2.tgz -C /opt
      rocks create package /opt/vine2 vine2

   To install vine see rocks-lmcompute/: addVine, mountinfo. 
   Create mount points using rocks-lmcompute/addMount.

