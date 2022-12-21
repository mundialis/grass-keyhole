#!/usr/bin/env python3
# -*- coding: utf-8 -*-

############################################################################
#
# MODULE:     i.ortho.position
# AUTHOR(S):  Markus Metz
# PURPOSE:    Estimate sensor position from scene center and angles
#
# COPYRIGHT:  (C) 2020 by the GRASS Development Team
#
#        This program is free software under the GNU General Public
#        License (>=v2). Read the file COPYING that comes with GRASS
#        for details.
#
#############################################################################
# %module
# % description: Estimate sensor position from scene center and angles
# % keyword: imagery
# % keyword: orthorectification
# %end
# %option G_OPT_I_GROUP
# % guisection: Input
# % required: yes
# %end
# %option G_OPT_M_COORDS
# % key: nw
# % label: North-West corner coordinates in ll (lon,lat)
# % description: must be decimal degrees
# % required: yes
# %end
# %option G_OPT_M_COORDS
# % key: ne
# % label: North-East corner coordinates in ll (lon,lat)
# % description: must be decimal degrees
# % required: yes
# %end
# %option G_OPT_M_COORDS
# % key: sw
# % label: South-West corner coordinates in ll (lon,lat)
# % description: must be decimal degrees
# % required: yes
# %end
# %option G_OPT_M_COORDS
# % key: se
# % label: South-East corner coordinates in ll (lon,lat)
# % description: must be decimal degrees
# % required: yes
# %end
# %option
# % key: proj
# % type: string
# % label: PROJ definition of the target CRS
# % description: e.g. +proj=utm +zone=32 +datum=WGS84 +units=m
# % required: yes
# %end
# %option
# % key: omega
# % type: double
# % description: Omega (pitch): Raising or lowering of the aircraft's front (turning around the wings' axis)
# % required: no
# %end
# %option
# % key: height
# % type: double
# % description: Flight height
# % required: yes
# %end

# import library
import os
import sys
import threading
import math
import re
import grass.script as gscript
from grass.script.utils import separator, parse_key_val, encode, decode
from grass.script import core as gcore


class TrThread(threading.Thread):

    def __init__(self, ifs, inf, outf):
        threading.Thread.__init__(self)
        self.ifs = ifs
        self.inf = inf
        self.outf = outf

    def run(self):
        while True:
            line = self.inf.readline()
            if not line:
                break
            line = line.replace(self.ifs, ' ')
            line = encode(line)
            self.outf.write(line)
            self.outf.flush()

        self.outf.close()


def main():
    # check if GISBASE is set
    if "GISBASE" not in os.environ:
        # return an error advice
        print("You must be in GRASS GIS to run this program.")
        sys.exit(1)

    # input group
    group = options['group']
    # input nw
    nw = options['nw']
    # input ne
    ne = options['ne']
    # input sw
    sw = options['sw']
    # input se
    se = options['se']
    # input proj
    projstring = options['proj']
    # input flight height
    height = float(options['height'])
    # input omega
    omega = 0
    if options['omega']:
        omega = float(options['omega'])

    # check for cct
    have_cct = True
    coordsep = ' '
    if not gcore.find_program('cct'):
        have_cct = False
        coordsep = '\t'
        if not gcore.find_program('proj'):
            gcore.fatal(_(
                "Neither cct nor proj program found, install PROJ first: \
                https://proj.org"))

    nw_east = float(nw.split(',')[0])
    nw_north = float(nw.split(',')[1])
    ne_east = float(ne.split(',')[0])
    ne_north = float(ne.split(',')[1])
    sw_east = float(sw.split(',')[0])
    sw_north = float(sw.split(',')[1])
    se_east = float(se.split(',')[0])
    se_north = float(se.split(',')[1])

    # check south
    if sw_east > se_east:
        gcore.fatal("se must be east of sw")
    # check north
    if nw_east > ne_east:
        gcore.fatal("ne must be east of nw")
    # check west
    if sw_north > nw_north:
        gcore.fatal("nw must be north of sw")
    # check east
    if se_north > ne_north:
        gcore.fatal("ne must be north of se")

    scene_center_east = (nw_east + ne_east + sw_east + se_east) / 4.0
    scene_center_north = (nw_north + ne_north + sw_north + se_north) / 4.0

    dxn = ne_east - nw_east
    dyn = ne_north - nw_north
    dxs = se_east - sw_east
    dys = se_north - sw_north

    kappan = math.degrees(math.atan2(dyn, dxn))
    kappas = math.degrees(math.atan2(dys, dxs))
    kappa = (kappan + kappas) / 2.0

    # convert ll coordinates to target CRS
    # shell: echo 9.19625 36.47025 | cct -z0 -t0 +proj=utm +zone=32 +datum=WGS84 +units=m
    tmpfile = gcore.tempfile()
    fd = open(tmpfile, "w")
    fd.write("%s %s\n" % (scene_center_east, scene_center_north))
    fd.close()
    inf = open(tmpfile)

    outf = sys.stdout

    if have_cct:
        cmd = ['cct'] + ['-z0'] + ['-t0'] + projstring.split()
    else:
        cmd = ['proj'] + projstring.split()

    p = gcore.Popen(cmd, stdin=gcore.PIPE, stdout=gcore.PIPE)

    ifs = ' '
    tr = TrThread(ifs, inf, p.stdin)
    tr.start()

    x = y = 0

    for line in p.stdout:
        try:
            # incredibly unfriendly output format of cct
            line = re.sub(' +', ' ', decode(line).strip())
            outcoords = line.split(coordsep)
            x = outcoords[0]
            y = outcoords[1]
        except ValueError:
            gcore.fatal(line)
        # only one line
        break

    scene_center_east = float(x)
    scene_center_north = float(y)

    p.wait()

    if p.returncode != 0:
        gcore.warning(_(
            "Projection transform probably failed, please investigate"))

    tan_omega = math.tan(math.radians(omega))
    ground_offset = height * tan_omega
    dx = ground_offset * math.sin(math.radians(kappa))
    dy = -ground_offset * math.cos(math.radians(kappa))
    camera_x = scene_center_east + dx
    camera_y = scene_center_north + dy

    outf.write("summary:\n")
    outf.write("omega: %.3f\n" % omega)
    outf.write("phi: 0\n")
    outf.write("kappa: %.3f\n" % kappa)
    outf.write("camera east: %.2f\n" % camera_x)
    outf.write("camera north: %.2f\n\n" % camera_y)

    outf.write("Parameters for i.ortho.init:\n")
    outf.write("i.ortho.init -r group=%s xc=%.2f yc=%.2f zc=%.2f omega=%.3f phi=0 kappa=%.3f xc_sd=1000 yc_sd=1000 zc_sd=1000 omega_sd=0.1 phi_sd=0.1 kappa_sd=0.1\n" %
               (group, camera_x, camera_y, height, omega, kappa))


if __name__ == "__main__":
    options, flags = gscript.parser()
    sys.exit(main())
