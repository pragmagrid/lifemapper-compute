lifemapper
==========

lifemapper roll


Installing lmCompute
---------------------

This is a temp  distro creation till we get a versioned tarball from KU

  - wget --no-check-certificate https://github.com/lifemapper/lmCompute/archive/master.tar.gz -O lmCompute.tar.gz
  - mkdir lifemapper
  - tar xzvf  lmCompute.tar.gz --strip=1  -C lifemapper/
  - tar czvf lifemapper.tar.gz lifemapper
  - rm -rf lifemapper lmCompute.tar.gz

