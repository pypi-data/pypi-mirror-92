
# --- libs ---
import pygame as pg
import sys
import fish
import os


# --- basescreen ---
class BaseScreen:
	def __init__(self, draw, update, inputreg=None):
		self.draw = draw
		self.update = update
		self.inputreg = inputreg


	def run(self, win, clock):

		run = True #not equal to self.run()
		continue_ = True
		while run:

			self.draw(win)
			run, options = self.update()

			for evt in pg.event.get():
				if evt.type == pg.QUIT:
					run, continue_ = False, False

				if evt.type == pg.KEYDOWN:
					if self.inputreg:
						self.inputreg(evt)

			clock.tick(60)
			pg.display.update()

		return continue_, options


# --- error ---
class Error:
	def __init__(self, error):
		self.error = error
		self.l1 = fish.Label('ERROR MESSAGE', 10, 20, color=(0,0,0), size=40)
		self.l2 = fish.Label('', 10, 60, color=(0,0,0))
		self.l2.set_text(error)


	def run(self):

		win = pg.display.set_mode((400,400))
		pg.display.set_caption('ERROR')

		# from stackoverflow
		try:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			self.l2.set_text([self.error,exc_type, fname + ', line ' + str(exc_tb.tb_lineno)])
		except:
			pass


		while True:
			for evt in pg.event.get():
				if evt.type == pg.QUIT:
					sys.exit()

			win.fill((255,255,255))
			self.l1.draw(win)
			self.l2.draw(win)
			pg.display.update()


# --- pop measge ---
class PopMsg:
	def __init__(self, text, time, id_type=None, size=20, color=(0,0,0)):
		text = str(text)

		"""
		in main loop
	
		for i in popmesages:
			popmessages = i.show(win, popmessages)
		
		always have this running.

		when a new pop message shall appear then
		simply add it onto the list.

		"""
		info = pg.display.Info()
		w,h = info.current_w, info.current_h

		self.lb = fish.gui.Label(str(text), w/2-len(text)*size/2, h*0.4, size=size, color=color)
		self.time = time
		self.clock = 0

		# id type used for changing of pop of message i.e you have to zoom.
		# and stacking pop up messages is a bad idea.
		self.id_type = id_type


	def show(self, win, l=None):
		
		if self.time > self.clock:
			self.lb.draw(win)
		self.clock += 1

		if len(l) > 1:
			for i in l:
				if i.id_type == self.id_type: #i == self
					l.pop(l.index(i))

		return l


