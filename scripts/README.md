## Bash scripts
- `raster_patch_xy.sh`: patches the pieces together and outputs a raster in the GRASS location/mapset, as well as a GeoTiff and a .vrt with a rough georeferencing. Required in step [../documentation/1_stitching.md](../documentation/1_stitching.md)

- `hugin_automatic_stitching.sh`: automatically stitches the pieces together and outputs a 2-band-raster (1st band: image, 2nd band: alpha channel). Required in step [../documentation/1_automatic_stitching.md](../documentation/1_automatic_stitching.md)

- `gcp_qgis2grass.sh`: the GCPs collected in QGIS have to be adapted to be processable by GRASS, which is done by this script. Required in step [../documentation/3_gcp_collection.md](../documentation/3_gcp_collection.md)
