#!/bin/sh

# run inside GRASS
# run in the target location

qgisgcpfile="$1"
dem=$2
utmzone=$3

grassgcpfile="${qgisgcpfile}.grass"

rm -f "$grassgcpfile"

g.region rast=$dem

counter=0

# cct available ?
HAVE_CCT=`which cct`

# clean comments from input file
cat ${qgisgcpfile} | grep -v '^#' > ${qgisgcpfile}.clean


while read LINE ; do
  if [ $counter -gt 0 ] ; then
    mapX=`echo $LINE | cut -d ',' -f1`
    mapY=`echo $LINE | cut -d ',' -f2`
    pixelX=`echo $LINE | cut -d ',' -f3`
    pixelY=`echo $LINE | cut -d ',' -f4`

    # convert to utm32/31n
    if [ "$HAVE_CCT" ] ; then
      UTMCOORDS=`echo $mapX $mapY | cct -z0 -t0 +proj=utm +zone=$utmzone +datum=WGS84 +units=m`
    else
      UTMCOORDS=`echo $mapX $mapY | proj +proj=utm +zone=$utmzone +datum=WGS84 +units=m`
    fi
    mapX=`echo $UTMCOORDS | tr -s ' ' | cut -d ' ' -f1`
    mapY=`echo $UTMCOORDS | tr -s ' ' | cut -d ' ' -f2`
  
    height=`r.what map=$dem coordinates=${mapX},${mapY} | cut -d '|' -f4`

    # for i.ortho.rectify
    echo "$pixelX $pixelY 0.0    $mapX $mapY $height    1" >>"$grassgcpfile"
    # for i.rectify
    #echo "$pixelX $pixelY    $mapX $mapY    1" >>"$grassgcpfile"
  
  fi
  counter=`expr $counter + 1`
done < "$qgisgcpfile"

