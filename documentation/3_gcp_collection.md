# GCP Collection
The collection of Ground Control Points (GCPs) is the most time-consuming step. QGIS is used here as it provides a simpler handling of the GCP collection process.

## Preparation
**1)** Launch QGIS, activate the GDAL-georeferencing plug-in (one time only). Make sure you are in EPSG:4326 (WGS84)

**2)** Load reference data:
   - OSM: e.g. use the Terrestris OSM WMS (http://ows.terrestris.de/osm/service)
   - Google Imagery: In the QGIS Browser, right click XYZ-Tiles, New Connection:
     [http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}](http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z})
   - BING Aerial: In the QGIS Browser, right click XYZ-Tiles, New Connection:
   [http://ecn.t3.tiles.virtualearth.net/tiles/a{q}.jpeg?g=1](http://ecn.t3.tiles.virtualearth.net/tiles/a{q}.jpeg?g=1)
   - ESRI World Imagery: In the QGIS Browser, add a connection to ArcGisMapServer:
     [http://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer](http://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer)

**3)** Open the Georeferencing tool
- Open the Georeferencing window ("Raster" --> "Georeferencing"). Load the newly created .tif raster (The result of [2_cropping.md](2_cropping.md))
- Inside the Georeferencing Window: Open Settings --> Configure Georeferencer --> Click "Show Georeferencer Window docked" to directly have the window of the target Raster (the .tif) under the window of your reference data which makes it easier to quickly collect the GCPs.

## GCP collection
Use the footprint that was delivered together with the scene pieces by the USGS or the .vrt-file to get a rough idea of where the scene is located.
Start collecting GCPs:
Identify a point in the target raster that you would like to have as GCP. Click at this point --> in the new window "Enter Map Coordinates" select "From Map Canvas" --> click at the same point in the reference data to set the reference GCP. Set ~20 GCPs at points where
the reference data agree well. Try to distribute the GCPs as evenly as possible across the image. Good points are street junctions, because there you can
compare OSM and imagery data. If no OSM data is available, pick points that agree in the different imagery sources, e.g. river junctions. Avoid mountain tops or ares with
steep terrain, because the imagery might be a bit shifted or distorted there.
Setting 20 GCPs for one image takes roughly 1.5 hours. Note that 20 GCPs are usually enough as the improvement in accuracy when using more GCPs is only marginal.
IMPORTANT: Manually SAVE your progress regularly by clicking "Save GCPs as". Save the
final GCPs accordingly.  

## Multiple overlapping scenes
If you have multiple scenes from the same overflight with overlapping areas, there is a possibility to rectify them more quickly than doing this for each scene individually. Therefore look at [3.1_gcps_overlapping_scenes.md](3.1_gcps_overlapping_scenes.md)

## GCP conversion
The GCPs collected in QGIS have to be adapted to be processable by GRASS, which is done by the script [gcp_qgis2grass.sh](../scripts/gcp_qgis2grass.sh)

**1)** Start GRASS in the location with the projection of the target UTM zone (e.g. corona_utm32).

**2)** Run the script passing the qgis-gcp file and the DEM as arguments, e.g.:

`bash gcp_qgis2grass.sh xyz.points dem_<country> 32`

The last argument is the UTM zone. The script outputs a GRASS-optimized GCP-file with the file-ending ".grass" next to the original file.

## For KH-7 (GAMBIT-1)
The .grass file has to be manually edited. Open the file in a Text Editor and remove each entry of z-coordinates (presumably the 3rd entry in each row). Save this file as `POINTS`.

**Continue** with the rectification in [4_orthorectification.md](4_orthorectification.md) (for CORONA or HEXAGON) or [4_georectification.md](4_georectification.md) (for GAMBIT)
