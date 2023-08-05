
# --- libs --- 
from random import randint
import pygame as pg

# --- class ---
class Button:
	def __init__(self, x, y, img=None, size=None, color=(0,0,150),highlight=None,base=None, drawbackground=True):
		
		# - ui -
		self.x = x
		self.y = y
		self.color = color
		self.ogColor = tuple(color)

		self.tp = 'not declared'
		
		if img:
			self.tp = 'image'
			self.w, self.h = img.get_size()
			self.img = img

		elif size:
			self.tp = 'size'
			self.w = size[0]
			self.h = size[1]

		else:
			print('Please enter a size or an image')

		self.id = str(randint(100,999))

		# - mechanics -
		self.press = False
		self.highlight = highlight
		if base:
			self.baseX = int(x)
			self.baseY = int(y)
		self.on = True
		self.drawbackground = drawbackground
		self.hover = False


	def draw(self, win, correction=None):
		
		if correction:
			x = self.x - correction[0]
			y = self.y - correction[1]

		else:
			x = self.x
			y = self.y


		if self.tp == 'image':
			win.blit(self.img, (x, y))
		
		elif self.tp == 'size':
			if self.drawbackground:
				pg.draw.rect(win, self.color, [x, y, self.w, self.h])
			else:
				if self.color != self.ogColor:
					pg.draw.rect(win, self.color, [x, y, self.w, self.h])


	
	def get_pressed(self):

		if self.tp != 'not declared' and self.on:
			
			mouse_pos = pg.mouse.get_pos()

			if mouse_pos[0] in range(round(self.x), round(self.x + self.w)) and mouse_pos[1] in range(round(self.y), round(self.y + self.h)):
		
				self.hover = True
				if self.highlight:
					self.color = self.highlight

				if self.press and pg.mouse.get_pressed()[0] == 0:
					self.press = False
					return True

				if pg.mouse.get_pressed()[0] == 1:
					self.press = True

			else:
				self.hover = False
				self.press = False
				self.color = self.ogColor

	def get_size(self):
		return (self.w, self.h)

	def get_info(self):
		return {'x':self.x, 'y':self.y, 'w':self.w, 'h':self.h, 'id':self.id, 'highlight':self.highlight, 'size':self.get_size()}
