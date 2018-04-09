#!/bin/bash

. /opt/rocks/share/devel/src/roll/etc/bootstrap-functions.sh

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
compile proj
install lifemapper-proj
/sbin/ldconfig

# install tiff
compile tiff
install lifemapper-tiff
/sbin/ldconfig

# need for gdal
compile geos
install lifemapper-geos
/sbin/ldconfig

# need for modules
compile gdal
install lifemapper-gdal
/sbin/ldconfig

# for pysal, rtree
#compile setuptools
#install opt-lifemapper-setuptools

# for rtree
compile spatialindex
install lifemapper-spatialindex
/sbin/ldconfig

# for pysal
compile scipy
install opt-lifemapper-scipy

echo "You will need to checkout Lifemapper src from Github:"
echo "    cd src/lmcompute"
echo "    make prep "
echo "and download data from Lifemapper:"
echo "    cd src/lmdata-env"
echo "    make prep "
echo "finally download CCTools source code:"
echo "    cd src/cctools"
echo "    make prep "
echo "and DendroPy source code:"
echo "    cd src/dendropy"
echo "    make prep "