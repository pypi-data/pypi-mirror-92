

"""

pygame.key.start_text_input() -> None

        start handling IME compositions

    Start receiving pygame.TEXTEDITING and pygame.TEXTINPUT events to handle IME.

    A pygame.TEXTEDITING event is received when an IME composition is started or changed. It contains the composition text, length, and editing start position within the composition (attributes text, length, and start, respectively). When the composition is committed (or non-IME input is received), a pygame.TEXTINPUT event is generated.

    Normal pygame.TEXTINPUT events are not dependent on this.

    New in pygame 2.

pygame.key.stop_text_input() -> None

        stop handling IME compositions


"""




# --- libs --- 
from random import randint
import pygame as pg


# --- class ---
currentInput = {}

class Input:
	def __init__(self, x, y, w=200, h=40, color=(255,255,255), font='freesansbold.ttf', fontsize=20, fontcolor=(0,0,0), border=True, erase=False):
		
		self.square = [x, y, w, h]
		self.color = color

		self.border = border
		self.on = False
		self.text = ''

		# - font -
		self.font = pg.font.Font(font, fontsize)
		self.fontcolor = fontcolor
		self.screen = pg.Surface((w-4, h-4))
		self.fontsize = fontsize

		self.id = str(randint(100,99999))
		self.next = None
		self.erase = erase
		self.enter = False


	def draw(self, win):
		
		self.screen.fill(self.color)
		if not self.border:
			pg.draw.rect(win, self.color, self.square)
		else:
			pg.draw.rect(win, self.color, self.square)
			pg.draw.rect(win, self.fontcolor, self.square, 2)

		if len(self.text) > 0:
			render = self.font.render(self.text, True, self.fontcolor)
			self.screen.fill(self.color)
			
			r = render.get_size()[0] + 5

			if r < self.square[2]:
				self.screen.blit(render, (5,5))
			else:
				self.screen.blit(render, (self.square[2]-r,5))

		win.blit(self.screen, (self.square[0]+2, self.square[1]+2))


	def register_event(self, evt):
		
		if self.on and evt:
			
			if evt.key == pg.K_BACKSPACE:
				self.text = self.text[:-1]

				"""
				elif evt.key == pg.K_RETURN:
					print(self.text)
				"""
	
			elif evt.key == pg.K_TAB:
				currentInput[self.next[0]] = (True, self.next[0], self.next[1])
				self.on = False

			elif evt.key == pg.K_RETURN:
				self.enter = True

			else:
				self.text += evt.unicode


	def update(self):
		global currentInput
		

		# - detect -
		ms = pg.mouse.get_pressed()
		pos = pg.mouse.get_pos()
		
		if ms[0] == 1:
			if pos[0] in range(round(self.square[0]), round(self.square[0]+self.square[2])) and pos[1] in range(round(self.square[1]), round(self.square[1]+self.square[3])):
				self.on = True
				if self.erase:
					self.set_text('')
			else:
				self.on = False

		if self.next:
			
			#print(currentInput)
			if currentInput[self.next[0]][2] == self.id:
				if currentInput[self.next[0]][0]:
					currentInput[self.next[0]] = (False, self.next[0], self.id)
					self.on = True

		if self.enter:
			self.enter = False
			return True


	def get_text(self):
		return self.text

	def set_text(self, text):
		self.text = str(text)

	def get_size(self):
		return (self.square[2], self.square[3])

	def get_info(self):
		return {'x':self.square[0], 'y':self.square[1], 'w':self.square[2], 'h':self.square[3],'text':self.text, 'color':self.color, 'font':self.font, 'fontsize':self.fontsize, 'id':self.id, 'size':(self.square[2],self.square[3]), 'border':self.border}


# --- function ---
ident = 0

def connectInputs(inputs): 
	global ident, currentInput

	l = []

	# set next to the next input
	# last gets first
	# so it goes full cirlce

	# in each class when tab is pressed
	# the id and "currentInput" is set to the new one.
	# for each update it is checked

	ident += 1


	for i in range(len(inputs)-1):
		inputs[i].next = (ident,inputs[i+1].id)

	inputs[-1].next = (ident,inputs[0].id)

	currentInput[ident] = (False,-1,-1)
