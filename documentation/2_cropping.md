# Cropping
The scenes are delivered with black borders that should be removed for asthetic and functional reasons.

**0)** If you manually stitched the raster: import the stitched raster using `r.import`, e.g.:
    `r.import in=DS1036-2155DF050_stitched.tif out=DS1036_stitched_raster` Note: Make sure the output name does not include `-`, otherwise `r.mapcalc` in the next step  will not work. Use the `g.rename` command if required.

**1)** Manually set the region in the GUI to the extent of the actual image (only the relevant pixels, no black border etc.):

Therefore right-click on the stitched layer --> "Display Layer" --> "Different Zoom Settings" --> "Set computational region extent interactively" --> Draw a rectangle only around the image data (leave out the black film border)

OR

Use "Display Layer" --> "Analyze Map" --> "Measure Distance" to measure the distance of the four edges of the raster to the start of actual image data, and then set the region accordingly, e.g.: `g.region n=n-4593 s=s+710 e=e-3075 w=w+12865`

**2)** Use `r.mapcalc` to recalculate the stitched raster map. Black areas (with a pixel value of 0) are recalculated to 1 to use the 0 as NoData later on: `r.mapcalc expression="DS1036_stitched_raster_calc = if(DS1036_stitched_raster == 0,1,DS1036_stitched_raster)"`

**3)** `r.mapcalc` changed the colors of the raster map - set it back to grey scale using `r.colors`.
    `r.colors map=DS1036_stitched_raster_calc color=grey255`

**4)** Run `r.info` to get the basic information about the raster that are used in the next step (rows & columns of the image):
    `r.info DS1036_stitched_raster_calc`

**5)** Use the values of the rows and columns from the previous step to reset the image coordinates of the raster map so that the image coordinate with the value 0,0 is in the lower left corner of the image. Use the rows value for `north` and the columns value for `east`:
    `r.region map=DS1036_stitched_raster_calc s=0 n=<ROWS_VALUE> w=0 e=<COLUMNS_VALUE>`

**6)** Set the region to the raster:
    `g.region raster=DS1036_stitched_raster_calc`

**7)** Export the cropped raster map as a GeoTIFF:
    `r.out.gdal -cm overviews=5 createopt="COMPRESS=LZW,PREDICTOR=2,TILED=YES" in=DS1036_stitched_raster_calc out=DS1036_stitched_raster_calc.tif`

**Continue** with the selection of GCPs in QGIS in [3_gcp_collection.md](3_gcp_collection.md)
