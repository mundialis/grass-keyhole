# CORONA / HEXAGON / GAMBIT processing overview
This directory contains detailed READMEs for each step of the rectification process. See below for a short description:

- [0_preparation.md](0_preparation.md): setup of required software and data
- [1_stitching.md](1_stitching.md): stitching of the 2 (or more) partial GeoTIFF scenes into one single GeoTIFF (applicable for CORONA; HEXAGON and GAMBIT scenes)
    OR
- [1_automatic_stitching.md](1_automatic_stitching.md): automatic stitching for CORONA and HEXAGON scenes with a maximum of 4-5 scene pieces (scenes with more pieces will need >60GB RAM)
- [2_cropping.md](2_cropping.md): crop the raster to an extent where only relevant image pixels are left and residual pixels from the physical film scan are removed
- [3_gcp_collection.md](3_gcp_collection.md): identification of GCPs between unrectified scene and reference data
- [3.1_gcps_overlapping_scenes.md](3.1_gcps_overlapping_scenes.md): additional hints for GCP collection of an entire swath of scenes
- [4_orthorectification.md](4_orthorectification.md): orthorectification of CORONA and HEXAGON scenes (incl. correction of panoramic distortion)
- [4_georectification.md](4_georectification.md): georectification of GAMBIT scenes (no correction of panoramic distortion required)
