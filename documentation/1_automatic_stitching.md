# Automatic Stitching
The Keyhole scenes are delivered in several pieces: CORONA scenes usually in 2-4 pieces, GAMBIT in 2 pieces and HEXAGON in 4-14 pieces. These pieces are not georeferenced and must be stitched together.

Automatic stitching is successfully tested for CORONA (KH-4A/KH-4B) scenes, GAMBIT 1 (KH-7) scenes and HEXAGON (KH-9) scenes with a maximum of 4 pieces. Scenes with a very high proportion of undifferentiable land cover (>80%), e.g. deserts or ocean, or scenes with poor image quality may not be successfully stitched.
Automatic stitching is particularly suitable for scenes that can also be easily stitched manually and scenes that do not have clearly identifiable infrastructure but do have clearly recognisable land structures such as rock formations.

The automatic stitching is processed with [Hugin](https://hugin.sourceforge.io/).


## Requirements

- 30++ GB RAM for CORONA scenes
- 55++ GB RAM for HEXAGON scenes
- 65++ GB RAM for GAMBIT scenes

Note: some HEXAGON scenes are delivered in more than 4 pieces. The automatic stitching process for these scenes would possibly need more than 60 GB RAM, which has not been successfully tested yet. Splitting scenes with e.g. 7 pieces in two stitching groups has not been successful too due to the same RAM problem. For those scenes it is possibly practical to enlarge the physical RAM with a swap file to a total of > 80 GB.

## Stitching process

**1)** Create a folder in your local file system that only contains the [hugin_automatic_stitching.sh](../scripts/hugin_automatic_stitching.sh) script and the pieces of the scene that you would like to stitch together. Note: The script has to be adapted for HEXAGON scenes with more or fewer pieces (currently for scene pieces `_a` to `_f`) --> lines 35, 45 in the script

**2)** Navigate to the created folder in your terminal and run the `hugin_automatic_stitching.sh` script passing the name of the satellite mission (`CORONA`, `GAMBIT` or `HEXAGON`) as an argument:

e.g. `bash hugin_automatic_stitching.sh CORONA`

It outputs `stitched_D*.tif` which is the result of the stitching process.

**3)** The stitching process produces a `.tif` that contains 2 bands. Only the first band is relevant for further processing steps. Therefore only import the first band to the GRASS xy location using the `band=1`parameter.

`r.in.gdal input=stitched_D*.tif output=stitched_D* band=1`
Note: Make sure the output name does not include `-`, otherwise `r.mapcalc` in the next step  will not work. Use the `g.rename` command if required.

**Continue** with the cropping of the remaining physical film border in [2_cropping.md](2_cropping.md).
