
# --- lib ---
import pygame as pg
import fish
from math import *


# --- player movement ---

# good for platformer
# collision with grounds
# in any direction

GRAVITY = 9.82
V0 = 60
TIMEOFFLIGHT = 5
FALLAMP = 0.1

# make an ability to change these properties

# --- class ---
class PlayerMovement:
	def __init__(self, x, y):
		self.x = x
		self.y = y

		self.w = 40
		self.h = 80

		self.top = [(self.x-self.w/2, self.y+self.h/2), (self.x+self.w/2, self.y+self.h/2)]
		self.buttom = [(self.x-self.w/2, self.y-self.h/2), (self.x+self.w/2, self.y-self.h/2)]
		self.left = [(self.x-self.w/2, self.y-self.h/2), (self.x-self.w/2, self.y+self.h/2)]
		self.right = [(self.x+self.w/2, self.y-self.h/2), (self.x+self.w/2, self.y+self.h/2)]

		self.marker_height = 1.8 #1.6
		self.left_marker = [(int(self.x-self.w/2), int(self.y+self.h/self.marker_height)), (int(self.x-self.w/2), int(self.y+self.h/3))]
		self.right_marker = [(int(self.x+self.w/2), int(self.y+self.h/self.marker_height)), (int(self.x+self.w/2), int(self.y+self.h/3))]


		# - move logic -
		self.t = 0
		self.jump = 0
		self.v = 5


	"""
	def _abbreviate_vector_(self, vek, lenght):

		try:
			lengtVec = sqrt(vek[0]**2 + vek[1]**2)
			n = lengtVec / lenght
			return (vek[0]/n, vek[1]/n)
		except ZeroDivisionError:
			return (0,0)
	"""

	def _round_(self, val, con):
		
		if val % con > con/2:
			return val+(con-val%con)
		else:
			return val-val%con


	def _check_collision_(self, lines):
		
		coll_res = []
		
		#player_lines = [self.left_marker, self.right_marker]
		#player_lines = [self.top, self.buttom, self.left, self.right]

		for l in lines:
			
			for pl in [self.left_marker, self.right_marker]:

				res = fish.intersection(pl, l)
				if res:
					coll_res.append(res)

		if len(coll_res) > 0:
			return coll_res

		else:
			return None


	def _collide_with_ground_(self, lines):

		coll_res = self._check_collision_(lines)
		
		#print(int(self.t))
		if int(self.t) not in range(-1, 1):
			if coll_res:
			
				high = coll_res[0]
				for res in coll_res:
					#pg.draw.circle(win, (255,0,0), res, 5) #collision cicles
					if res[1] < high[1]:
						high = list(res)
			
				self.y = high[1] - self.h/2
				self.jump = False


	def movePlayer(self, lines):
	
		# - move -
		keys = pg.key.get_pressed()
		if keys[pg.K_w] == 1:
			if not self.jump:
				self.jump = True
				self.t = 0
		if keys[pg.K_a] == 1:
			self.x -= self.v
		if keys[pg.K_d] == 1:
			self.x += self.v


		# - F(gravity) -
		# v=-g·t+v_0
		
		fall = -GRAVITY * self.t + V0
		self.y -= fall*FALLAMP

		if self.jump:
			self.t += 1/TIMEOFFLIGHT

			#if fall < - V0:
			#	self.jump = False

		else:
			self.t = 12.22


		# - F(normal) -
		self._collide_with_ground_(lines)


		# - update -
		self.top = [
			(int(self.x-self.w/2), int(self.y+self.h/2)), 
			(int(self.x+self.w/2), int(self.y+self.h/2))
		]
		
		self.buttom = [
			(int(self.x-self.w/2), int(self.y-self.h/2)), 
			(int(self.x+self.w/2), int(self.y-self.h/2))
		]
		
		self.left = [
			(int(self.x-self.w/2), int(self.y-self.h/2)), 
			(int(self.x-self.w/2), int(self.y+self.h/2))
		]
		
		self.right = [
			(int(self.x+self.w/2), int(self.y-self.h/2)), 
			(int(self.x+self.w/2), int(self.y+self.h/2))
		]

		self.left_marker = [
			(int(self.x-self.w/2), int(self.y+self.h/self.marker_height)), 
			(int(self.x-self.w/2), int(self.y+self.h/3))
		]
		
		self.right_marker = [
			(int(self.x+self.w/2), int(self.y+self.h/self.marker_height)), 
			(int(self.x+self.w/2), int(self.y+self.h/3))
		]


	def drawHitbox(self, win):

		pg.draw.line(win, (255,0,0), self.top[0], self.top[1], 5)
		pg.draw.line(win, (255,0,0), self.buttom[0], self.buttom[1], 5)
		pg.draw.line(win, (255,0,0), self.left[0], self.left[1], 5)
		pg.draw.line(win, (255,0,0), self.right[0], self.right[1], 5)

		# - center -
		pg.draw.circle(win, (0,255,255), (int(self.x), int(self.y)), 3)
		
		"""
		pg.draw.line(win, (0,255,0), self.left_marker[0], self.left_marker[1], 5)
		pg.draw.line(win, (0,255,0), self.right_marker[0], self.right_marker[1], 5)
		"""