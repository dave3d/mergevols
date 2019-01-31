#! /usr/bin/env python


import sys, getopt
import SimpleITK as sitk

nx = 2
ny = 2
pad = 20
verbose = False

# this script assumes you have a grid (default=2x2) of volumes that you want to put together into
# a single volume.  it lays them out first in the Y direction then X.
#

#
#
def usage():
    print ""
    print "mergevols.py: [opts] volume1 ... volumeN output_volume"
    print ""

# parse the command line arguments
#
try:
    opts, args = getopt.getopt(sys.argv[1:], "vhsx:y:p:",
        [ "verbose", "help", "sort", "pad"] )
except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit(2)

for o, a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-v", "--verbose"):
        verbose = True
    elif o in ("-p", "--pad"):
        pad = int(a)
    elif o in ("-x"):
        nx = int(a)
    elif o in ("-y"):
        ny = int(a)
    else:
       assert False, "unhandled option"

files = args

if len(files) < 2:
    usage()
    sys.exit(3)

names = files[0:len(files)-1]
outname = files[len(files)-1]

if len(names) != nx*ny:
    print "Error:  number of input volumes is not NX by NY"
    print "Files: ", names
    print "NX-NY: ", nx, ny
    sys.exit(4)

if verbose:
    print ""
    print "Input volumes: ", names
    print "Output volume: ", outname
    print "NX, NY: ", nx, ny

images = []

for name in names:
    img = sitk.ReadImage(name)
    images.append(img)

print len(images)

xsizes = []
ysizes = []

for x in range(nx):
  xsizes.append(0)
for y in range(ny):
  ysizes.append(0)

x = 0
y = 0
coords = []
zend = 0

for img in images:
    coord = [x, y]
    coords.append(coord)
    size = img.GetSize()
    print size
    img.SetOrigin([0,0,0])

    if size[0] > xsizes[x]:
        xsizes[x] = size[0]
    if size[1] > ysizes[y]:
        ysizes[y] = size[1]
    if size[2] > zend:
        zend = size[2]

    y = y+1
    if y>=ny:
      x = x+1
      y = 0

print coords

print "X sizes:", xsizes
print "Y sizes:", ysizes


xstarts = [pad]
i = 0
xend = 0
for x in xsizes:
    xstarts.append(xstarts[i]+x)
    i=i+1
    xend = xstarts[i]

print "X starts:", xstarts

ystarts = [pad]
i = 0
yend = 0
for y in ysizes:
    ystarts.append(ystarts[i]+y)
    i=i+1
    yend = ystarts[i]

print "Y starts:", ystarts

outsize = [xend, yend, zend]
print "Output size", outsize

outimg = sitk.Image(outsize, images[0].GetPixelID(), 1)
origin0 = images[0].GetOrigin()
spacing = images[0].GetSpacing()
#origin = [origin0[0] - pad*spacing[0], origin0[1] - pad*spacing[1], origin0[2]]
outimg.SetSpacing(spacing)
outimg.SetOrigin([0,0,0])
outimg.SetDirection(images[0].GetDirection())


i = 0

for img in images:
#    sitk.Show(img)
    coord = coords[i]
    xpos = xstarts[coord[0]]
    ypos = ystarts[coord[1]]
    destindex = [xpos, ypos, 0]
    print destindex
    outimg = sitk.Paste(outimg, img, img.GetSize(), [0,0,0], destindex)
    i = i+1

#sitk.Show(outimg)
print outimg.GetSize()
print outimg.GetOrigin()
print outimg.GetSpacing()

sitk.WriteImage(outimg, outname)
