LMBASE		= /opt/lifemapper
PKGROOT		= /opt/lifemapper/LmCompute
LMDISK          = /share/lm
NAME        	= lifemapper-lmcompute
PKGNAME         = LmCompute
#INSTDIR		= LmCompute
VERSION     	= 1.0
RELEASE 	= 0
TARBALL_POSTFIX	= tar.gz

PYBIN           = /opt/python/bin/python2.7
LMUSER          = pragma,lm2

DIST            = 20140314

RPM.EXTRAS = %define __os_install_post %{nil}

