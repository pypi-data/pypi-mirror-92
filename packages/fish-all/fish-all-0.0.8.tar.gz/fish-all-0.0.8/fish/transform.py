
# --- libs ---
from PIL import Image
import os
import pygame as pg


# --- rotate image ---
def rotate(name, angle_range):

	r_images = []
	image = Image.open(name)

	for i in range(angle_range[0], angle_range[1]):
		
		image_copy = image.copy()
		image_copy = image_copy.rotate(i)

		mode = image_copy.mode
		size = image_copy.size
		data = image_copy.tobytes()

		r_images.append(pg.image.fromstring(data, size, mode))
	
	return r_images


# --- functions ---
# only works for pygame surfaces
def change_color(surface, color):
   
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pg.Color(r, g, b, a))

# credit to stackoverflow user 'skrx'
