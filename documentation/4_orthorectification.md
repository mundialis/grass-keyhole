## Orthorectification for KH-4A/KH-4B CORONA and KH-9 HEXAGON
The final step is the rectification of the scene using GRASS commands. Note: This readme applies only to KH-4A, KH-4B (CORONA) and KH-9 (HEXAGON). For KH-7 GAMBIT go to [4_georectification.md](4_georectification.md).

For an exhaustive explanation of the underlying processing steps, see the [i.ortho.photo help](https://grass.osgeo.org/grass82/manuals/i.ortho.photo.html).


## Preparation & Rectification
**1)** Launch GRASS GIS in the corona_xy location

**2)** create a group of the raster to be orthorectified, e.g.

   `i.group group=DS1043-2201DF006 in=DS1043-2201DF006`
Note: Make sure the group name is not too long (not longer than ~20 digits), otherwise an error can occur: `buffer overflow detected`

**3)** use `i.ortho.corona` to check the GCPs and rectify the image


  Use `i.ortho.corona` as follows:

  Use the -t flag first to examine the RMS of the GCPs. If the RMS are within limits (total Reverse RMS < 25m), run i.ortho.corona without the -t flag, but use the logfile parameter to save the pointwise error statistics.

**3.1)** Estimate the RMS
   - use the `i.ortho.corona --help` command to get a better understanding of the individual parameters

   - for CORONA (KH-4A/KH-4B), the following parameters have to be adapted:
  ```
   i.ortho.corona -t group=<GROUP> grasspoints=path/to/adapted/grasspoints nw=<NW_COORDINATES> ne=<NE_COORDINATES> sw=<SW_COORDINATES> se=<SE_COORDINATES> targetdem=<DEM> targetlocmapset=<MAPSET_WITH_PROJECTION_OF_TARGET_UTM_ZONE> proj=<PROJ_STRING_WITH_UTM_ZONE> camheading=<CAMHEADING> flightdir=<FLIGHT_DIRECTION> target_res=2 memory=5000

    e.g.:
   i.ortho.corona -t group=DS1043-2201DF006 grasspoints=path/to/adapted/gcps nw=7.639,36.330 ne=10.720,36.792 sw=7.642,36.116 se=10.816,36.591 targetdem=nasadem_tun_alg_complete targetlocmapset=corona_utm32/PERMANENT proj="+proj=utm +zone=32 +datum=WGS84 +units=m" camheading=forward flightdir=south target_res=2 memory=5000
   ```
   - for HEXAGON (KH-9), the following parameters have to be adapted:
   ```
   i.ortho.corona -t group=<GROUP> grasspoints=path/to/adapted/grasspoints nw=<NW_COORDINATES> ne=<NE_COORDINATES> sw=<SW_COORDINATES> se=<SE_COORDINATES> targetdem=<DEM> targetlocmapset=<MAPSET_WITH_PROJECTION_OF_TARGET_UTM_ZONE>
   proj=<PROJ_STRING_WITH_UTM_ZONE> camheading=<CAMHEADING> flightdir=<FLIGHT_DIRECTION> target_res=1 memory=5000 focal_length=1052.4

   e.g.
   i.ortho.corona -t group=D3C1207-400442F004 grasspoints=path/to/adapted/gcps nw=7.639,36.330 ne=10.720,36.792 sw=7.642,36.116 se=10.816,36.591 targetdem=nasadem_tun_alg_complete targetlocmapset=hexagon_utm32/PERMANENT
   proj=+proj=utm +zone=32 +datum=WGS84 +units=m camheading=forward flightdir=south target_res=1 memory=5000 focal_length=1052.4
   ```
   - If the error attributed to individual GCPs is too high, deactivate them in the points file in `grassdata/corona_xy/PERMANENT/group/>GROUPNAME</CONTROL POINTS`. Change the 1 in the last column of the respective point to a 0 and rerun `i.ortho.corona -t ...`


**3.2)** Start the actual rectification and indicate the logfile

   - Uses the same command as in **3.1**, but remove -t flag and add `logfile=~/logfile` at the end of the command and add `target_res=1` for HEXAGON:

   - for CORONA (KH-4A/KH-4B):
   ```
   i.ortho.corona group=<GROUP> grasspoints=path/to/adapted/grasspoints nw=<NW_COORDINATES> ne=<NE_COORDINATES> sw=<SW_COORDINATES> se=<SE_COORDINATES> targetdem=<DEM> targetlocmapset=<MAPSET_WITH_PROJECTION_OF_TARGET_UTM_ZONE> proj=<PROJ_STRING_WITH_UTM_ZONE> camheading=<CAMHEADING> flightdir=<FLIGHT_DIRECTION> target_res=2 memory=5000 logfile=~/logfile
   ```
   - for HEXAGON (KH-9):
   ```
   i.ortho.corona group=<GROUP> grasspoints=path/to/adapted/grasspoints nw=<NW_COORDINATES> ne=<NE_COORDINATES> sw=<SW_COORDINATES> se=<SE_COORDINATES> targetdem=<DEM> targetlocmapset=<MAPSET_WITH_PROJECTION_OF_TARGET_UTM_ZONE>
   proj=<PROJ_STRING_WITH_UTM_ZONE> camheading=<CAMHEADING> flightdir=<FLIGHT_DIRECTION> target_res=1 memory=5000 focal_length=1052.4 logfile=~/logfile
   ```

Note: If the used imagery has a different scan resolution than 1432 pixels/cm, this can be adapted using the `scan_res` parameter.

`i.ortho.corona` without the `-t` flag will run the rectification and create a result raster in the indicated target location/mapset.

## File Saving

**4)** Start GRASS in the location with the projection of the target UTM zone (e.g. corona_utm32)

**5)** Set the region to the new orthorectified raster, e.g.:

   `g.region raster=DS1043-2201DF006_utm_v1`

**6)** Export the result as GeoTiff. Since the raster is very large, activate compression, tiles, and overviews.

   `export COMPRESS_OVERVIEW="LZW"`

   `r.out.gdal -cm overviews=5 createopt="COMPRESS=LZW,PREDICTOR=2,TILED=YES,BIGTIFF=YES" in=DS1043-2201DF006_utm_v1 out=DS1043_2201DF006_utm.tif nodata=0`

**7)** Analyze the GeoTiff in QGIS, e.g. compare it to OSM data.
