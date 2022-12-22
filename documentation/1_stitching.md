# Stitching
The Keyhole scenes are delivered in several pieces: CORONA scenes usually in 2-4 pieces, GAMBIT in 2 pieces and HEXAGON in 4-14 pieces. These pieces are not georeferenced and must be stitched together:

**1)** Start GRASS GIS in the xy location that was created in the first step, select the mapset `PERMANENT`

**2)** import the westernmost part using `r.in.gdal` (usually *_d for CORONA, but check with the USGS earth explorer thumbnail):
   `r.in.gdal in=DS1043-2201DF006_d.tif out=DS1043-2201DF006_d`

**3)** Move the remaining parts to the correct place, while the westermost part stays the reference. For each part after the westernmost, do the following:

 * create a new mapset named after the part, e.g. *_c:
    `g.mapset -c DS1043-2201DF006_c`
 * import the part to stitch, e.g. *_c:
     `r.in.gdal in=DS1043-2201DF006_c.tif out=DS1043-2201DF006_c`
 * create an image group named after and consisting of the raster, e.g. *_c:
     `i.group group=DS1043-2201DF006_c in=DS1043-2201DF006_c`
 * In the GUI: Launch the "Georectify" dialog. source location: corona_xy,
     source mapset: *_c, e.g. DS1043-2201DF006_c. click next, keep the settings
     in the next dialog, click next, source-map: the map to be stitched, e.g. *_c in
     the corresponding mapset. target map: The previous reference map, e.g. *_d in the
     PERMANENT mapset.
 * Collect 4-8 GCPs that you find in the overlap area of the two scene pieces, e.g. four at the edge, and two within the images to compensate for rotation. Use distinct pixels.
 * Under "Georectifier Settings" --> "Georectification", make sure 1.st order is ticked
 * Tick all GCPs, and click on "Recalculate RMS error". Since we don't have a CRS,
     the unit of the errors is pixels. It should be < 1.0.
 * click on "Georectify"
 * Sometimes the writing to the PERMANENT mapset does not work, if so: copy the "rectified"
     raster to the PERMANENT mapset and if necessary rename it, e.g.:
     `g.mapset PERMANENT`
     `g.copy DS1043-2201DF006_c_georect17884@DS1043-2201DF006_c,DS1043-2201DF006_c`
 * Load the result in the GUI check if it fits. Therefore, right-click on the reference map, e.g. *_d and choose "Display layer". Then navigate in the GUI to "Layers" (at the bottom) and click "Add Raster Map" and choose the georectified raster.
 * Delete the temporary mapset in your local file system inside the grassdb
 * Repeat step **3)** for the next pieces of the scene (e.g. *_b), until all pieces have been moved to the correct position.

**4)** Run the script [raster_patch_xy.sh](../scripts/raster_patch_xy.sh). It patches the pieces together and outputs a raster in the GRASS location/mapset, as well as a GeoTiff and a .vrt with a rough georeferencing.
* modify in the script the parameters `ORDEREDLIST` (line 21) and `FLIP` (line 28) according to the respective scene. `ORDEREDLIST` has to begin with the part that was stitched last (e.g. *_a, see the comments in the script)
* run the script by passing the parameters of the scene ID and the corner coordinates:

   `bash raster_patch_xy.sh SCENEID NWLON NWLAT NELON NELAT SWLON SWLAT SELON SELAT`

   e.g.:

   `bash raster_patch_xy.sh DS1043-2201DF006 7.639 36.330 10.720 36.792 7.642 36.116 10.816 36.591`

   (latitude and longitude coordinates can be found in the attribute table of the vector map)
   Note: KH-7 Gambit scenes may be flipped by rougly 90 degrees so the coordinates passed to the script may not be correct. This however only affects the output .vrt, which is just a visual aid for GCP collection and not crucial for the process.

**Continue** with the cropping of the remaining physical film border in [2_cropping.md](2_cropping.md).
