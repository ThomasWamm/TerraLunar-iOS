#!/usr/bin/python3
#  20:59pm  18-May-2020      TerraLunar program
# This version for Pythonista environment on iOS devices.
#
# 2-D orbital mechanics simulation in Earth-Moon space.
# by Thomas during Spring 2020 for learning Python & SWEng
# 
# use simplified Newtonian physics and numerical integrations
# F = ma = -GMm/r^2
# a = F/m = -GM/r^2
# v = v + dv = v + adt
# x = x + dx = x + vdt
# t = t + dt

import canvas
from random import randint
import math
import time
import json
import motion
import dialogs

print('TerraLunar: simplified orbital mechanics simulation')

# global objects for graphics, Earth, Moon, and one spacecraft

cfg0 = {'for local configuration: ': 'edit this then resave as tl.cfg',
       'windowwidth': 380,
       'windowheight': 450,
       'localconfig': 'low res on iPad Air2'}

cfg1 = {'for local configuration: ': 'edit this then resave as tl.cfg',
       'windowwidth': 760,
       'windowheight': 900,
       'localconfig': 'optimized for iPad Air2'}

cfg11 = {'for local configuration: ': 'edit this then resave as tl.cfg',
       'windowwidth': 1520,
       'windowheight': 1800,
       'localconfig': 'hi res on iPad Air2'}


cfg2 = {'for local configuration: ': 'edit this then resave as tl.cfg',
       'windowwidth': 500,
       'windowheight': 900,
       'localconfig': 'optimized for iPhoneX'}

cfg3 = {'for local configuration: ': 'edit this then resave as tl.cfg',
       'windowwidth': 300,
       'windowheight': 426,
       'localconfig': 'optimized for iPod6'}

cfg4 = {'for local configuration: ': 'edit this then resave as tl.cfg',
       'windowwidth': 150,
       'windowheight': 213,
       'localconfig': 'low res on iPod6'}

cfg5 = {'for local configuration: ': 'edit this then resave as tl.cfg',
       'windowwidth': 600,
       'windowheight': 852,
       'localconfig': 'hi res on iPod6'}

cfg6 = {'for local configuration: ': 'edit this then resave as tl.cfg',
       'windowwidth': 450,
       'windowheight': 639,
       'localconfig': 'medium res on iPod6'}

cfg = cfg1

with open('tl-sample.cfg', 'w') as f:
	json.dump(cfg, f)

try:
	with open('tl.cfg', 'r') as f:
		cfg = json.load(f)
	print('Found local config file tl.cfg')
except:
	print('\nLocal config file tl.cfg not found, so will use defaults.')
	
winwidth = cfg['windowwidth']
winheight = cfg['windowheight']
localconfig = cfg['localconfig']

print(f'Screen width x height = {winwidth} x {winheight} {localconfig}')
print()

# define a class to store each set of initial conditions
class Iset:
	def __init__(self, moondegrees=60.0,
											shipxmd=1.0,
											shipymd=0.0,
											shipvx=0.0,
											shipvy=851.0,
											dtime=10,
											winscale=1.2,
											radscale=5.0,
											checktrigger=1000,
											description='Default setup'):
	
		self.moondegrees = moondegrees
		self.shipxmd = shipxmd
		self.shipymd = shipymd
		self.shipvx = shipvx
		self.shipvy = shipvy
		self.dtime = dtime
		self.winscale = winscale
		self.radscale = radscale
		self.checktrigger = checktrigger
		self.description = description
		
setuplib = (['moondeg','xmd','ymd','vx','vy','dt','wscale','rscale','chktrig','Description'],
            [60.0, 1.1, 0.0, 0.0, 1000.0, 1, 2.0, 5.0, 10000, 'eventual impact'],
            [60.0, 1.1, 0.0, 0.0, 1000.0, 10, 2.0, 5.0, 10000, 'eventual lunar impact'],
            [60.0, 1.1, 0.0, 0.0, 1000.0, 60, 2.0, 5.0, 1000, 'eventual lunar impact; big dt'],
            [60.0, 1.1, 0.0, 0.0, 1000.0, 30, 2.0, 5.0, 10000, 'eventual escape 30'],
            [60.0, 1.1, 0.0, 0.0, 1000.0, 3, 2.0, 5.0, 10000, 'eventual escape 3'],
            [60.0, 1.1, 0.0, 0.0, 1000.0, 3, 2.0, 5.0, 10000, 'eventual escape .3'],
            [0.0, 0.017, 0.0, 0.0, 9200.0, 1, 0.03, 1.0, 1000, 'elliptical orbit'],
            [0.0, 0.017, 0.0, 0.0, 7900.0, 1, 0.02, 1.0, 1000, 'LEO = low Earth orbit'],
            [0.0, 0.10968811, 0.0, 0.0, 3074.7937, 1, 1.0, 1.0, 1000, 'geosynchronous orbit'],
            [0.0, 0.8491, 0.0, 0.0, 861.2724303351369, 10, 0.8, 1.0, 1000, 'just inside L1 orbit'],
            [0.0, 0.8491, 0.0, 0.0, 861.272430335137, 10, 0.8, 1.0, 1000, 'just outside L1 orbit'],
            [0.0, 0.85, 0.0, 0.0, 870.0, 10, 1.0, 1.0, 1000, 'lunar orbit'],
            [0.0, 0.90, 0.0, 0.0, 770.0, 10, 0.8, 1.0, 1000, 'distant lunar orbit'],
            [135.4, 0.0168, 0.0, 0.0, 11050.0, 1, 1.5, 1.0, 1000, 'escape with lunar assist'],
            [135.0, 0.0168, 0.0, 0.0, 11050.0, 0.1, 0.9, 1.0, 1000, 'Ranger direct lunar impact'],
            [0.0, 0.995, 0.0, 0.0, 2590.0, 1, 0.7, 1.0, 1000, 'Apollo 8 orbiting moon'],
            [135.0, 0.017, 0.0, 0.0, 10998.0, 1, 0.7, 1.0, 1000, 'Apollo 13 safe return'],
            [135.0, 0.017, 0.0, 0.0, 11000.0, 1, 0.8, 1.0, 1000, 'lost Apollo 13, later impact'],
            [130.0, 0.02, 0.0, 0.0, 10080.0, 1, 1.0, 1.0, 1000, 'chaos, then lunar impact'],
            [60.0, 0.8, 0.0, 400.0, 1100., 50, 2.0, 5.0, 1000, 'chaos, then escape'],
            [60.0, 0.8, 0.0, 100.0, 1073., 1, 10.0, 10.0, 10000, 'gravity assist escape'],
            [60.0, 1.0, 0.0, 0.0, 900.0, 101, 1.3, 1.0, 1000, 'chaos, then lunar impact'],
            [55.0, 3.0, 0.0, 0.0, 0.0, 1, 3.0, 10.0, 10000, 'non-fall to Earth from 3 moonunits.'],
            [40.0, 5.0, 0.0, 0.0, 0.0, 1, 3.0, 1.0, 10000, 'fall to Earth from 5 moonunits.'],
            [60.0, 0.9, 0.0, 0.0, 950.0, 60, 1.7, 5.0, 1000, '1.1M steps to Lunar Impact'],
            [60.0, 0.8, 0.0, 0.0, 1073., 10, 1.3, 1.0, 1000, 'lunar impact'],
            [60.0, 1.0, 0.0, 0.0, 923.0, 10, 1.1, 1.0, 1000, 'lunar impact, vy=921-926'])

def grabsetup(i):   # return indexed setup from sample library
	return Iset(moondegrees=setuplib[i][0],
							shipxmd=setuplib[i][1],
							shipymd=setuplib[i][2],
							shipvx=setuplib[i][3],
							shipvy=setuplib[i][4],
							dtime=setuplib[i][5],
							winscale=setuplib[i][6],
							radscale=setuplib[i][7],
							checktrigger=setuplib[i][8],
							description=setuplib[i][9])

def parseparams(d):   # extract setup from json dictionary object
	return Iset(moondegrees=d['moondeg'],
							shipxmd=d['xmd'],
							shipymd=d['ymd'],
							shipvx=d['vx'],
							shipvy=d['vy'],
							dtime=d['dt'],
							winscale=d['wscale'],
							radscale=d['rscale'],
							checktrigger=d['chktrig'],
							description=d['Description'])

def grabsnap():   # grab parameter snapshot to enable logging and replays
  snapdict = {'moondeg': math.degrees(moonangle),
  	'xmd': shipx/moondistance,
  	'ymd': shipy/moondistance,
  	'vx': shipvx,
  	'vy': shipvy,
  	'dt': dtime,
  	'wscale': inz.winscale,
  	'rscale': inz.radscale,
  	'chktrig': inz.checktrigger,
  	'Description': 'Logging: ' + inz.description}
  return snapdict

i = 1
columns = 2
while i < len(setuplib):
	for j in range(i, min(i+columns, len(setuplib))):
		print(f'{j:2d}: {setuplib[j][9]:40}', end='')
	print()
	i += columns

query = None
while query is None:
	query = input("Choose an initial setup (or 0 to pick a json file): ")
	if query == '':     # <Enter> is convenient
		query = 1
	else:
		try:
			query = int(query)
		except:
			print("Enter a number to choose initial setup.")
			query = None

setupnum = query
if setupnum < 1:
	setupnum = 1
if setupnum > len(setuplib)-1:
	setupnum = len(setuplib)-1

inz = grabsetup(setupnum)

params = None
if query == 0:
	try:
		paramfile = dialogs.pick_document()
		with open(paramfile, 'r') as f:
			params = json.load(f)
		inz = parseparams(params)
		print()
		print('Found parameter file ' + paramfile + 
					' with description: ' + inz.description)
		print()
		setupnum = query
	except:
		print('\nValid parameter file not found, so will use setup 1.')
		inz = grabsetup(setupnum)

# start showing stuff on screen

canvas.set_size(winwidth, winheight)
canvas.set_aa_enabled(False)				# important to make thin lines visible
canvas.set_fill_color(0, 0, .15)      # make space almost black
canvas.fill_rect(0, 0, winwidth, winheight)

# plot some random white stars

canvas.set_fill_color(1, 1, 1)
for i in range(53):
	x = randint(0, winwidth)
	y = randint(0, winheight)
	canvas.fill_pixel(x, y)

# use MKS units:  meter, kg, sec
# use average Earth-Moon distance for view scaling
moondistance = 3.84399e8

# set up initial conditions in our simulated universe
# Earth at center origin
earthrad = 6.3781e6
earthx = 0.0
earthy = 0.0

canvas.translate(winwidth/2.0, winheight/2.0)		# earth at center of view
winmin = min(winwidth, winheight)
winmax = max(winwidth, winheight)
viewscale = winmin / (3.0 * moondistance * inz.winscale)		# pixels/meter
canvas.scale(viewscale, viewscale)
apixel = 0.4 / viewscale   # to plot pixels as ship moves
offscreen = winmax / viewscale     # meters to be out of view

# RGB colorsets for Earth and Moon

er, eg, eb = 0.2, 0.2, 1.0		# the blue-ish Earth
mr, mg, mb = 0.6, 0.6, 0.4		# the grey-ish Moon

def show_earth(er, eg, eb):
	canvas.save_gstate()
	canvas.set_fill_color(er, eg, eb)
	rad = earthrad * inz.radscale
	diam = 2.0 * rad
	canvas.fill_ellipse(earthx - rad, earthy - rad, diam, diam)
	canvas.restore_gstate()

def show_moon(mr, mg, mb):
	canvas.save_gstate()
	canvas.set_fill_color(mr, mg, mb)
	rad = moonrad * inz.radscale
	diam = 2.0 * rad
	canvas.fill_ellipse(moonx - rad, moony - rad, diam, diam)
	canvas.restore_gstate()

def hide_old_moon():
	canvas.save_gstate()
	canvas.set_fill_color(0,0,0)		# paint it as black as outer space
	rad = moonrad * inz.radscale
	diam = 2.0 * rad
	canvas.fill_ellipse(oldmx - rad, oldmy - rad, diam, diam)
	canvas.restore_gstate()


show_earth(er, eg, eb)

moonrad = 1.7374e6      # radius of moon
moonangle = math.radians(inz.moondegrees)    # position in radians
moonx = earthx + moondistance*math.cos(moonangle)
moony = earthy + moondistance*math.sin(moonangle)
oldmx = moonx
oldmy = moony

hide_old_moon()
show_moon(mr, mg, mb)

shipx = earthx + moondistance*inz.shipxmd
shipy = earthy + moondistance*inz.shipymd
oldx = shipx
oldy = shipy
d2e = math.hypot(shipx - earthx, shipy - earthy)
shipvx = inz.shipvx
shipvy = inz.shipvy

shipcolors = [(1,0,0), (0,1,0), (0.6,0.6,1), (1,1,0), (1,0,1), (0,1,1)]
shipcolor = 0
colorsteps = 0

def setshipcolor(i):
	if i in range(0, len(shipcolors)):
		colorset = shipcolors[i]
	else:
		colorset = (1,1,1)
	canvas.set_fill_color(colorset[0], colorset[1], colorset[2])

setshipcolor(shipcolor)

simtime = 0             # elapsed simulation time
dtime = inz.dtime       # time step for simulation
gravcon = -6.67430e-11
earthgrav = gravcon * 5.972e24
moongrav = gravcon * 7.342e22
# moon orbits counterclockwise 360 degrees/(27 days + 7 hr + 43 min + 12 sec)
moonstep = math.radians(dtime*360./(27.*24*60*60 + 7.*3600 + 43.*60 + 12.))

orbits = 0     # to count orbits around Earth
iters = 0
olditers = iters
starttime = time.process_time()
oldtime = starttime
plots = 0
ips = 0
maxips = 0
timestamp = time.asctime(time.localtime())
running = True

motion.start_updates()
logfile = open('tl-log.txt', 'a')		# open log file for append
logfile.write(timestamp)
logfile.write(f"\n{setupnum}: {inz.description}\n\n")

print()
print(timestamp)

while running:
	oldd2e = d2e
	d2e = math.hypot(shipx - earthx, shipy - earthy)
	if d2e < earthrad:
		show_earth(1,0,0)		# red crash site
		print("\n>>>>>>> Crashed on Earth ! <<<<<<<")
		break
	d2m = math.hypot(shipx - moonx, shipy - moony)
	if d2m < moonrad:
		show_moon(1,0,0)		# red crash site
		print("\n******  Lunar impact !  ******")
		break
	s2eaccel = dtime * earthgrav / (d2e * d2e * d2e)
	s2maccel = dtime * moongrav / (d2m * d2m * d2m)
	shipvx += s2eaccel * (shipx - earthx) + s2maccel * (shipx - moonx)
	shipvy += s2eaccel * (shipy - earthy) + s2maccel * (shipy - moony)
	oldshipy = shipy
	shipx += dtime * shipvx
	shipy += dtime * shipvy
	
	if oldshipy < earthy and shipy >= earthy:
		orbits += 1
		colorsteps += 1			# change ship color every orbit around Earth
		snapshot = grabsnap()				# snapshot and log current parameters
		json.dump(snapshot, logfile)
		logfile.write('\n\n')

	moonangle += moonstep
	moonx = earthx + moondistance*math.cos(moonangle)
	moony = earthy + moondistance*math.sin(moonangle)
	
	if abs(shipx - oldx) + abs(shipy - oldy) > apixel:
		shipcolor = colorsteps % len(shipcolors)
		setshipcolor(shipcolor)
		canvas.fill_pixel(shipx, shipy)
		oldx = shipx
		oldy = shipy
		hide_old_moon()
		show_moon(mr, mg, mb)
		oldmx = moonx
		oldmy = moony
		plots += 1

	if iters % inz.checktrigger == 0:
		newtime = time.process_time()   # calculate current iterations per second
		delta = newtime - oldtime
		if delta != 0:
			ips = int((iters - olditers)/delta)
			maxips = max(maxips, ips)
		oldtime = newtime
		olditers = iters
		moonunits = d2e / moondistance
		velocity = math.hypot(shipvx, shipvy)
		escapevelocity = math.sqrt(-2.0 * (earthgrav + moongrav) / d2e)

		if (velocity > escapevelocity) and (d2e > offscreen):
			show_earth(0,1,0)		# show green Earth then quit
			print("\n+++++++  Escape velocity !  +++++++")
			break

		gravx, gravy, gravz = motion.get_gravity()  # device orientation

		if gravz > 0.3:			# quit if user turns device screen downwards
			show_earth(1,1,0)		# show yellow Earth
			break

		if gravx > 0.8:     # output info if tipped to landscape
		  print(f"{moonunits:6.2f} moonu @ {velocity:7.0f} mps")

	simtime += dtime
	iters += 1

motion.stop_updates()
logfile.close()

stoptime = time.process_time()
elapsedtime = stoptime - starttime
if elapsedtime == 0:
	elapsedtime = 1.0
itrate = int(iters / elapsedtime)
plotrate = int(plots / elapsedtime)

print()
print(f"{setupnum}: {inz.description}\n",
      f"{iters} iterations in {int(elapsedtime)} process seconds\n",
      f"avg.ips={itrate}   last.ips={ips}   max.ips={maxips}\n",
      f"plot.rate={plotrate}    orbits={orbits}\n")
print(f"{moonunits:6.2f} moonu @ {velocity:7.0f} mps")

# end.
