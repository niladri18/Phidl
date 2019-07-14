from __future__ import division, print_function, absolute_import
import numpy as np
import pdb
import pylab
import math

from phidl import Device, Layer, LayerSet, make_device
#from phidl import quickplot as qp # Rename "quickplot()" to the easier "qp()"
import phidl.geometry as pg
import phidl.routing as pr
import phidl.utilities as pu
from phidl import quickplot2 as qp


def makeLine(x0,y0,width, height, layer):
	L = Device('line')
	L.add_polygon([(x0, y0), (x0 + width, y0), (x0 + width, y0+ height), (x0, y0+ height)], layer = layer)
	return L

def makeLineSpace(x0,y0,width, height,pitch,ymax, layer):
	#---------------------------------------------#
	# Creates a line space pattern in y-direction
	#	x0: x coordinate of the lower left line
	#	y0: y coordinate of the lower left line
	#	width: width of each line
	#	height: height of each line
	#	pitch: pitch of each line
	#	pitch > height
	#---------------------------------------------#
	if abs(pitch) < abs(height):
		print("pitch must be greater then height")
		return 
	LS = Device('linespace')
	if pitch > 0:
		while y0+height <= ymax:
			Li = makeLine(x0,y0,width,height,layer)
			LS.add_ref(Li)
			y0 += pitch
	elif pitch < 0:
		while y0+height >= -ymax:
                        Li = makeLine(x0,y0,width,height,layer)
                        LS.add_ref(Li)
                        y0 += pitch
	return y0, LS

def makeCross(x0,y0,width,lw, layer):
	# Make cross with 
	# x0,y0 : center
	# width: width of the bounding box
	# lw: linewidth
	cross = Device("cross")
	cross.add_polygon([(x0-width/2,y0-lw/2),(x0-width/2,y0+lw/2), (x0+width/2,y0+lw/2), (x0+width/2,y0-lw/2) ], layer = layer)
	cross.add_polygon([(x0-lw/2,y0-width/2),(x0-lw/2,y0+width/2), (x0+lw/2,y0+width/2), (x0+lw/2,y0-width/2) ], layer = layer)
	return cross
	
#==============================================================================
# Template for creating a PPE macro
#==============================================================================
D = Device('PPE')
layer = 1
NOOPC = 2
OPC = 3

# Define global variables
xmax = 500
ymax = 500
xmin = 0
ymin = 0
xm = (xmax-xmin)/2.0
ym = (ymax-ymin)/2.0

# Cover the entire macro
D.add_polygon([(0,0),(xmax,0),(xmax,ymax),(0,ymax) ], layer = 0)

## Place the pattern rec
Cross = makeCross(xm,ym,100,10, layer)
Cross.rotate(45,center = [xm,ym])
D.add_ref(Cross)

# calculate offset due to the cross
xoff = math.sqrt(100*50)
yoff = math.sqrt(100*50)

## Top left 1
x0 = 10
y0 = ym
y0, LS1 = makeLineSpace(x0,y0, 240 - xoff ,10,20,ym + yoff, layer)
D.add_ref(LS1)
## Top left 2
x0 = 10
y0 = y0 
y0, LS1 = makeLineSpace(x0,y0,240,10,20,500, layer)
D.add_ref(LS1)

## Top right 1
x0 = xm + xoff 
y0 = ym
y0, LS2 = makeLineSpace(x0,y0, 240 - xoff + 10 ,10,30,ym + yoff, layer)
D.add_ref(LS2)
## Top right 2
x0 = xm + 10
y0 = y0
y0, LS2 = makeLineSpace(x0,y0,240,10,30,500, layer)
D.add_ref(LS2)
## Lower left 1
x0 = 10
y0 = 0
y0, LS3 = makeLineSpace(x0,y0,240,10,30,xm - yoff, layer)
D.add_ref(LS3)
## Lower left 2
x0 = 10
y0 = y0
y0, LS3 = makeLineSpace(x0,y0,240 - xoff ,10,30,240, layer)
D.add_ref(LS3)
## Lower right 1
x0 = xm + 10
y0 = 0
y0, LS4 = makeLineSpace(x0,y0,240,10,20,xm - yoff, layer)
D.add_ref(LS4)

## Lower right 2
x0 = xm + xoff
y0 = y0
y0, LS4 = makeLineSpace(x0,y0,240 - xoff + 10 ,10,20,240, layer)
D.add_ref(LS4)

# Add NOOPC cover on the pattern rec
xt = xoff - 10
yt = yoff - 10
D.add_polygon([(xm-xt,ym-yt), (xm-xt,ym+yt), (xm+xt,ym+yt), (xm+xt,ym-yt) ], layer = NOOPC)


D.write_gds("ppe.gds")

