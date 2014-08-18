.. hightlight:: rest

LifeMapper roll
===============
.. contents::

Introduction
---------------
This roll installs lmcompute part of Lifemapper on a cluster. 

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

Required rolls must be added at the same time when the  lifemapper-server roll is isntalled.
See ``Adding a roll`` section for details.

:**python**:    Python roll provides python2.7 and numpy


Building a roll
------------------

Checkout roll distribution from git repo :: 

   # git clone https://github.com/pragmagrid/lifemapper.git 
   # cd lifemapper/

To build a roll, first execute a script that downloads and installs some packages
and RPMS that are prerequisites for other packages during the roll build stage: ::

   # ./bootstrap.sh  

When the scirpt finishes, it prints the next step instruction to get the lifemapper source ::  

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

Adding a roll
--------------
The roll (ISO file) can be added (1) during the initial installation of the cluster (frontend)
or (2) to the existing frontend.


1 Adding a roll to a new server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Add roll ISO to your existing frontend that is configured to be
   a central server. This procesdure is documented in the section ``Frontend 
   Central Server`` of `Rocks Users Guide <http://central6.rocksclusters.org/roll-documentation/base/6.1.1/>`_.

#. During the frontend install choose the lifemapper-server roll from the list of available rolls
   when you see ``Select Your Rolls`` screen.

#. During the frontend install choose python roll, it is a prerequisite for lifemapper roll.

2 Adding a roll to a live frontend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A roll can be added to the existing frontend.
Make sure that the python roll is installed (can be downloaded from
`Rocks Downloads <http://www.rocksclusters.org/wordpress/?page_id=80>`_ )

Execute all commands from top level lifemapper-server/ ::

   # rocks add roll lifemapper-6.1-0.x86_64.disk1.iso   
   # rocks enable roll lifemapper
   # (cd /export/rocks/install; rocks create distro)  
   # yum clean all
   # rocks run roll lifemapper > add-roll.sh  
   # bash add-roll.sh  > add-roll.out 2>&1

After the  last command  is finished, examine the add-roll.out file for errors
and then reboot your frontend: ::

   # reboot

The reboot is needed to run a few initialization commands.
After the frontend boots up you can rebuild the compute nodes ::  

   # rocks set host boot compute action=install
   # rocks run host compute reboot 

Where installed roll components are
------------------------------------

#. Created group ``lmwriter``

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
Currently, KU is setup as a default jobs server. See TODO 


TODO
---------

#. automate or create a command that will specify wich server to use for lmjobs

#. correct permissions for /share/lm/data/layers/layers.db file





**TODO**
  * establish QUEUE_SIZE on the server and update submitterConfig.ini. Need on frontend only
  * find what other files/packages after refactoring need to be on FE or computes 
  * running jobs from KU server on compute results in errors from rad plugin: 

          Could not import: (310, rad.intersect.intersectRunner, IntersectRunner) -- No module named rtree 
          Could not import: (331, rad.randomize.randomizeRunners, RandomizeSwapRunner) -- No module named pysal 
          Could not import: (332, rad.randomize.randomizeRunners, RandomizeSplotchRunner) -- No module named pysal 
          
  * manual settting LM_JOB_SERVER in /LmCompute/common/lmConstants.py. Need to change

Running lmcompute jobs
-----------------------

The jobs are run on the frontend via a job submitter script.
The scirpt requests the jobs from the LM server and sends them to the compute nodes of the cluster.

  * The environment is set via /etc/init.d/lmcompute.sh
  * Need to set a correct jobs server LM_JOB_SERVER  specified in /opt/lifemapper/LmCompute/common/lmConstants.py
  * Start lm jobs via the following script:

        #!/bin/bash  
        rm -rf /share/lm/logs/submitter.die  
        screen  
        bash $LM_SCRIPTS_PATH/startLifemapper.sh  

* Stop jobs via the following script:

        #!/bin/bash
        touch /share/lm/logs/submitter.die

