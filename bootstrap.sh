#!/bin/bash

. /opt/rocks/share/devel/src/roll/etc/bootstrap-functions.sh

# download needed RPMS
#yum --enablerepo base install cmake.x86_64;

# Do once for roll repo
#(cd src/RPMS; 
## ??yumdownloader --resolve --enablerepo base gsl.x86_64; \
## ??yumdownloader --resolve --enablerepo base gsl-devel.x86_64; \
#yumdownloader --resolve --enablerepo base screen.x86_64; \
#yumdownloader --resolve --enablerepo epel hdf5.x86_64 hdf5-devel.x86_64; \
#yumdownloader --resolve --enablerepo epel proj.x86_64; \
#)

echo "/opt/lifemapper/lib" > /etc/ld.so.conf.d/lifemapper.conf
/sbin/ldconfig

module unload opt-python
rpm -i src/RPMS/screen*rpm

# for gdal
rpm -i src/RPMS/hdf5*rpm
# rpm -i src/RPMS/gsl*rpm 

# install proj, tiff, geos (for gdal?)
module load opt-python
compile proj
module unload opt-python
install lifemapper-proj
/sbin/ldconfig

module load opt-python
compile tiff
module unload opt-python
install lifemapper-tiff
/sbin/ldconfig

# geos for gdal
module load opt-python
compile geos
module unload opt-python
install lifemapper-geos
/sbin/ldconfig

# need for modules
module load opt-python
compile gdal
module unload opt-python
install lifemapper-gdal
/sbin/ldconfig

# # for pysal, rtree
# setuptools 36.2.7 included in /opt/python 2.7
# setuptools 20.7, needed for cherrypy build (on devapp, not in LM install)
# #compile setuptools
# module load opt-python
# (cd src/setuptools; /opt/python/bin/python2.7 setup.py install)

# spatialindex for rtree
module load opt-python
compile spatialindex
module unload opt-python
install lifemapper-spatialindex
/sbin/ldconfig

# scipy for pysal
module load opt-python
compile scipy
module unload opt-python
install opt-lifemapper-scipy

echo "You will need to download source code, data and dependencies."
echo "    lmcompute"
echo "    lmdata-env"
echo "    cctools"
echo "    dendropy"
echo "Go to each of the packages and execute:"
echo "    make prep "