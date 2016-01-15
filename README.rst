.. highlight:: rest

Lifemapper roll
===============
.. contents::

Introduction
---------------
This roll installs lmcompute part of Lifemapper on a cluster.  This is Aimee's test commit.

Installing lmCompute
---------------------

Prerequisites
~~~~~~~~~~~~~~~
This section lists all the prerequisites for lifemapper code dependencies.
The dependencies are either build from source or installed from RPMs
during the roll build.

#. RPMs from standard yum repos:

   :base:     cmake, screen, subversion, gsl, gsl-devel, sqlite-devel
   :rpmforge: hdf4, hdf4-devel, hdf5, hdf5-devel 


#. Source distributions:

   :binaries: proj, tiff, openmodeller, gdal, spatialindex
   :python modules: setuptools, scipy, numpy, pysal, rtree

Downloads
~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section is for information on some packages build dependencies. These dependencies are handled
by the bootstrap.sh

:**rtree**: setuptools, setuptools
:**pysal**: setuptools, scipy, numpy
:**gdal**:  hdf5, hdf5-devel

Required Rolls
~~~~~~~~~~~~~~~

These rolls must be installed for lifemapper roll to work  properly.

:**python**:    Python roll provides python2.7 and numpy
:**sge**:    SGE roll provides batch-queuing system for distributed resource management. 


Building a roll
------------------

Checkout roll distribution from git repo :: 

   # git clone https://github.com/pragmagrid/lifemapper.git 
   # cd lifemapper/

To build a roll, first execute a script that downloads and installs some packages
and RPMS that are prerequisites for other packages during the roll build stage: ::

   # ./bootstrap.sh  

When the script finishes, it prints the next step instruction to get the lifemapper source ::  

   # cd src/lmcompute/
   # make prep

This will produce lifemappser-X.tar.gz
The X is the revision number in lifemapper SVN. The X is recorded in version.mk.in
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
-----------------

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
   # /opt/lifemapper/rocks/bin/updateIP-lmcompute

The ``updateIP-lmcompute`` is needed for this specfic RPM because  a newly 
installed config.ini file needs template IP addressees updated. 


Adding a roll
--------------
The roll (ISO file) can be added (1) during the initial installation of the cluster (frontend)
or (2) to the existing frontend.


1 Adding a roll to a new server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#. Add the updated python roll that Nadya prepared to the frontend: ::

       # rocks add roll python*iso clean=1
       # (cd /export/rocks/install; rocks create distro)

#. To upgrade your frontend
       # rpm --nodeps -ev opt-python-27 opt-python-3
       # yum install opt-python-27 opt-python-3

#. and then re-install compute nodes or run the previous 2 commands on all compute nodes 

 
#. Add roll ISO to your existing frontend that is configured to be
   a central server. This procesdure is documented in the section ``Frontend 
   Central Server`` of `Rocks Users Guide <http://central6.rocksclusters.org/roll-documentation/base/6.1.1/>`_.

#. During the frontend install choose the lifemapper roll from the list of available rolls
   when you see ``Select Your Rolls`` screen. 

#. During the frontend install choose python  and sge rolls, they are a prerequisite for lifemapper roll.

#. If this frontend is NOT being shared with LmServer, set the attributes to point to LmWebserver and LmDbServer, 
   either FQDN or IP can be used: ::  

       # /opt/rocks/bin/rocks add host attr localhost LM_webserver value=111.222.333.444
       # /opt/rocks/bin/rocks add host attr localhost LM_dbserver value=my.host.domain 

#. Check with  : :: 

       # /opt/rocks/bin/rocks list host attr | grep LM_ 

#. Run command (only on new install, for live frontends, this happens on reboot 
   in /etc/rc.d/rocksconfig.d/post-99-lifemapper): :: 

       # /opt/lifemapper/rocks/bin/initLMcompute 

#. Install compute nodes 

2 Adding a roll to a live frontend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A roll can be added to the existing frontend.
Make sure that the python roll is installed (can be downloaded from
`Rocks Downloads <http://www.rocksclusters.org/wordpress/?page_id=80>`_ )

#. Execute all commands from top level lifemapper/ ::

   # rocks add roll lifemapper-compute-6.1-0.x86_64.disk1.iso   
   # rocks enable roll lifemapper-compute
   # (cd /export/rocks/install; rocks create distro)  
   # yum clean all
   # rocks run roll lifemapper-compute > add-roll.sh  
   # bash add-roll.sh  > add-roll.out 2>&1

#. After the  last command  is finished, examine the add-roll.out file for errors
   Set the attributes to point to LmWebserver and LmDbServer, either FQDN or IP can be used: ::  

   # /opt/rocks/bin/rocks add host attr localhost LM_webserver value=111.222.333.444
   # /opt/rocks/bin/rocks add host attr localhost LM_dbserver value=my.host.domain 

#. and then reboot your frontend to run a few initialization commands 
   (/etc/rc.d/rocksconfig.d/post-99-lifemapper, created by add-roll.sh): ::

   # reboot

#. After the frontend boots up you can rebuild the compute nodes ::  

   # rocks set host boot compute action=install
   # rocks run host compute reboot 

Where installed roll components are
------------------------------------

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
-----------------

After the roll is installed, the cluster is ready to run lifemapper jobs.  

#. Test the installation.

   As 'lmwriter' user on the frontend, execute the following command to run the 
   test script on all nodes::

        $ rocks run host compute "$PYTHON /opt/lifemapper/LmCompute/tests/scripts/testJobsOnNode.py" 2>&1 > /tmp/testJobsOnNode.log
    
#. Seed any layers already present on LmCompute instance (here with example
   30sec-present-future-SEA) by following these steps.  
   
   * Change to JOB_DATA_PATH/layers::
   
        $ cd /share/lm/data/layers

   * Uncompress the package of layers and csv file (created on LmServer by
     /opt/lifemapper/LmDbServer/populate/createScenarioPackage.py
     Step 3 of https://github.com/pragmagrid/lifemapper-server/blob/kutest/docs/Using.rst.) 
     in the JOB_DATA_PATH/layers directory on LmCompute::

        $ unzip -o 30sec-present-future-SEA.zip

     need -o option to overwrite existing tiff files. 
     
   * Populate the local Sqlite database by running the seedLayers script::

        $ $PYTHON /opt/lifemapper/LmCompute/tools/layerSeeder.py  30sec-present-future-SEAlayers.csv
        
   * Check the contents of the resulting sqlite database with:
   
        $ sqlite3 layers.db
        sqlite> select * from layers;
        
#. Register an LmServer to compute jobs for 

   Jobs are retrieved from an LmServer instance by looking at the config section 
   ``[LmCompute - Job Retrievers]`` of either the config.ini file (installed) or
   site.ini file (created, edited by user to override variables in config.ini).
    
   * Add a key to the [LmCompute - Job Retrievers] section::

        [LmCompute - Job Retrievers]
        JOB_RETRIEVER_KEYS: myJobServer

   * Add a section for the new key::

        [LmCompute - Job Retrievers - myJobServer]
        RETRIEVER_TYPE: server
        JOB_SERVER: http://myserver.pragma.org/jobs
   
#. Running lmcompute jobs

   The jobs are run on the frontend via a job submitter script.
   The script requests the jobs from the LM server and sends them to the compute nodes of the cluster.
   Execute the following commands as ``lmwriter`` user:

   * Start lm jobs via the following script: ::  

        lmwriter$ $PYTHON /opt/lifemapper/LmCompute/tools/jobMediator.py start

   * Stop jobs via the following script: :: 

        lmwriter$ $PYTHON /opt/lifemapper/LmCompute/tools/jobMediator.py stop


TODO
---------

#. automate or create a command that will specify which server to use for lmjobs
   this is done via initLMcompute script now.  
   LM_JOB_SERVER  specified in /opt/lifemapper/config/config.ini

#. Simplify steps for creating a layer package for local installation on 
   LmCompute, of input data with metadata cataloged in LmServer which will be 
   sending jobs to this LmCompute instance.  This includes creating a CSV file 
   consisting of lines of the metadataUrl from LmServer and corresponding 
   relative file location (in the layer package) 
   
#. Check that rocks-lmcompute/installCronJobs is handled properly in roll build and install 
    
#. correct permissions for /share/lm/data/layers/layers.db file

#. establish QUEUE_SIZE on the server frontend

#. Vine - needed for mounting satellite data using overlay network. This is a temp workaround.
   Vine is created as a package:  :: 

      wget http://vine.acis.ufl.edu/vine/lib/vine2.tgz -P /tmp
      tar ozxf /tmp/vine2.tgz -C /opt
      rocks create package /opt/vine2 vine2

   To install vine see rocks-lmcompute/: addVine, mountinfo. 
   Create mount points using rocks-lmcompute/addMount.

