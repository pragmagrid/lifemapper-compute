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

REDHAT.ROOT = $(CURDIR)/../../

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

PY.PATH = /opt/python/bin/$(PYTHONVER)
MAINTENANCE.PATH = $(PKGROOT)/LmCompute/scripts
APPS.PATH = $(PKGROOT)/LmCompute/apps

version.mk:
	cat ../version.mk version.mk.in > version.mk

SEDSPEC += \
	-e 's%@PKGROOT@%$(PKGROOT)%g' \
	-e 's%@LMHOME@%$(LMHOME)%g' \
	-e 's%@LMUSER@%$(LMUSER)%g' \
	-e 's%@LMDISK@%$(LMDISK)%g' \
	-e 's%@PYBIN@%$(PY.PATH)%g' \
	-e 's%@VERSION@%$(VERSION)%g'

PROFILES = \
	lmcompute.sh \
	lmcompute.csh 

SCRIPTS = \
	lifemapper.conf
	
LMAPPS = \
	maintenance-cleanup-jobs-rocks
	maintenance-aggregate-logs
	maintenance-free-memory-rocks
	lmJobScript
	lmMaxent
	maxent.bat
	

PROGS = \
	updateIP-lmcompute \
	confSysvals \
	seedLayers \
	installCronJobs

lmcompute.sh: lmcompute.sh.in
	$(SED) $(SEDSPEC) $^ > $@

lmcompute.csh: lmcompute.csh.in
	$(SED) $(SEDSPEC) $^ > $@

updateIP-lmcompute: updateIP-lmcompute.in
	$(SED) $(SEDSPEC) $^ > $@

confSysvals: confSysvals.in
	$(SED) $(SEDSPEC) $^ > $@

lifemapper.conf: lifemapper.conf.in
	$(SED) $(SEDSPEC) $^ > $@

seedLayers: seedLayers.in
	$(SED) $(SEDSPEC) $^ > $@

installCronJobs: installCronJobs.in
	$(SED) $(SEDSPEC) $^ > $@

maintenance-aggregate-logs: $(MAINTENANCE.PATH)/maintenance-aggregate-logs.in
	$(SED) $(SEDSPEC) $^ > $@

maintenance-cleanup-jobs-rocks: $(MAINTENANCE.PATH)/maintenance-cleanup-jobs-rocks.in
	$(SED) $(SEDSPEC) $^ > $@

maintenance-free-memory-rocks: $(MAINTENANCE.PATH)/maintenance-cleanup-jobs-rocks.in
	$(SED) $(SEDSPEC) $^ > $@

lmJobScript: $(MAINTENANCE.PATH)/lmJobScript.in
	$(SED) $(SEDSPEC) $^ > $@

lmMaxent: $(APPS.PATH)/maxent.in
	$(SED) $(SEDSPEC) $^ > $@

maxent.bat: $(APPS.PATH)/maxent.bat.in
	$(SED) $(SEDSPEC) $^ > $@

build: $(SCRIPTS) $(PROFILES) $(PROGS) $(LMAPPS)
	
install::

	mkdir -p $(ROOT)/etc/profile.d
	install -m 755 $(PROFILES) $(ROOT)/etc/profile.d

	mkdir -p $(ROOT)/$(PKGROOT)/rocks/bin
	install -m 755 $(PROGS) $(ROOT)/$(PKGROOT)/rocks/bin
	install -m 755 initLMcompute $(ROOT)/$(PKGROOT)/rocks/bin
	install -m 755 addMount addVine $(ROOT)/$(PKGROOT)/rocks/bin
	install -m 755 installCronJobs $(ROOT)/$(PKGROOT)/rocks/bin
	install -m 755 $(LMAPPS) $(ROOT)/$(PKGROOT)/rocks/bin

	mkdir -p $(ROOT)/$(PKGROOT)/rocks/etc
	install -m 644 mountinfo $(ROOT)/$(PKGROOT)/rocks/etc
	install -m 644 layerPairs.csv $(ROOT)/$(PKGROOT)/rocks/etc

	mkdir -p $(ROOT)/etc/ld.so.conf.d
	install -m 644 lifemapper.conf $(ROOT)/etc/ld.so.conf.d

clean::
	rm -rf version.mk $(SCRIPTS) $(PROFILES) $(PROGS) $(LMAPPS)
