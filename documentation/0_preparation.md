# Preparation
## Operating System
The described process was developed and tested using Linux Mint 20. It is in general optimized for use with Linux. No tests on other operating systems were performed.

## Required Software
- [GRASS GIS >= v7.9](https://grasswiki.osgeo.org/wiki/Installation_Guide)
- [QGIS](https://www.qgis.org/en/site/forusers/alldownloads.html#)
- (optional): [Hugin](https://hugin.sourceforge.io/) for the automatic stitching process:
    - for Ubuntu: use `apt-get install`
            --> `apt-get install hugin`
    - for Fedora: use `dnf install`
            --> `dnf install hugin`

- GRASS GIS Addons:
    - Start GRASS GIS and install the GRASS modules [i.ortho.position](../grass_addons/i.ortho.position) and [i.ortho.corona](../grass_addons/i.ortho.corona) from this repository:
    ```
    g.extension extension=i.ortho.position url=/path/to/this/repo/grass_addons/i.ortho.position
    g.extension extension=i.ortho.corona url=/path/to/this/repo/grass_addons/i.ortho.corona
    ```
    - install the [r.in.nasadem](https://grass.osgeo.org/grass82/manuals/addons/r.in.nasadem.html) addon from the official GRASS Addons repository:
    ```
    g.extension extension=r.in.nasadem
    ```
    To use this addon, you will need a registered user account at [NASA EARTHDATA](https://urs.earthdata.nasa.gov/)


## Data preparation
**0)** Download the raw Keyhole Scene you would like to process and the vector file containing its rough extent and metadata from the USGS Earth Explorer.
- if the vector dataset is not available yet:
  - Browse https://earthexplorer.usgs.gov/ and navigate to the scene of interest using the ENTITY ID (in Step 2: "Data Sets" select Declass I for CORONA, Declass II for GAMBIT or Declass III for HEXAGON; enter the ENTITY ID in Step 3: "Additional Criteria"). Click at "Click here to export your results" (above the search results) to export a .zip-file with the vector dataset of the scene
  - Note: For some HEXAGON scenes there is no specific vector dataset that can be downloaded. Instead the .zip-file will contain footprints for all HEXAGON scenes around the world. To cut out only the desired footprint you need to open the attribute table of this dataset in e.g. QGIS, search for the desired footprint using the ENTITY ID of the scene and create a new layer that only contains this footprint. Save this layer as a vector dataset and continue at the step above.  

**1)** Launch GRASS GIS and create a GRASS xy location, e.g. corona_xy (you can name it e.g. gambit_xy for GAMBIT scenes - Note: in the walkthrough below the location is always called corona_xy)
- xy means no CRS, no georeferencing information as the original USGS scans do not have any CRS information

**2)** create a GRASS location in the projection of the target UTM zone
- example for zone 32N:
    `grass -c epsg:32632 ~/grassdata/corona_utm32n`

**3)** download/import the DEM (Note: only applies to KH-4A/KH-4B CORONA and KH-9 HEXAGON scenes)
- if the DEM is already available, import it into the UTM location using `r.import input=/path/to/the/DEM.tif output=dem_<country>`
- if no DEM is available yet:
   - import the vector dataset of the rough scene extent using `v.import`: `v.import input=/path/to/scene_extent.shp output=<scene>_extent`
   - set the region to this vector and add some km of buffer around it (due to inaccuracies of the footprints):
    `g.region vector=<scene>_extent n=n+60000 s=s-60000 w=w-60000 e=e+60000 res=30 -pa`
   - import the nasadem:
    `r.in.nasadem user=<USER> password=<PASSWORD> output=dem_<COUNTRY> memory=6000 resolution=30 method=bilinear`
Note: The NASA only provides DEMs that cover an area of the Earth that consists at least proportionally of land mass. All parts of the earth that lie in water are not covered by the DEMs. Due to the enlargement of the region by 60km, it may happen that `r.in.nasadem` wants to download DEMs that are completely in water, especially when the area of interest is a coastal region - these DEMs are not available! Consequently, `r.in.nasadem` will raise an error. In order to get the DEMs anyway, either the region in the corresponding cardinal direction must be set smaller than 60km, or the DEMs must be downloaded manually for the corresponding area under https://search.earthdata.nasa.gov/.
   - set DEM NULLs to 0 to avoid nodata in oceans:
    `r.null dem_<COUNTRY> null=0`
   - round the DEM to integer values to save disk space:
    ` r.mapcalc expression="dem_<country> = round(dem_<country>)" --o`

Note: In the walkthrough below, it is assumed that the target UTM Zone is 32N.
For other zones, this has to be adapted in steps 2_gcp_collection, 3_georectification and 3_orthorectification

**4)** collect scene specifications

A scene specification document is not required as input, but it is helpful to keep track of the processing in it.
1. Get the four approximate corner coordinates.
    - Use the scene extent vector dataset
    - OR, check the USGS earth explorer (https://earthexplorer.usgs.gov/):
        - select Dataset -> Declassifed -> declassI (for CORONA), declassII (for GAMBIT) or declassIII (for HEXAGON)
        - additional criteria: scene id
        - get metadata + browse overlay
2. Check if the image needs to be flipped --> use the USGS earth explorer thumbnails to find out
3. For CORONA and HEXAGON note the look direction of the camera:
    - It's indicated in the scene name (F for forward, A for aft)

**Continue** with the stitching of the individual scene scans in [1_stitching.md](1_stitching.md) for manual stitching or [1_automatic_stitching.md](1_automatic_stitching.md) for automatic stitching using the Hugin panorama software
