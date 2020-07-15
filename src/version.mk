PKGROOT			= /opt/lifemapper
LMHOME			= /opt/lifemapper
LMURL			= http://yeti.lifemapper.org/dl
LMDISK			= /share/lm
# This variable is identical in the lifemapper-server roll
DATADIR_SHARED		= /share/lm/data
LMSCRATCHDISK		= /state/partition1/lmscratch
TEMPDIR			= /tmp

# Matches ENV_DATA_DIR in the lifemapper-server roll
ENV_DATA_DIR		= layers

INPUT_LAYER_DB		= layers.db
PYTHONVER		= python3.6
PYTHON36		= /opt/python/bin/$(PYTHONVER)
PYTHON36_PACKAGES	= /opt/python/lib/$(PYTHONVER)/site-packages
PGSQLVER		= 9.6
UNIXSOCKET		= /var/run/postgresql
SMTPSERVER		= localhost
SMTPSENDER		= no-reply-lifemapper@@PUBLIC_FQDN@
JAVABIN			= /etc/alternatives/java

# matplotlib dependencies
CYCLER_FILE_DEP     =   cycler-0.10.0-py2.py3-none-any.whl
DATEUTIL_FILE_DEP   =   python_dateutil-2.8.1-py2.py3-none-any.whl
KIWI_FILE_DEP       =   kiwisolver-1.2.0-cp36-cp36m-manylinux1_x86_64.whl
PYPARSING_FILE_DEP  =   pyparsing-2.4.7-py2.py3-none-any.whl

# This variable matches SCENARIO_PACKAGE in the lifemapper-server roll
SCENARIO_PACKAGE	= 10min-past-present-future

# Options are local or cluster
JOB_SUBMITTER_TYPE	= cluster
JOB_CAPACITY		= 20

# Code version
LMCODE_VERSION		= 3.4.8.p3
