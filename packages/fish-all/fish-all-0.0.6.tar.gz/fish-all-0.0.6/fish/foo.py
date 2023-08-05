
# --- libs ---
import pygame as pg


# --- functions ---
def isNaN(s):
	
	try:
		int(s)
		return True
	except ValueError: 
		return False


# --- in range ---
def inRange(comp, val1, val2, d=0):
	
	if int(val1) < int(val2):
		if int(comp) in range(int(val1)-d, int(val2)+d):
			return True
	else:
		if int(comp) in range(int(val2)-d, int(val1)+d):
			return True


def intersection(l,m):
	#global win

	"""
	:find sentence:
	y = ax + b
	a = (y2-y1)/(x2-x1)
	b = y - ax

	:substiotion:
	m into l
	la * x + lb = ma * x + mb
	x = (mb - lb)/(la - ma)

	y = a*res_x + lb

	:special cases:
	if lines is diagonal or horizontal
	this will result in a = 0

	just + 1 or some small number


	"""

	lx = l[0][0] - l[1][0]
	ly = l[0][1] - l[1][1]
	
	mx = m[0][0] - m[1][0]
	my = m[0][1] - m[1][1]

	oddCase = False

	try:
		la = ly/lx
	except ZeroDivisionError:
		lx = l[0][0] - l[1][0] + 0.1
		la = ly/lx
	
	try:
		ma = my/mx
	except ZeroDivisionError:
		mx = m[0][0] - m[1][0] + 0.1
		ma = my/mx

	lb = l[0][1] - la * l[0][0]
	mb = m[0][1] - ma * m[0][0]

	#print('y = '+str(la)+' x+ '+str(lb))
	#print('y = '+str(ma)+' x+ '+str(mb))

	x = (mb - lb)/(la - ma)
	y = la*x+lb

	# - only x and y in lines -
	#pg.draw.rect(win, (0,255,0), [l[0][0], l[0][1], l[1][0]-l[0][0], l[1][1]-l[0][1]], 5)
	if inRange(x, l[0][0], l[1][0], 1) and inRange(y, l[0][1], l[1][1], 1):
		
		if inRange(x, m[0][0], m[1][0], 1) and inRange(y, m[0][1], m[1][1], 1):
			return (int(x), int(y))	
	
	return None


# --- cool borders ---
def sharprect(win,color, rect, thickness=1):
	x,y,w,h = rect

	pg.draw.rect(win, color, [x-int(thickness/2),y-int(thickness/2),thickness,h+thickness])
	pg.draw.rect(win, color, [x-int(thickness/2),y-int(thickness/2),w+thickness,thickness])
	pg.draw.rect(win, color, [x+w-int(thickness/2),y-int(thickness/2),thickness,h+thickness])
	pg.draw.rect(win, color, [x-int(thickness/2),y+h-int(thickness/2),w+thickness,thickness])


# --- trim folder list for macos/darwin ---
def trimfolderlist(l):
	
	if '.DS_Store' in l:
		l.pop(l.index('.DS_Store'))

	return l


# --- wrong place ---
# --- pygame onepress key ---
class Onepress:
	def __init__(self, key, wait=200):
		self.wait = wait
		self.timer = 0
		self.key = key

	def get_pressed(self):
		keys = pg.key.get_pressed()
		if keys[self.key] == 1:
			if self.timer < 0:
				self.timer = int(self.wait)
				return True

		self.timer -= 1
		return False

