# Georectification for KH-7 (GAMBIT-1)
The final step is the rectification of the scene using GRASS commands.
Note: This readme applies only to KH-7 (GAMBIT-1). For KH-4A/KH-4B CORONA and KH-9 HEXAGON go to [4_orthorectification.md](4_orthorectification.md).

## Rectification
**1)** Launch GRASS GIS in the gambit_xy location.

**2)** Create a group in the gambit_xy location. The input raster is the stitched raster:
    `i.group group=<NAME> in=<NAME_OF_STITCHED_RASTER_MAP>`

**3)** Run i.target to target the group into the gambit UTM location:
    `i.target group=<NAME> location=gambit_utm33n mapset=PERMANENT`

**4)** Go to your local file system and manually insert the `POINTS`-file into the group-folder in the GRASS database (GRASSDATA/<LOCATIONS>/<MAPSETS>/group/<GROUP>)

**5)** Run `m.transform` to calculate the RMS of the GCPs:
    `m.transform -s group=<NAME> order=2`
(As a reference: in a first test the RMS was ~27m)


m.transform with `order=2` gives better results but requires evenly distributed GCPs; use `order=1` if evenly distributed GCPS can not be obtained

**6)** Run i.rectify to process the actual georectification:
    `i.rectify group=<NAME> extension=_rectified order=2 resolution=0.5 method=linear`


#### File Saving

**7)** Start GRASS in the location with the projection of the target UTM zone (e.g. gambit_utm33n)

**8)** Set the region to the new georectified raster, e.g.:
    `g.region raster=DZB00401700059H005001_rectified`

**9)** Round the raster back to integer:
    `r.mapcalc expression="DZB00401700059H005001_rectified_rounded = round(DZB00401700059H005001_rectified)"`

**10)** Export the result as GeoTiff.
    Since the raster is very large, activate compression, tiles, and overviews.
    `export COMPRESS_OVERVIEW="LZW"`
    `r.out.gdal -cm overviews=5 createopt="COMPRESS=LZW,PREDICTOR=2,TILED=YES,BIGTIFF=YES" in=DZB00401700059H005001_rectified_rounded out=DZB00401700059H005001.tif nodata=0`

**11)** Analyze the GeoTiff in QGIS, e.g. compare it to OSM data.
