PKGROOT       = /opt/lifemapper
LMHOME        = /opt/lifemapper
MAPSERVER_TMP = /var/www/tmp
LMWEB         = /var/lib/lm2
LMURL			  = http://lifemapper.org/dl
DATADIR_COMPUTE   = /share/lm/data
# TODO: 
# DATADIR_COMPUTE   = /share/lmcompute/data

# This variable is identical in the lifemapper-server roll
DATADIR_SHARED  = /share/lm/data

# This variable is identical to ENV_DATA_DIR in the lifemapper-server roll
INPUT_LAYER_DIR   = layers

INPUT_LAYER_DB    = layers.db
TEMPDIR       = /tmp
PYTHONVER     = python2.7
PGSQLVER      = 9.1
LMDISK        = /share/lm
LMSCRATCHDISK    = /state/partition1/lmscratch
UNIXSOCKET    = /var/run/postgresql
SMTPSERVER    = localhost
SMTPSENDER    = no-reply-lifemapper@@PUBLIC_FQDN@
JAVABIN       = /usr/java/latest/bin/java

SCENARIO_PACKAGE_SEED    = 10min-past-present-future

# Options are local or cluster
JOB_SUBMITTER_TYPE  = cluster
JOB_CAPACITY		  = 20
