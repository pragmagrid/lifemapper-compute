#!/bin/bash

. /opt/rocks/share/devel/src/roll/etc/bootstrap-functions.sh

module unload opt-python
# download needed RPMS
yum --enablerepo base install cmake.x86_64;

# Do once for roll repo
#(cd src/RPMS; 
#yumdownloader --resolve --enablerepo base screen.x86_64; \
#yumdownloader --resolve --enablerepo base gsl.x86_64; \
#yumdownloader --resolve --enablerepo base gsl-devel.x86_64; \
#yumdownloader --resolve --enablerepo base sqlite-devel.x86_64; \
#yumdownloader --resolve --enablerepo rpmforge hdf4.x86_64; \
#yumdownloader --resolve --enablerepo rpmforge hdf4-devel.x86_64; \
#yumdownloader --resolve --enablerepo rpmforge hdf5.x86_64; \
#yumdownloader --resolve --enablerepo rpmforge hdf5-devel.x86_64; \
#)

echo "/opt/lifemapper/lib" > /etc/ld.so.conf.d/lifemapper.conf

# for gdal
rpm -i src/RPMS/hdf5*rpm
rpm -i src/RPMS/gsl*rpm 
rpm -i src/RPMS/hdf4*rpm
rpm -i src/RPMS/sqlite-devel*rpm
rpm -i src/RPMS/screen*rpm

# install proj
module load opt-python
compile proj
module unload opt-python
install lifemapper-proj
/sbin/ldconfig

# install tiff
module load opt-python
compile tiff
module unload opt-python
install lifemapper-tiff
/sbin/ldconfig

# need for gdal
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

# for pysal, rtree
#compile setuptools
#install opt-lifemapper-setuptools

# for rtree
module load opt-python
compile spatialindex
module unload opt-python
install lifemapper-spatialindex
/sbin/ldconfig

# for pysal
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