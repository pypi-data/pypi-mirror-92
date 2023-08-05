
# helper class to handle animations
# animationhandler


# --- libs ---
import pygame as pg
import fish
import os, math
from random import randint


# --- class --- 
class Animation:
	def __init__(self, name, total, tick):
	
		self.images = []

		for i in range(total):
			self.images.append(pg.image.load(os.path.join(os.getcwd(), "assets", name, name+str(i)+".png")).convert_alpha())

		self.pic = self.images[0]
		self.picCount = 0

		self.timer = randint(0,50)
		self.tick = tick
		self.name = name

	def draw(self, win, place):
		if self.timer % self.tick == 0:
			self.picCount += 1
			if self.picCount > len(self.images)-1:
				self.picCount = 0
			self.pic = self.images[self.picCount]

		
		self.timer += 1
		win.blit(self.pic, place)