## Overview

- i.ortho.position estimates the camera postion from the corner coordinates of the scene in longitudes and latitudes, omega and flight height.
- i.ortho.corona runs the required steps from i.ortho.photo for the orthorectification of KH-4A/B Corona and KH-9 HEXAGON scenes.

## Installation

Install these addons in GRASS GIS (https://grass.osgeo.org/) with

```
g.extension extension=i.ortho.position url=/path/to/i.ortho.position
g.extension extension=i.ortho.corona url=/path/to/i.ortho.corona
```
