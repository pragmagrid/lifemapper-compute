PKGROOT		= /opt/lifemapper
LMDISK          = /share/lm
NAME        	= lifemapper
PKGNAME         = lmCompute
INSTDIR		= lm
VERSION     	= 1.0
RELEASE 	= 0
TARBALL_POSTFIX	= tar.gz

PYBIN          = /opt/python/bin/python
LMUSER           = pragma,lm2

RPM.EXTRAS = %define __os_install_post %{nil}

