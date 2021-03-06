#!/usr/local/env python

# check for correct usage
import os, sys
import string

if not sys.argv[1:]:
    print "Usage: python skullStripper.py image.mnc"
    sys.exit(1)
else:
    filename = sys.argv[1]

# first, load a script that sets the paths for the modules we load
import paths
import time
import vtk
import airs

ext = os.path.splitext(filename)[1]
if ext == '.mnc' or ext == '.MNC':
    reader = vtk.vtkMINCImageReader()

reader.SetFileName(filename)
reader.UpdateWholeExtent()

imageData = reader.GetOutput()

stripper = airs.vtkImageMRIBrainExtractor()
stripper.SetInput( imageData )

# A kludge to handle low axial resolution images
spacing = imageData.GetSpacing()
zres = spacing[2]

if zres > 1.5:
    bt = 0.50
else:
    bt = 0.70

# Optimized parameters
stripper.SetRMin(8.0)
stripper.SetRMax(10.0)
stripper.SetD1(7.0)
stripper.SetD2(3.0)
stripper.SetBT(bt)
stripper.Update()

# Get the basename
name = string.split(filename, "/")[-1]
basename = string.split(name, ".")[0]

# Write the mesh
writer = vtk.vtkPolyDataWriter()
writer.SetFileName(basename + "_mesh.vtk")
writer.SetInput( stripper.GetBrainMesh() )
writer.Write()

# Write the segemented image
writer2 = vtk.vtkMINCImageWriter()
writer2.SetInput( stripper.GetOutput() )
writer2.SetFileName(basename + "_seg.mnc" )
writer2.Write()
