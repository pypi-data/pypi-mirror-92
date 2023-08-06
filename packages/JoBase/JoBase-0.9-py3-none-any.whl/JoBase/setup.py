import arcade, sys

from .collision import collide

from .math import Angle
from .math import Distance
from .math import Direction

module = sys.modules['__main__']

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class Screen(arcade.Window):
    
    def __init__(self):
        super().__init__(800, 600, 'JoBase', resizable = True,
                         antialiasing = False)
                
        # The code above gets all the colors stored in 'arcade.color' and makes
        # global variables with the same name.        
        
        self.engines = []
        self.module = module
        self.resize = 0
        self.time = 0
        self.quit = 0
        self._color = (255, 255, 255)
        self._rate = 60
        self._fullscreen = 0
        self._visible = 1
        
        arcade.set_background_color(self._color)
        self.set_update_rate(1 / 60)
                
        # The code above finds all the variables starting with 'CURSOR_' and
        # makes new global variables without the 'CURSOR_' prefix.
                
    def collide(self, other):
        # This function checks if 'other' is on the screen.
        return collide(self.boundary(), other.boundary())
        
    def boundary(self):
        # This dictionary is eventually passed into the collision function.
        
        return {'points': arcade.get_rectangle_points(self.width / 2,
                                                      self.height / 2,
                                                      self.width, self.height),
                'type': 'polygon'}
    
    def _get_visible(self):
        return self._visible
    
    def _set_visible(self, value: bool):
        # 'set_visible' is an arcade function.
        self.set_visible(value)
        self._visible = value
        
    visible = property(_get_visible, _set_visible)
    
    def _get_x(self):
        # 'get_location' is an arcade function.
        return self.get_location()[0]
    
    def _set_x(self, value: float):
        # 'set_location' is an arcade function.
        self.set_location(value, self.y)
        
    x = property(_get_x, _set_x)
        
    def _get_y(self):
        return self.get_location()[1]
    
    def _set_y(self, value: float):
        self.set_location(self.x, value)
        
    y = property(_get_y, _set_y)
    
    def _get_title(self):
        return self.caption
    
    def _set_title(self, value: str):
        self.set_caption(value)
        
    title = property(_get_title, _set_title)
    
    def _get_fullscreen(self):
        return self._fullscreen
    
    def _set_fullscreen(self, value: bool):
        self.set_fullscreen(value)
        self.resize = 1
        # 'resize' becomes true when it enters fullscreen mode.
        
    fullscreen = property(_get_fullscreen, _set_fullscreen)
    
    def _get_rate(self):
        return self._rate
    
    def _set_rate(self, value: float):
        # We write '1 / value' to make the user set the frames per second.
        self.set_update_rate(1 / value)
        self._rate = value
        
    rate = property(_get_rate, _set_rate)
    
    def _get_color(self):
        return self._color
    
    def _set_color(self, value: arcade.Color):
        arcade.set_background_color(value)
        self._color = value
        
    color = property(_get_color, _set_color)
        
    def centralize(self):
        # A JoBase user could just use 'center_window'.
        self.center_window()
        
    def exit(self):
        self.quit = 1
        
    def on_update(self, time):
        self.time = 1 / time
        
        arcade.start_render()
        
        if 'loop' in dir(module):
            module.loop()
            
        for engine in self.engines:
            engine.update()
        
        KEY.press = 0
        KEY.release = 0
        SCREEN.resize = 0
        MOUSE.press = 0
        MOUSE.release = 0
        MOUSE.up = 0
        MOUSE.down = 0
        MOUSE.move = 0
        MOUSE.scroll = 0
        
        if self.quit:
            arcade.close_window()
            
        """
        When the user presses the close button, the 'module.loop()' function
        runs once before the window closes.
        """
        
    def on_close(self):
        self.quit = 1
        
    def on_mouse_motion(self, x, y, dx, dy):
        MOUSE.move = 1
        MOUSE.x_change = x - MOUSE._x
        MOUSE.y_change = y - MOUSE._y
        MOUSE._x = x
        MOUSE._y = y        

    def on_mouse_scroll(self, x, y, button, direction):
        MOUSE.scroll = 1
        
        if direction == 1.0:
            MOUSE.scroll_up = 1
            
        elif direction == -1.0:
            MOUSE.scroll_down = 1

    def on_mouse_press(self, x, y, button, modifiers):
        MOUSE.press = 1
        
        if button == 1:
            MOUSE.left = 1
            
        elif button == 4:
            MOUSE.right = 1
            
        elif button == 2:
            MOUSE.middle = 1

    def on_mouse_release(self, x, y, button, modifiers):
        MOUSE.release = 1
        
        if button == 1:
            MOUSE.left = 0
            
        elif button == 4:
            MOUSE.right = 0
            
        elif button == 2:
            MOUSE.middle = 0
        
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.resize = 1

    def on_key_press(self, key, modifiers):
        KEY.press = 1
        
        for keys in dir(arcade.key):
            if not keys.startswith('__') and key == getattr(arcade.key, keys):
                keys = keys.lower()
                setattr(KEY, keys, 1)
                
                if keys in alphabet:
                    if KEY.lshift or KEY.rshift:
                        KEY.text += keys.upper()
                        
                    else:
                        KEY.text += keys
                        
                elif keys == 'backspace':
                    KEY.text = KEY.text[:-1]
                    
                elif keys.startswith('num_') or keys.startswith('key_'):
                    KEY.text += keys[-1]
                
        # The code above finds all the values in 'arcade.key'. If a key is true,
        # we set the same JoBase key to true.

    def on_key_release(self, key, modifiers):
        KEY.release = 1
        
        for keys in dir(arcade.key):
            if not keys.startswith('__') and key == getattr(arcade.key,
                                                            str(keys)):
                keys = keys.lower()
                setattr(KEY, str(keys), 0)
                
class Key:
    
    def __init__(self):
        self.press = 0
        self.release = 0
        self.text = ''
        
        for keys in dir(arcade.key):
            if not keys.startswith('__'):
                keys = keys.lower()
                setattr(self, str(keys), 0)
                
        # The code above finds all the values in 'arcade.key' and makes a
        # JoBase key with the same name (lowercase).
        
    def clear(self):
        self.text = ''
        
class Mouse():
    
    def __init__(self):
        
        super()
        
        self.press = 0
        self.release = 0
        self.left = 0
        self.right = 0
        self.middle = 0
        self.scroll_up = 0
        self.scroll_down = 0
        self.move = 0
        self.scroll = 0
        self._x = 0
        self._y = 0
        self.x_change = 0
        self.y_change = 0
        self._visible = 1
        self._cursor = None
        
    def boundary(self):
        return {'x': self._x, 'y': self._y, 'type': 'point'}
    
    def _get_visible(self):
        return self._visible
    
    def _set_visible(self, value: bool):
        SCREEN.set_mouse_visible(value)
        self._visible = value
        
    visible = property(_get_visible, _set_visible)
    
    def _get_cursor(self):
        return self._cursor
    
    def _set_cursor(self, name):
        SCREEN.set_mouse_cursor(SCREEN.get_system_mouse_cursor(name))
        self._cursor = name
        
    cursor = property(_get_cursor, _set_cursor)
        
    def _get_x(self):
        return self._x
    
    def _set_x(self, value: float):
        SCREEN.set_mouse_position(round(value), round(self._y))
        
        self._x = value
        
    x = property(_get_x, _set_x)
    
    def _get_y(self):
        return self._y
    
    def _set_y(self, value: float):
        SCREEN.set_mouse_position(round(self._x), round(value))
        
        self._y = value
        
    y = property(_get_y, _set_y)
    
    def collide(self, other):
        return collide(self.boundary(), other.boundary())
    
    def angle(self, other):
        return Angle(self.x, self.y, other.x, other.y)

    def distance(self, other):
        return Distance(self.x, self.y, other.x, other.y)    
    
KEY = Key()
MOUSE = Mouse()
SCREEN = Screen()