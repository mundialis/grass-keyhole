#!/bin/bash

# patch different parts of a CORONA scene together
# the order of patching must match the order of alignment
# i.e. if map a is in the display on top of map b
# the order must be map a, map b

# variables to adjust

SCENEID=$1
NWLON=$2
NWLAT=$3
NELON=$4
NELAT=$5
SWLON=$6
SWLAT=$7
SELON=$8
SELAT=$9
# odered list assuming a on top of b (on top of c on top of d)
# 4 image parts
ORDEREDLIST="${SCENEID}_a,${SCENEID}_b,${SCENEID}_c,${SCENEID}_d"
# 2 image parts
#ORDEREDLIST="${SCENEID}_a,${SCENEID}_b"

# set FLIP to non-zero if the image needs to be
# flipped top-bottom and left-right
# applies to KH-4A aft
FLIP=0

# nothing to change below
export GRASS_OVERWRITE=1

g.region -pa res=1 rast=$ORDEREDLIST
r.patch in=$ORDEREDLIST out=${SCENEID}_patch

south=0
west=0
eval `r.info -g ${SCENEID}_patch`

if [ "$south" != "0" ] ; then
  # invert sign
  if [ "${south:0:1}" = "-" ] ; then
    south="+${south:1}"
  else
    south="-${south}"
  fi
  r.region map=${SCENEID}_patch n=n$south s=s$south
fi

if [ "$west" != "0" ] ; then
  # invert sign
  if [ "${west:0:1}" = "-" ] ; then
    west="+${west:1}"
  else
    west="-${west}"
  fi
  r.region map=${SCENEID}_patch w=w$west e=e$west
fi

g.region rast=${SCENEID}_patch
r.mapcalc "\"${SCENEID}_zero\" = if(isnull(\"${SCENEID}_patch\"), 0, \"${SCENEID}_patch\")"
g.remove rast name=${SCENEID}_patch -f

if [ $FLIP -ne 0 ] ; then
  r.flip -b in=${SCENEID}_zero out=${SCENEID}
  g.remove rast name=${SCENEID}_zero -f
else
  g.rename rast=${SCENEID}_zero,${SCENEID}
fi

r.out.gdal -cm overviews=4 createopt="COMPRESS=DEFLATE,PREDICTOR=2,TILED=YES,BIGTIFF=YES" in=${SCENEID} out=${SCENEID}.tif

# get rows and cols from r.info
eval $(r.info -g map=$SCENEID)

# GDAL counts rows from top to bottom:
# upper left (ul): 0 0
# lower left (ll): 0 nrows
# upper right (ur): ncols 0
# lower right (lr): ncols nrows

# KH-4A:
# GDAL ul = NW
# GDAL ll = SW
# GDAL ur = NE
# GDAL lr = SE

# KH-7:
# GDAL ul = SW
# GDAL ll = SE
# GDAL ur = NW
# GDAL lr = NE

# run gdal_translate
gdal_translate -of VRT -a_srs EPSG:4326 \
               -gcp 0 0 $NWLON $NWLAT \
               -gcp 0 $rows $SWLON $SWLAT \
               -gcp $cols 0 $NELON $NELAT \
               -gcp $cols $rows $SELON $SELAT ${SCENEID}.tif ${SCENEID}.vrt
