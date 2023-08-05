
# needs polishing
# old file
# please update, future me

# --- libs ---
import pygame as pg
import fish
import os
from random import randint


# --- class --- 
class PersonAnimation:
	def __init__(self):
		
		names = ["graverobber", "steamman", "woodcutter"] #,"woman"]
		self.name = names[randint(0, len(names)-1)]

		path = os.path.join(os.getcwd(), "assets", self.name)
		dist = 48

		self.img_running = []
		self.img_idle = []
		self.img_damage = []
		self.img_jump = []
		self.img_standard = pg.image.load(os.path.join(path, self.name + ".png"))


		for i in range(4):
			self.img_idle.append(self.crop(pg.image.load(os.path.join(path, "_idle.png")), (40,64,-dist*i,0)))
		
		for i in range(6):
			self.img_running.append(self.crop(pg.image.load(os.path.join(path, "_run.png")), (40,64,-dist*i,0)))

		for i in range(1,2):
			self.img_damage.append(self.crop(pg.image.load(os.path.join(path, "_hurt.png")), (40,64,-dist*i,0)))

		l = []
		for i in range(6):
			l.append(self.crop(pg.image.load(os.path.join(path, "_jump.png")), (40,64,-dist*i,0)))

		self.img_jump = [[l[0], l[1], l[2]], [l[3]], [l[4], l[5]] ]


		self.img = list(self.img_running)
		self.img_count = 0
		self.pic = self.img[self.img_count]

		self.timer = 0
		self.tick = 8
		self.state = ""
		self.d_state = ""
		self.place = (0,0)
		self.ori = "left"

	def crop(self, img, size):
		
		cImg = pg.Surface((size[0], size[1]))
		cImg.blit(img, (size[2], size[3]))

		return cImg


	def switch_animation(self, state):
		self.img_count = 0
		
		if state == "idle":
			self.img = list(self.img_idle)

		elif state == "jump":
			self.img = list(self.img_jump[0])

		elif state == "left":
			self.img = list(self.img_running)

		elif state == "right":
			self.img = list(self.img_running)

		else:
			self.img = list(self.img_jump[1])

		
	def animate(self, platform):
		
		# - close to ground -
		if not self.state:

			for i in range(len(platform)):
				if platform[i] - self.place[1] <= 120:
					self.img = self.img_jump[2]


		if self.timer % self.tick == 0:
			self.img_count += 1
		
			if self.img_count >= len(self.img) and self.state != "jump":
				self.img_count = 0
		
		self.timer += 1

		# - desiered state -
		if self.state != self.d_state:
			self.pic = self.img_standard
			self.state = self.d_state
			self.switch_animation(self.state)
		
		
		#print(len(self.img), self.img_count)
		self.pic = self.img[self.img_count]

		# - jump -
		if self.state == "jump" and self.img_count == len(self.img)-1:
			self.timer = 1
			self.img_count == len(self.img)-1
			self.pic = self.img_jump[1][0]


	def draw(self, win, place):
		self.place = place
		if self.ori == "left":
			self.pic = pg.transform.flip(self.pic, True, False)

		win.blit(self.pic, place)