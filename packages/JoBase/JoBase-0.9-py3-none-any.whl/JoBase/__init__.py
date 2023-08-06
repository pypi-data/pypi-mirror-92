"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

# Welcome to JoBase.
# This is a Python educational resource for beginner coders.

import arcade, os

from arcade.resources import *

from .setup import SCREEN
from .setup import MOUSE
from .setup import KEY

from .engine import DYNAMIC
from .engine import STATIC
from .engine import KINEMATIC
from .engine import INFINITE

from .engine import Engine
from .engine import Pin_Joint
from .engine import Spring_Joint
from .engine import Gear_Joint
from .engine import Groove_Joint
from .engine import Pivot_Joint
from .engine import Motor_Joint

from .draw import Point
from .draw import Line
from .draw import Strip
from .draw import Shape
from .draw import Circle
from .draw import Box
from .draw import Image
from .draw import Text

from .math import Distance
from .math import Angle
from .math import Direction
from .math import Random
from .math import Random_Angle
from .math import Random_Color
from .math import Random_Alpha_Color

from .data import List
from .data import File
from .data import Sound

from .point import Rotate_Points
from .point import Scale_X_Points
from .point import Scale_Y_Points
from .point import Scale_Points
from .point import Center_X_Of_Points
from .point import Center_Y_Of_Points
from .point import Left_Of_Points
from .point import Top_Of_Points
from .point import Right_Of_Points
from .point import Bottom_Of_Points

print('Welcome to JoBase. Please visit the official website \'jobase.org\' for '
      'tutorials and documentation.')

for name in dir(arcade.color):
    if not name.startswith('__'):
        globals()[name] = getattr(arcade.color, str(name))

for name in dir(SCREEN):
    if name.startswith('CURSOR_'):
        globals()[name[7:]] = getattr(SCREEN, name)
        
def Random_Screen_X():
    return Random(0, SCREEN.width)
    
def Random_Screen_Y():
    return Random(0, SCREEN.height)
    
def Random_Screen_Pos():
    return Random_Screen_X(), Random_Screen_Y()

def run():
    arcade.run()
