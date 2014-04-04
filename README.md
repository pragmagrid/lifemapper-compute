LifeMapper roll
===============

This roll installs lmcompute part of LifeMapper

Installing lmCompute
---------------------

**Prerequisites**  
  * *yum base repo:* cmake, jasper, subversion, gsl, gsl-devel, sqlite-devel
  * *yum rpmforge repo:* txt2tags
  * *build rpms from source:* proj, tiff, openmodeller, gdal

  source downloads:  
    wget http://download.osgeo.org/proj/proj-4.8.0.tar.gz  
    wget http://download.osgeo.org/libtiff/tiff-4.0.3.tar.gz  
    wget http://sourceforge.net/projects/openmodeller/files/openModeller/1.3.0/libopenmodeller-src-1.3.0.tar.gz/download  
    wget http://download.osgeo.org/gdal/gdal-1.9.2.tar.gz  

**lmcompute source**  
This is a temp  distro creation till we get a versioned tarball from KU:  

    wget --no-check-certificate https://github.com/lifemapper/lmCompute/archive/master.tar.gz -O lmCompute.tar.gz  
    mkdir lifemapper  
    tar xzvf  lmCompute.tar.gz --strip=1  -C lifemapper/  
    tar czvf lifemapper.tar.gz lifemapper  
    rm -rf lifemapper lmCompute.tar.gz  

**TODO**

  * establish QUEUE_SIZE on the server and update submitterConfig.ini. Need on frontend only
  * find what other files/packages after refactoring need to be on FE or computes 
  * running jobs from KU server on compute results in : 
      Could not import: (310, rad.intersect.intersectRunner, IntersectRunner) -- No module named rtree 
      Could not import: (331, rad.randomize.randomizeRunners, RandomizeSwapRunner) -- No module named pysal 
      Could not import: (332, rad.randomize.randomizeRunners, RandomizeSplotchRunner) -- No module named pysal 
    these are frm rad pugin. 
  * manual settting LM_JOB_SERVER in /LmCompute/common/lmConstants.py. Need to change

