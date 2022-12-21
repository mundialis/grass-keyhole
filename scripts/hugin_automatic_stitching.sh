#!/bin/sh

## Hugin based stitching

# fail immediately on error
set -e

# Requirements: 30++ GB RAM for CORONA scenes, 65++ GB RAM for GAMBIT scenes, 55++ GB RAM for HEXAGON scenes
# Ubuntu: apt-get install hugin
# Fedora: dnf install hugin

# NOTE: only a single scene per directory!

###
# variables to adjust
MISSION=$1

if [ "$MISSION" == "GAMBIT" ]; then
    BASENAME=$(basename DZ*_a.tif _a.tif)
elif [ "$MISSION" == "CORONA" ]; then
    BASENAME=$(basename DS*_a.tif _a.tif)
elif [ "$MISSION" == "HEXAGON" ]; then
    BASENAME=$(basename D3*_a.tif _a.tif)
else
    echo "Automatic stitching does not support this satellite mission."
fi

# generate Hugin project file
# Note: if there are more less scene pieces the following part has to be adjusted
if [ "$MISSION" == "GAMBIT" ]; then
    pto_gen -f 1 ${BASENAME}_b.tif ${BASENAME}_a.tif
elif [ "$MISSION" == "CORONA" ]; then
    pto_gen ${BASENAME}_d.tif ${BASENAME}_c.tif ${BASENAME}_b.tif ${BASENAME}_a.tif
elif [ "$MISSION" == "HEXAGON" ]; then
    pto_gen ${BASENAME}_f.tif ${BASENAME}_e.tif ${BASENAME}_d.tif ${BASENAME}_c.tif ${BASENAME}_b.tif ${BASENAME}_a.tif
fi

# search for GCPs
METHOD=linearmatch
if [ "$MISSION" == "GAMBIT" ]; then
    cpfind -o output_${BASENAME}.pto ${BASENAME}_b-${BASENAME}_a.pto
elif [ "$MISSION" == "CORONA" ]; then
    cpfind --$METHOD -o output_${BASENAME}.pto ${BASENAME}_d-${BASENAME}_a.pto
elif [ "$MISSION" == "HEXAGON" ]; then
    cpfind --$METHOD -o output_${BASENAME}.pto ${BASENAME}_f-${BASENAME}_a.pto
fi

# pruning GCPs
cpclean -o project_${BASENAME}.pto output_${BASENAME}.pto

# Optimising positions and geometry
autooptimiser -a -l -s -m -o project_${BASENAME}.pto project_${BASENAME}.pto

# modify panorama output parameters
if [ "$MISSION" == "GAMBIT" ]; then
pano_modify --output modify_${BASENAME}.pto --canvas=AUTO project_${BASENAME}.pto
elif [ "$MISSION" == "CORONA" ]; then
pano_modify --output modify_${BASENAME}.pto --canvas=100% --crop=AUTO project_${BASENAME}.pto
elif [ "$MISSION" == "HEXAGON" ]; then
pano_modify --output modify_${BASENAME}.pto --canvas=100% --crop=AUTO project_${BASENAME}.pto
fi

# stitching to a single TIFF
hugin_executor --stitching --prefix=stitched_${BASENAME} modify_${BASENAME}.pto
echo "Written <stitched_${BASENAME}.tif>"

echo "If needed, rotate scene by 180 degree, using:
convert stitched_${BASENAME}.tif  -rotate 180 -compress lzw stitched_${BASENAME}_flipped.tif
"

####### Alternative in GRASS GIS:

# i.points.auto
# https://grass.osgeo.org/grass7/manuals/addons/i.points.auto.html

# see Abbildung 4 in https://www.grassbook.org/wp-content/uploads/neteler/papers/neteler2005_IJG_051-061_draft.pdf
