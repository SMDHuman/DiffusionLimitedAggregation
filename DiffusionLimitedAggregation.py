from graphics import *
from time import sleep
from random import randint
from math import hypot, sin, cos, radians
from opensimplex import OpenSimplex

def hlsRGB(x):
	x = x % 1
	rgb = [0.0, 0.0, 0.0]
	if(x < 1/2):
		rgb[0] = 1 - x / (1/2)
		rgb[1] = x / (1/2)

	elif(x <= 1):
		rgb[1] = 1 - (x - 1/2) / (1/2)
		rgb[2] = x
	return(rgb)

class Ball():
	def __init__(self, win, r = 10):
		self.win = win
		self.winX = self.win.width
		self.winY = self.win.height

		x = randint(0, self.winX)
		if(self.winX / 3 < x < self.winX * 2 / 3):
			y = [randint(0, self.winY/3), randint(self.winY*2 /3, self.winY)][randint(0, 1)]
		else:
			y = randint(0, self.winY)

		self.r = r
		self.speed = 3
		self.mag = 1/20

		self.body = Circle(Point(x, y), self.r)
		self.body.setWidth(1)

		self.seed = randint(0, 1000) / 10

		self.enable = 1

	def update(self, atoms, t):
		if(self.enable):
			sX = self.getX()
			sY = self.getY()

			v = (os.noise2d(self.seed, t) * 360) + 360
			x = cos(radians(v)) * self.speed
			y = sin(radians(v)) * self.speed
			self.body.move(x, y)

			if(sX  < 0):
				self.moveTo(self.winX, sY)
			if(sY < 0):
				self.moveTo(sX, self.winY)
			if(sX  > self.winX):
				self.moveTo(0, sY)
			if(sY> self.winY):
				self.moveTo(sX, 0)

			R = (self.r * 2)
			for atom in atoms:
				if(atom != self and atom.enable == 0):
					dist = hypot(sX - atom.getX(), sY - atom.getY())
					if(dist < R): return(1)
		return(0)

	def moveTo(self, x, y):
		bX = self.body.p1.getX() + self.r
		bY = self.body.p1.getY() + self.r
		self.body.move(x - bX, y - bY)

	def getX(self):
		return(self.body.p1.getX() + self.r)

	def getY(self):
		return(self.body.p1.getY() + self.r)

winX = 600
winY = 600
win = GraphWin("DLA", winX, winY, autoflush = False)
os = OpenSimplex(randint(0, 1000))
r = 5
dt = 0.01
dc = 0.0025

atoms = [Ball(win, r) for i in range(150)]
atoms[0].enable = 0
atoms[0].moveTo(winX / 2, winY / 2)
atoms[0].body.setFill("red")
atoms[0].body.draw(win)

t = 0
c = 0
while(win.isOpen()):
	for i in range(100):
		for atom in atoms:
			stat = atom.update(atoms, t)
			if(stat):
				c += dc
				rgb = hlsRGB(c)
				color = color_rgb(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
				atom.body.setFill(color)
				atom.body.draw(win)
				atom.enable = 0
				atoms.append(Ball(win, r))
	t += dt


	win.update()
