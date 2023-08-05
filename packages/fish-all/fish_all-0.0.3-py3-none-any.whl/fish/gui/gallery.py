
# --- libs --- 
import pygame as pg
import fish
import os


# --- class ---
class Gallery:
	def __init__(self, x, y, w, h, color=(0,0,0),ES=80):
		self.ES = ES
		
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.color = color

		self.elements = {1:[]} #add dict to it, with surface and button
		self.freepos = [0,0]
		self.c = 1

		# display surfaces on buttons
		# in a container

		self.current_screen = 1
		self.avaliable_screen = 1

		leftimg = pg.image.load(os.path.join(os.path.dirname(__file__),'left.png'))
		self.left = fish.gui.Button(self.x+self.w*0.75,self.y-25,img=leftimg)
		self.left_highlight = fish.gui.Button(self.x+self.w*0.75,self.y-25,size=leftimg.get_size(), color=(255,255,255), highlight=(200,200,200))

		rightimg = pg.image.load(os.path.join(os.path.dirname(__file__),'right.png'))
		self.right = fish.gui.Button(self.x+self.w*0.92,self.y-25,img=rightimg)
		self.right_highlight = fish.gui.Button(self.x+self.w*0.92,self.y-25,size=rightimg.get_size(), color=(255,255,255), highlight=(200,200,200))




	def _resize(self, img):
		return pg.transform.scale(img, (int(self.ES*0.5), int(self.ES*0.5)))


	def _newpos(self):

		self.freepos[0] = self.freepos[0] + 1

		if self.freepos[0] * self.ES > self.w - self.ES:
			self.freepos[0] = 0
			self.freepos[1] = self.freepos[1] + 1


	def _maketext(self, text, x, y):
		
		mx = 8

		label = fish.gui.Label('<3', x+self.ES*0.05, y+self.ES*0.6, color=self.color, size=int(self.ES*0.15))

		tx = []

		if len(text) > mx:
			tx = [text[:mx]]
			if len(text[mx:]) > mx:
				tx.append(text[mx:mx*2])
			else:
				tx.append(text[mx:])

		else:
			tx = text

		label.set_text(tx)

		return label


	def add(self, l):
		
		# 50, 50 for every element

		for e in l:

			if self.freepos[1] >= round(self.h/self.ES):
				self.c += 1
				self.elements[self.c] = []
				self.freepos[1] = 0
				self.avaliable_screen += 1

			d = {}
			x = self.freepos[0]*self.ES+self.x+3
			y =self.freepos[1]*self.ES+self.y+3
			d['fullname'] = str(e[0])
			d['name'] = self._maketext(e[0], x,y)
			d['image'] = self._resize(e[1])
			d['button'] = fish.gui.Button(x, y, size=(self.ES,self.ES), color=(255,255,255), highlight=(200,200,200))
			d['pos'] = (x,y)
			
			self.elements[self.c].append(d)

			self._newpos()


	def draw(self, win):
		
		for elm in self.elements[self.current_screen]:
			
			elm['button'].draw(win)
			win.blit(elm['image'], (elm['pos'][0]+self.ES*0.05, elm['pos'][1]+self.ES*0.1))
			elm['name'].draw(win)

		fish.sharprect(win, self.color, [self.x, self.y, self.w, self.h], 5)
		
		self.left_highlight.draw(win)
		self.right_highlight.draw(win)
		self.left.draw(win)
		self.right.draw(win)


	def update(self):

		for elm in self.elements[self.current_screen]:
			if elm['button'].get_pressed():
				return elm

		if self.left.get_pressed():
			self.current_screen -= 1
			if self.current_screen < 1:
				self.current_screen = 1

		if self.right.get_pressed():
			self.current_screen += 1
			if self.current_screen > self.avaliable_screen:
				self.current_screen -= 1

		# highlight
		self.left_highlight.get_pressed()
		self.right_highlight.get_pressed()
		return 0