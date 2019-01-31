# mergevols
A python script that uses SimpleITK to combine multiple volumes into one.

It assumes the files on the command line are volume images, readable by SimpleITK.

The script assumes you have a grid (default=2x2) of volumes that you want to put together into
a single volume.  it lays them out first in the Y direction then X.

It uses SimpleITK's Paste function to copy the source volumes into the target volume.
