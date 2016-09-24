echo "This script requires that the lmdata-seed and lmcompute packages have been prepped (i.e. make prep)"
BASEDIR=/state/partition1/workspace/lifemapper-compute

declare -a easyrpms=("cctools" "dateutil" "egenix" "futures" "gdal" "geos" "lmcompute"
          "lmdata-seed" "matplotlib" "openmodeller" "proj" "pyparsing"
          "pysal" "requests" "rocks-lmcompute" "rtree" "scipy" "spatialindex" 
          "tiff" "usersguide")

for i in "${easyrpms[@]}"
do
   cd $BASEDIR/src/"$i"
   make rpm
done



