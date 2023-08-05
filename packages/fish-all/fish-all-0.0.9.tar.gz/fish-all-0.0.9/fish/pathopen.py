
# --- libs ---
import pygame as pg
from multiprocessing import Pool
import easygui
import os


"""
pygame blocks main thread for other windows
so a new thread is opened and execute the following lines
"""


# --- function ---
def openfilebox(path):
	r = easygui.fileopenbox(title='amok', default=path)
	return r


def get_path(path):
	
	path = os.path.dirname(path)

	with Pool(1) as p:
		res = p.map(openfilebox, [path])
		print(res)

	return res[0]