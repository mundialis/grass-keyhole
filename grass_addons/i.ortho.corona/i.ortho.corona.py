#!/usr/bin/env python3
# -*- coding: utf-8 -*-

############################################################################
#
# MODULE:     i.ortho.corona
# AUTHOR(S):  Guido Riembauer
# PURPOSE:    Runs steps for i.ortho.photo for KH-4A/B Corona and KH-9 Hexagon scenes
#
# COPYRIGHT:  (C) 2020 by the GRASS Development Team
#
#        This program is free software under the GNU General Public
#        License (>=v2). Read the file COPYING that comes with GRASS
#        for details.
#
#############################################################################


# %module
# % description: Runs steps for i.ortho.photo for KH-4A/B Corona and KH-9 Hexagon scenes
# % keyword: imagery
# % keyword: orthorectification
# %end

# %option G_OPT_I_GROUP
# % key: group
# % guisection: Input
# % required: yes
# %end

# %option G_OPT_F_INPUT
# % key: grasspoints
# % label: path to GCP file in grass format
# % description: path to GCP file in grass format
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
# % required: no
# % answer: +proj=utm +zone=32 +datum=WGS84 +units=m
# %end

# %option
# % key: camheading
# % type: string
# % label: camera heading (forward or aft)
# % required: yes
# % options: forward,aft
# % answer: forward
# %end

# %option
# % key: flightdir
# % type: string
# % label: flight direction (north or south)
# % required: yes
# % options: north,south
# % answer: south
# %end

# %option
# % key: targetdem
# % type: string
# % label: Name of DEM in target location/mapset
# % required: yes
# %end

# %option
# % key: targetlocmapset
# % type: string
# % label: target location and mapset in the format location/mapset
# % required: yes
# %end

# %option G_OPT_MEMORYMB
# %end

# %option
# % key: map_extension
# % type: string
# % label: extension to be added to the rectified map in the target mapset
# % required: no
# % answer: _utm_v1
# %end

# %option
# % key: target_res
# % type: string
# % label: resolution of rectified map (in meters)
# % required: no
# % answer: 2
# %end

# %option
# % key: focal_length
# % type: string
# % label: focal length of the camera
# % required: no
# % answer: 609.602
# %end

# %option
# % key: scan_res
# % type: string
# % label: scan resolution of films in pixels/cm
# % required: no
# % answer: 1432.3507
# %end

# %option
# % key: default_height
# % type: string
# % label: altitude of the satellite in meters
# % required: no
# % answer: 160000
# %end

# %option
# % key: logfile
# % type: string
# % label: path to store logfile of i.ortho.transform
# % required: no
# %end

# %flag
# % key: t
# % description: Only run until i.ortho.transform to analyse GCPs - don't run rectification
# %end

# import library
import os
import sys
import shutil
import psutil
import grass.script as grass
import subprocess

def freeRAM(unit, percent=100):
    """ The function gives the amount of the percentages of the installed RAM.
    Args:
        unit(string): 'GB' or 'MB'
        percent(int): number of percent which shoud be used of the free RAM
                      default 100%
    Returns:
        memory_MB_percent/memory_GB_percent(int): percent of the free RAM in
                                                  MB or GB

    """
    # use psutil cause of alpine busybox free version for RAM/SWAP usage
    mem_available = psutil.virtual_memory().available
    swap_free = psutil.swap_memory().free
    memory_GB = (mem_available + swap_free)/1024.0**3
    memory_MB = (mem_available + swap_free)/1024.0**2

    if unit == "MB":
        memory_MB_percent = memory_MB * percent / 100.0
        return int(round(memory_MB_percent))
    elif unit == "GB":
        memory_GB_percent = memory_GB * percent / 100.0
        return int(round(memory_GB_percent))
    else:
        grass.fatal("Memory unit <%s> not supported" % unit)


def getfiducials(rows, cols, scan_resolution):
    height_mm = rows*10/scan_resolution
    width_mm = cols*10/scan_resolution
    fid_nw = -width_mm/2, height_mm/2
    fid_ne = width_mm/2, height_mm/2
    fid_se = width_mm/2, -height_mm/2
    fid_sw = -width_mm/2, -height_mm/2
    return fid_nw, fid_ne, fid_se, fid_sw


def string_refpoints(fid_nw, fid_ne, fid_se, fid_sw, rows, cols):
    string = ('# Ground Control Points File\n#\n# target location: XY\n# target mapset: '+
              'source_mapset\n# source  target  status\n# east north east north '+
              '(1=ok, 0=ignore)\n#-------------------------------------------------------------\n'+
              '0 %s     %s %s     1\n'%(rows, fid_nw[0], fid_nw[1])+
              '%s %s     %s %s     1\n'%(cols, rows, fid_ne[0],fid_ne[1])+
              '%s 0     %s %s     1\n'%(cols,fid_se[0],fid_se[1])+
              '0 0     %s %s     1\n'%(fid_sw[0],fid_sw[1]))
    return string


def main():

    # input parameters
    group = options['group']
    grasspoints = options['grasspoints']
    nw = options['nw']
    ne = options['ne']
    sw = options['sw']
    se = options['se']
    proj = options['proj']
    cameraheading = options['camheading']
    flightdirection = options['flightdir']
    targetloc = options['targetlocmapset'].split('/')[0]
    targetmapset = options['targetlocmapset'].split('/')[1]
    targetdem = options['targetdem']
    memory = int(options['memory'])
    map_extension = options['map_extension']
    target_resolution = options['target_res']
    focal_length = options['focal_length']
    scan_resolution = float(options['scan_res'])
    default_height = options['default_height']
    transform_only = flags['t']

    # get omega
    if cameraheading == 'forward':
        omega = 15
    elif cameraheading == 'aft':
        omega = -15
    if flightdirection == 'south':
        omega = -omega
    omega = str(omega)

    # get current GRASS environment
    env = grass.gisenv()
    start_gisdbase = env['GISDBASE']
    start_location = env['LOCATION_NAME']
    start_mapset = env['MAPSET']

    # check for i.ortho.position
    if not grass.find_program('i.ortho.position', '--help'):
        grass.fatal(_("The 'i.ortho.position' module was not found, install it first:") +
                    "\n" +
                    "g.extension i.ortho.position url=/path/to/i.ortho.position")

    # check for free ram
    free_ram = freeRAM('MB', 100)
    if free_ram < memory:
        grass.warning(
            "Using %d MB but only %d MB RAM available. Setting memory to free RAM"
            % (memory, free_ram))
        memory = free_ram

    # get name of the raster to be rectified
    rastername_keys = list(grass.parse_command('i.group', group=group, flags='lg').keys())
    if len(rastername_keys) > 1:
        grass.fatal(_("Group contains more than one raster, Exiting..."))
    rastername = rastername_keys[0]

    # get raster size
    raster_rows = grass.parse_command('r.info', map=rastername, flags='g')['rows']
    raster_cols = grass.parse_command('r.info', map=rastername, flags='g')['cols']

    # run i.ortho.target
    grass.run_command('i.ortho.target', group=group, target_location=targetloc, mapset_loc=targetmapset)

    # run i.ortho.elev
    grass.run_command('i.ortho.elev', group=group, elev=targetdem, location=targetloc, mapset=targetmapset, units='meters')

    # get fiducials
    fid_nw, fid_ne, fid_se, fid_sw = getfiducials(int(raster_rows), int(raster_cols), scan_resolution)

    fidstring = '%s,%s,%s,%s,%s,%s,%s,%s'%(fid_nw[0],fid_nw[1],fid_ne[0],fid_ne[1],fid_se[0],fid_se[1],fid_sw[0],fid_sw[1])
    # run i.ortho.camera
    grass.run_command('i.ortho.camera', group=group, camera=group, name=group, id=group, clf=focal_length, pp='0,0', fid=fidstring)

    # write REF_POINTS file
    ref_points_string = string_refpoints(fid_nw, fid_ne, fid_se, fid_sw, raster_rows, raster_cols)
    ref_points_path = '%s/%s/%s/group/%s/REF_POINTS'%(start_gisdbase,start_location,start_mapset,group)

    if os.path.isfile(ref_points_path):
        grass.message(_('REF_POINTS file already in group folder.'))
    else:
        try:
            with open(ref_points_path, "w") as file:
                file.write(ref_points_string)
        except Exception as e:
            grass.fatal(_('Unable to write REF_POINTS file.'))

    # copy the GCP file into the group folder
    control_points_path = '%s/%s/%s/group/%s/CONTROL_POINTS'%(start_gisdbase,start_location,start_mapset,group)
    if os.path.isfile(control_points_path):
        grass.message(_('CONTROL_POINTS file already in group folder.'))
    else:
        try:
            shutil.copyfile(grasspoints,control_points_path)
        except Exception as e:
            grass.fatal(_('Unable to copy CONTROL_POINTS file.'))

    # run i.ortho.position
    keylist = list(grass.parse_command('i.ortho.position', group=group, omega=omega, height=default_height, nw=nw, ne=ne, sw=sw, se=se, proj=proj).keys())
    omega_est = keylist[1].split(': ')[1]
    phi_est = keylist[2].split(': ')[1]
    kappa_est = keylist[3].split(': ')[1]
    xc_est = keylist[4].split(': ')[1]
    yc_est = keylist[5].split(': ')[1]
    zc_est = str(float(default_height))

    # run i.ortho.init
    grass.run_command('i.ortho.init', group=group, xc=xc_est, yc=yc_est, zc=zc_est, omega=omega_est, phi=phi_est, kappa=kappa_est, xc_sd='1000', yc_sd='1000', zc_sd='1000', omega_sd='0.1', phi_sd='0.1', kappa_sd='0.1', flags='r')

    # run i.ortho.transform
    grass.run_command('i.ortho.transform', group=group, flags='sp', verbose=True)

    if not transform_only:
        if options['logfile']:
            # write logfile
            # i.ortho.transform writes to stderr and stdout, we want to catch both
            stdout_stderr = grass.Popen('i.ortho.transform -sp group=%s --v' % group,
                                        shell=True, stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE).communicate()
            camerastats = stdout_stderr[1].decode('utf-8')
            pointstats = stdout_stderr[0].decode('utf-8')
            logstring = camerastats + pointstats
            logfile = options['logfile']
            if os.path.isfile(logfile):
                grass.warning(_('File %s already exists, will be overwritten...' %
                                logfile))
            with open(logfile, 'w') as file:
                file.write(logstring)
        # run i.ortho.rectify
        grass.run_command('i.ortho.rectify', group=group, extension=map_extension, resolution=target_resolution, mem=memory, flags='ap', verbose=True)


if __name__ == "__main__":
    options, flags = grass.parser()
    sys.exit(main())
