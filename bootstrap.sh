#!/bin/bash

. /opt/rocks/share/devel/src/roll/etc/bootstrap-functions.sh

# download needed RPMS
#yum --enablerepo base install cmake.x86_64;

# Do once for roll repo
#(cd src/RPMS; 

#yumdownloader --resolve --enablerepo base atlas.x86_64 atlas-devel.x86_64
#yumdownloader --resolve --enablerepo base blas.x86_64 blas-devel.x86_64
#yumdownloader --resolve --enablerepo base lapack.x86_64 lapack-devel.x86_64
#
#yumdownloader --resolve --enablerepo epel hdf5-devel.x86_64
#yumdownloader --resolve --enablerepo epel proj.x86_64
#)

echo "/opt/lifemapper/lib" > /etc/ld.so.conf.d/lifemapper.conf
/sbin/ldconfig

module unload opt-python

# for scipy
rpm -i src/RPMS/blas-3.4.2-8.el7.x86_64.rpm
rpm -i src/RPMS/blas-devel-3.4.2-8.el7.x86_64.rpm
rpm -i src/RPMS/atlas-3.10.1-12.el7.x86_64.rpm
rpm -i src/RPMS/atlas-devel-3.10.1-12.el7.x86_64.rpm
rpm -i src/RPMS/lapack-3.4.2-8.el7.x86_64.rpm
rpm -i src/RPMS/lapack-devel-3.4.2-8.el7.x86_64.rpm

# for gdal
rpm -i src/RPMS/libaec-1.0.4-1.el7.x86_64.rpm
rpm -i src/RPMS/hdf5-1.8.12-10.el7.x86_64.rpm
rpm -i src/RPMS/hdf5-devel-1.8.12-10.el7.x86_64.rpm

# for postgis
rpm -i src/RPMS/proj-4.8.0-4.el7.x86_64.rpm

# install proj, tiff, geos for gdal
cd src/proj
make prep
cd ../..
module load opt-python
compile proj
module unload opt-python
install lifemapper-proj
/sbin/ldconfig

cd src/tiff
make prep
cd ../..
module load opt-python
compile tiff
module unload opt-python
install lifemapper-tiff
/sbin/ldconfig

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