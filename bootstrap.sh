#!/bin/bash

. /opt/rocks/share/devel/src/roll/etc/bootstrap-functions.sh

# download needed RPMS
(cd src/RPMS; 
yumdownloader --resolve --enablerepo base cmake.x86_64; \
yumdownloader --resolve --enablerepo base subversion.x86_64; \
yumdownloader --resolve --enablerepo base screen.x86_64; \
yumdownloader --resolve --enablerepo base gsl.x86_64; \
yumdownloader --resolve --enablerepo base gsl-devel.x86_64; \
yumdownloader --resolve --enablerepo base sqlite-devel.x86_64; \
yumdownloader --resolve --enablerepo rpmforge hdf4-devel.x86_64; \
yumdownloader --resolve --enablerepo rpmforge hdf5-devel.x86_64; \
)

echo "/opt/lifemapper/lib" > /etc/ld.so.conf.d/lifemapper.conf

compile_and_install proj
compile_and_install lifemapper-tiff
/sbin/ldconfig

compile_and_install gdal
/sbin/ldconfig
