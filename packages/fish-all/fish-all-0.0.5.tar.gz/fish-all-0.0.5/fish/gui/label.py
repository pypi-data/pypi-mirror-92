
# --- libs --- 
from random import randint
import pygame as pg
import fish


# --- class ---
fonts_initialized = []
fonts = {}
class Label:
	def __init__(self, text, x, y, color=(0,0,255), font='freesansbold.ttf', size=20, base=False):
		self.x = x
		self.y = y

		self.text = str(text)
		self.color = color
		
		try:
			if str(font) + '<>' + str(size) in fonts_initialized:
				self.font = fonts[str(font) + '<>' + str(size)]
			else:
				self.font = pg.font.Font(font, size)
				fonts_initialized.append(str(font) + '<>' + str(size))
				fonts[str(font) + '<>' + str(size)] = self.font
		except Exception as e:
			
			print('\n'+str(e))
			print('\n' + fish.console.color.fg.red + 'Please initialize font in main' + fish.console.color.reset + '\n')
		

		self.fontname = font
		self.render = self.font.render(str(text), True, color)
		self.size = size

		if base:
			self.baseX = int(x)
			self.baseY = int(y)

		self.id = str(randint(100,999))

	def set_text(self, text):
		
		if type(text) is str:
			self.text = text
			self.render = self.font.render(str(text), True, self.color)
		else:
			self.text = str(text)
			self.render = []
			for i in text:
				self.render.append(self.font.render(str(i), True, self.color))


	def draw(self, win):

		if type(self.render) is pg.Surface:
			win.blit(self.render, (self.x, self.y))
		
		else:
			for i in range(len(self.render)):
				win.blit(self.render[i], (self.x, self.y + i*self.size*1.2))

	def get_size(self):
		return self.render.get_size()

	def get_info(self):
		return {'text':self.text, 'color':self.color, 'font':self.fontname, 'id':self.id}

	def update_info(self, iden='', text='', color='', font='', size=''):
		
		try:
			if iden != '':
				self.id = iden
			
			if size != '':
				self.size = int(size)

			if font != '':
				self.fontname = font

			self.font = pg.font.Font(self.fontname, self.size)
			
			if color != '':
				self.color = list(map(int, color.split(',')))

			if text != '':
				self.set_text(text)
			else:
				self.set_text(self.text)

			self.draw(pg.Surface((0,0)))

		except Exception as e:
			print('Error ' + str(e))