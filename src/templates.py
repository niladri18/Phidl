
from __future__ import division, print_function, absolute_import
import numpy as np
import pdb
import pylab
import math

from numpy import sqrt, pi, cos, sin, log, exp, sinh
from phidl import Device, Layer, LayerSet, make_device
#from phidl import quickplot as qp # Rename "quickplot()" to the easier "qp()"
import phidl.geometry as pg
import phidl.routing as pr
import phidl.utilities as pu
from phidl import quickplot2 as qp
import time



def fibonacci(n, width = 0.008, angle_resolution = 1.5, layer = 0):
	# ---------------------------------------
	# Template that draws a golden spiral
	# n : number of points on the spiral
	# width: width of the spiral
	# ---------------------------------------
	pi = 3.14
	F = Device("spiral")
	start_angle = 0
	dtheta = 360/n
	theta = dtheta
	for i in range(n):
		angle1 = (start_angle)*pi/180
		angle2 = (start_angle + dtheta)*pi/180
		r1 = 0.0053*start_angle
		r2 = 0.0053*(start_angle + dtheta)
		x1 = r1*math.cos(angle1)
		y1 = r1*math.sin(angle1)

		x2 = (r1+width)*math.cos(angle1)
		y2 = (r1+width)*math.sin(angle1)
	
		x3 = (r2+width)*math.cos(angle2)
		y3 = (r2+width)*math.sin(angle2)


		x4 = (r2)*math.cos(angle2)
		y4 = (r2)*math.sin(angle2)


		F.add_polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)], layer = layer)
		start_angle += dtheta
	
	return F

def makeResonator(radius = 10, width = 0.5, space = 1.0):
	#------------------------
	# Make a ring resonator
	# radius: of the ring
	# width: of the ring and the line
	# space: space between the edge of the ring and the line
	#------------------------
	C= Device("Resonator")
	R = pg.ring(radius = radius, width = width)
	C.add_ref(R)
	L1 = makeLine(radius+space,-radius,width,2*radius)
	C.add_ref(L1)
	L2 = makeLine(-radius-space-width,-radius,width,2*radius)
	C.add_ref(L2)
	

	return C
	
		
	

def makeLine(x0,y0,width, height, layer=0):
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
	#--------------------------------
	# Make cross with 
	# x0,y0 : center
	# width: width of the bounding box
	# lw: linewidth
	#----------------------------------
	cross = Device("cross")
	cross.add_polygon([(x0-width/2,y0-lw/2),(x0-width/2,y0+lw/2), (x0+width/2,y0+lw/2), (x0+width/2,y0-lw/2) ], layer = layer)
	cross.add_polygon([(x0-lw/2,y0-width/2),(x0-lw/2,y0+width/2), (x0+lw/2,y0+width/2), (x0+lw/2,y0-width/2) ], layer = layer)
	return cross


def main():

	#---- Example of using the templates---#
	D = Device()


	# Make a golden spiral with 1000 grids
	F = fibonacci(1000)
	D.add_ref(F)
	D.write_gds("spiral.gds")

	# Make a ring resonator
	D2 = Device()
	C = makeResonator()
	D2.add_ref(C)
	D2.write_gds("resonator.gds")



if __name__=="__main__":
	start_t = time.time()
	main()
	end_t = time.time()
	print("time: %fs"%(end_t-start_t))
