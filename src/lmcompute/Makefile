# $Id$
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.6 (Emerald Boa)
# 		         version 6.1 (Emerald Boa)
# 
# Copyright (c) 2000 - 2013 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log$

REDHAT.ROOT = $(CURDIR)/../../

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

version.mk:
	cat ../version.mk version.mk.in > version.mk

PY.PATH = /opt/python/bin/$(PYTHONVER)

SEDSPEC += \
	-e 's%@PKGROOT@%$(PKGROOT)%g' \
	-e 's%@LMHOME@%$(LMHOME)%g' \
	-e 's%@LMUSER@%$(LMUSER)%g' \
	-e 's%@LMDISK@%$(LMDISK)%g' \
	-e 's%@PYBIN@%$(PY.PATH)%g' \
	-e 's%@VERSION@%$(VERSION)%g'

SCRIPTS = \
	config.ini \
	config-test.ini \
	submitterConfig.ini \
	layerSeeder.py \
	lmcompute.sh \
	lmcompute.csh  \
	confSysvals

config.ini: $(ARCHIVENAME)/LmCompute/config/config.ini.in
	$(SED) $(SEDSPEC) $^ > $(ARCHIVENAME)/LmCompute/config/$@
	$(SED) -i '/\[system\]/,$$d' $(ARCHIVENAME)/LmCompute/config/$@

config-test.ini: $(ARCHIVENAME)/LmCompute/config/config-test.ini.in
	$(SED) $(SEDSPEC) $^ > $(ARCHIVENAME)/LmCompute/config/$@
	$(SED) -i '/\[system\]/,$$d' $(ARCHIVENAME)/LmCompute/config/$@

submitterConfig.ini: $(ARCHIVENAME)/LmCompute/config/submitterConfig.ini.in
	$(SED) $(SEDSPEC) $^ > $(ARCHIVENAME)/LmCompute/config/$@
	$(SED) -i '/\[system\]/,$$d' $(ARCHIVENAME)/LmCompute/config/$@

layerSeeder.py: $(ARCHIVENAME)/LmCompute/scripts/layerSeeder.py.in
	$(SED) $(SEDSPEC) $^ > $(ARCHIVENAME)/LmCompute/scripts/$@
	$(SED) -i '/\[system\]/,$$d' $(ARCHIVENAME)/LmCompute/scripts/$@

confSysvals: confSysvals.in
	$(SED) $(SEDSPEC) $^ > $@

lmcompute.sh: lmcompute.sh.in
	$(SED) $(SEDSPEC) $^ > $@

lmcompute.csh: lmcompute.csh.in
	$(SED) $(SEDSPEC) $^ > $@

prepSrc.sh: prepSrc.sh.in 
	make version.mk
	$(SED) $(SEDSPEC) $^ > $@
	chmod 755 $@

prep: prepSrc.sh
	./prepSrc.sh

build: 
	tar xzvf $(NAME)-$(VERSION).tar.gz  
	make $(SCRIPTS)

install::
	mkdir -p $(ROOT)/$(PKGROOT)
	mv $(ARCHIVENAME)/*  $(ROOT)/$(PKGROOT) 

	(					\
		cd $(ROOT)/$(LMHOME)/apps; 	\
		ln -s /usr/java/latest/bin/java java; 	\
		ln -s $(PKGROOT)/bin/om_model om_model; 	\
		ln -s $(PKGROOT)/bin/om_project om_project; 	\
	)

	mkdir -p $(ROOT)/$(PKGROOT)/bin
	install -m 755 confSysvals $(ROOT)/$(PKGROOT)/bin

	mkdir -p $(ROOT)/etc/profile.d
	install -m 755 lmcompute.sh $(ROOT)/etc/profile.d
	install -m 755 lmcompute.csh $(ROOT)/etc/profile.d

clean::
	rm -rf $(SCRIPTS) 
	rm -rf version.mk prepSrc.sh
	rm -rf $(ARCHIVENAME)
