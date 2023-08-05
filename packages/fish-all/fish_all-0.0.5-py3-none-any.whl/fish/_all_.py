
#AUTOMATED FILE
#DO NOT EDIT
#VALTERT
VERSION = "version 0.8.2"

#--- Imports ---
from .screen import BaseScreen
from .screen import Error
from .screen import PopMsg
from .animate.person import PersonAnimation
from .animate.general import Animation
from .database import Database
from .transform import change_color
from .transform import rotate
from .gui.button import Button
from .gui.label import Label
from .gui.gallery import Gallery
from .gui.inp import connectInputs
from .gui.inp import Input
from .pathopen import get_path
from .pathopen import openfilebox
from .engine.movement import PlayerMovement
from .foo import inRange
from .foo import intersection
from .foo import isNaN
from .foo import sharprect
from .foo import trimfolderlist
from .foo import Onepress
from .console.color import color

#--- Assigns ---
BaseScreen = BaseScreen
Error = Error
PopMsg = PopMsg
class animate:
    PersonAnimation = PersonAnimation
    Animation = Animation
Database = Database
change_color = change_color
rotate = rotate
class gui:
    Button = Button
    Label = Label
    Gallery = Gallery
    connectInputs = connectInputs
    Input = Input
get_path = get_path
openfilebox = openfilebox
class engine:
    PlayerMovement = PlayerMovement
inRange = inRange
intersection = intersection
isNaN = isNaN
sharprect = sharprect
trimfolderlist = trimfolderlist
Onepress = Onepress
class console:
    color = color
