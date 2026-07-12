## DESCRIPTION

*i.ortho.corona* runs the required steps from
[i.ortho.photo](i.ortho.photo.md) for the orthorectification of KH-4A/B
Corona and KH-9 Hexagon scenes.

*i.ortho.corona* requires the image group to be already created. Based
on the input parameters it then runs
[i.ortho.target](i.ortho.target.md), [i.ortho.elev](i.ortho.elev.md),
[i.ortho.camera](i.ortho.camera.md),
[i.ortho.position](i.ortho.position.md),
[i.ortho.init](i.ortho.init.md),
[i.ortho.transform](i.ortho.transform.md), and
[i.ortho.rectify](i.ortho.rectify.md). If the **-t** flag is applied, it
only outputs the result of [i.ortho.transform](i.ortho.transform.md) and
does not continue to run [i.ortho.rectify](i.ortho.rectify.md). If the
**logfile** parameter is indicated, the output of [i.ortho.transform
-t](i.ortho.tranform.md) will be written to a logfile.

## SEE ALSO

*[i.ortho.photo](i.ortho.photo.md), [i.ortho.target](i.ortho.target.md),
[i.ortho.elev](i.ortho.elev.md), [i.ortho.camera](i.ortho.camera.md),
[i.ortho.position](i.ortho.position.md),
[i.ortho.init](i.ortho.init.md),
[i.ortho.transform](i.ortho.transform.md),
[i.ortho.rectify](i.ortho.rectify.md)*

## AUTHOR

Guido Riembauer, [mundialis](https://www.mundialis.de/)
