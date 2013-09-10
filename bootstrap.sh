#!/bin/bash

. /opt/rocks/share/devel/src/roll/etc/bootstrap-functions.sh

yum --enablerepo base install cmake
yum --enablerepo base install jasper
yum --enablerepo base install subversion
yum --enablerepo base install gsl
yum --enablerepo base install gsl-devel
yum --enablerepo base install sqlite-devel
yum --enablerepo rpmforge install txt2tags

echo "/opt/lifemapper/lib" > /etc/ld.so.conf.d/lifemapper.conf

compile_and_install proj
compile_and_install lifemapper-tiff
/sbin/ldconfig

compile_and_install gdal
/sbin/ldconfig
