# Overview
## Summary
This repository contains GRASS GIS Addons, bash scripts, and a detailed step-by-step documentation of a GRASS GIS based georectification process of satellite images from the KEYHOLE reconnaissance missions KH-4A/B (CORONA), KH-7 (GAMBIT), and KH-9 (HEXAGON). Further background can be found [here](https://www.mundialis.de/en/georeferenzierung-von-corona-spionagesatellitendaten/).
## Repo Content
 - **documentation**: contains a detailed step-by-step guide to rectify KEYHOLE reconnaissance missions based on GRASS GIS. See [documentation/README.md](documentation/README.md) to get started.
 - **grass_addons**: contains two addons for GRASS GIS that are required for the rectification process
 - **scripts**: contains shell scripts that are required for the rectification process


 ## KEYHOLE missions overview:

 ##### KH-4A, KH-4B - CORONA

 - Panorama camera
     - -> orthorectification with panorama correction
 - Film size: 70 mm x 756.9 mm
 - flight direction seems to be south
 - in the scanned film, north is approximately up

 ##### KH-7 - GAMBIT

 - strip camera, acquired imagery in continuous lengthwise sweeps of the terrain.
     - -> orthorectification does not really work, bad geolocation
     - -> panorama correction not applicable
     - -> standard rectification
 - Film size: 9 inch (228.6 mm) x variable length
 - flight direction seems to be south
 - in the scanned film, north is approximately right

 ##### KH-9 - HEXAGON

 - Panorama camera
     -> orthorectification with panorama correction
 - flight direction seems to be south
 - in the scanned film, north is approximately up
 - focal_length: 152.4 cm

 ##### Further KEYHOLE missions

 - KH-6 Lanyard: Lanyard was a failed mission - no data with acceptable quality available
 - KH-5 Argon: ground resolution too low - irrelevant
 - KH-8 Gambit 3: no data available
