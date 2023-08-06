import arcade, math, copy, pymunk, warnings

from .collision import collide

from .point import Rotate_Points
from .point import Scale_X_Points
from .point import Scale_Y_Points
from .point import Center_X_Of_Points
from .point import Center_Y_Of_Points
from .point import Left_Of_Points
from .point import Top_Of_Points
from .point import Right_Of_Points
from .point import Bottom_Of_Points

from .math import Angle
from .math import Distance
from .math import Direction

class Pymunk:
    
    def __init__(self):
        self.engine = None
        self.shape = None
        self.body = None
        self.max_x_speed = 0
        self.max_y_speed = 0
        self.moment = None

class Base(object):

    def collide(self, other):
        if self.pymunk.engine is other.pymunk.engine is not None:
            return self.pymunk.engine.collide(self, other)
            
        return collide(self.boundary(), other.boundary())
    
    def copy(self):
        return copy.deepcopy(self)
    
    def angle(self, other):
        return Angle(self.x, self.y, other.x, other.y)

    def distance(self, other):
        return Distance(self.x, self.y, other.x, other.y)
    
    def on_ground(self):# This is a copied, complicated Arcade function.
        grounding = {'normal': pymunk.Vec2d.zero(),
                     'penetration': pymunk.Vec2d.zero(),
                     'impulse': pymunk.Vec2d.zero(),
                     'position': pymunk.Vec2d.zero(),
                     'body': None}

        def f(arbiter):
            n = -arbiter.contact_point_set.normal
            
            if n.y > grounding['normal'].y:
                
                grounding['normal'] = n
                grounding['penetration'] = -arbiter.contact_point_set.points[0].distance
                grounding['body'] = arbiter.shapes[1].body
                grounding['impulse'] = arbiter.total_impulse
                grounding['position'] = arbiter.contact_point_set.points[0].point_b

        self.pymunk.body.each_arbiter(f)

        return grounding['body'] is not None
    
    def apply_impulse(self, x_impulse: float, y_impulse: float,
                      x_point: float = 0, y_point: float = 0):
        self.pymunk.body.apply_impulse_at_local_point((x_impulse, y_impulse),
                                                      (x_point, y_point))
        
    def apply_force(self, x_force: float, y_force: float, x_point: float = 0,
                    y_point: float = 0):
        
        self.pymunk.body.apply_force_at_local_point((x_force, y_force),
                                                    (x_point, y_point))    
        
    def _get_max_x_speed(self):
        return self.pymunk.max_x_speed
    
    def _set_max_x_speed(self, value: float):
        self.pymunk.max_x_speed = value
        
    max_x_speed = property(_get_max_x_speed, _set_max_x_speed)
    
    def _get_max_y_speed(self):
        return self.pymunk.max_x_speed
    
    def _set_max_y_speed(self, value: float):
        self.pymunk.max_y_speed = value
        
    max_y_speed = property(_get_max_y_speed, _set_max_y_speed)
    
    def _get_x_speed(self):
        return self.pymunk.body.velocity[0]
    
    def _set_x_speed(self, value: float):
        self.pymunk.body.velocity = (value, self.pymunk.body.velocity[1])
        
    x_speed = property(_get_x_speed, _set_x_speed)
    
    def _get_y_speed(self):
        return self.pymunk.body.velocity[1]
    
    def _set_y_speed(self, value: float):
        self.pymunk.body.velocity = (self.pymunk.body.velocity[0], value)
        
    y_speed = property(_get_y_speed, _set_y_speed)
        
    def kill(self):
        if self.array is not None:
            self.array.remove(self)
            
        if self.pymunk.engine is not None:
            self.pymunk.engine.remove(self)
            
        del self
        
    def _get_x(self):
        return self.sprite.center_x
    
    def _set_x(self, value: float):
        if self.pymunk.engine is not None:
            self.pymunk.body.position = value, self.pymunk.shape.body.position.y
            self.pymunk.engine.space.reindex_shapes_for_body(self.pymunk.shape.body)
            self.x_speed = 0
            
        else:
            self.sprite.center_x = value
            
    x = property(_get_x, _set_x)

    def _get_y(self):
        return self.sprite.center_y
    
    def _set_y(self, value: float):
        if self.pymunk.engine is not None:
            self.pymunk.body.position = self.pymunk.shape.body.position.x, value
            self.pymunk.engine.space.reindex_shapes_for_body(self.pymunk.body)
            self.y_speed = 0
            
        else:
            self.sprite.center_y = value
            
    y = property(_get_y, _set_y)
    
    def _get_rotation(self):
        return self.sprite.angle
    
    def _set_rotation(self, value: float):
        if self.pymunk.engine is not None:
            self.pymunk.body.angle = math.radians(value)
            self.pymunk.engine.space.reindex_shapes_for_body(self.pymunk.body)
            
        else:
            self.sprite.angle = value
    
    rotation = property(_get_rotation, _set_rotation)    
    
class Point(Base):
    
    def __init__(self, x: float = 100, y: float = 100, color: arcade.Color = (0, 0, 0),
                 size: float = 10, rotation: float = 0):

        self._color = color
        self._size = size
        self.pymunk = Pymunk()
        self.array = None
        
        self.update(x, y, rotation)
        
    def draw(self):
        self.sprite.program['Angle'] = self.sprite._angle
        self.sprite.draw()
        
    def boundary(self):
        return {'points': self.get_corners(),
                'type': 'polygon'}
    
    def get_corners(self):
        return arcade.get_rectangle_points(self.sprite.center_x,
                                           self.sprite.center_y,  self._size,
                                           self._size)
    
    def update(self, x = None, y = None, angle = None):
        
        if x is None: x = self.sprite.center_x
        if y is None: y = self.sprite.center_y
        if angle is None: angle = self.sprite.angle
            
        self.shape = arcade.create_rectangle_filled(0, 0, self._size,
                                                    self._size, self._color)
        
        self.sprite = arcade.ShapeElementList()
        self.sprite.append(self.shape)
        
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.angle = angle
        
        if self.pymunk.engine is not None:
            self.pymunk.engine.refresh(self)        
        
    def get_moment(self, mass):
        return pymunk.moment_for_box(mass, (self._size, self._size))
    
    def get_shape(self, body):
        return pymunk.Poly.create_box(body, (self._size, self._size))
        
    def _get_top(self):
        return Top_Of_Points(self.get_corners())
    
    def _set_top(self, value: float):
        distance = value - self.top
        
        self.sprite.center_y += distance
        
    top = property(_get_top, _set_top)
    
    def _get_bottom(self):
        return Bottom_Of_Points(self.get_corners())
    
    def _set_bottom(self, value: float):
        distance = value - self.bottom
        
        self.sprite.center_y += distance
        
    bottom = property(_get_bottom, _set_bottom)
    
    def _get_left(self):
        return Left_Of_Points(self.get_corners())
    
    def _set_left(self, value: float):
        distance = value - self.left
        
        self.sprite.center_x += distance
        
    left = property(_get_left, _set_left)
    
    def _get_right(self):
        return Right_Of_Points(self.get_corners())
    
    def _set_right(self, value: float):
        distance = value - self.right
        
        self.sprite.center_x += distance
        
    right = property(_get_right, _set_right)
    
    def _get_size(self):
        return self._size
    
    def _set_size(self, value: float):
        if self._size is not value:
            self._size = value
        
            self.update()
            
    size = property(_get_size, _set_size)
    
    def _get_color(self):
        return self._color
    
    def _set_color(self, value: arcade.Color):
        if self._color is not value:
            self._color = value
        
            self.update()
            
    color = property(_get_color, _set_color)
       
class Line(Base):
    
    def __init__(self, x1: float = 0, y1: float = 0, x2: float = 100,
                 y2: float = 100, thickness: float = 1,
                 color: arcade.Color = (0, 0, 0), rotation: float = 0):
        
        x = (x2 + x1) / 2
        y = (y2 + y1) / 2

        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._thickness = thickness
        self._color1 = color
        self._color2 = color
        self.pymunk = Pymunk()
        self.array = None

        self.update(x, y, rotation)
        
    def draw(self):
        self.sprite.program['Angle'] = self.sprite._angle
        self.sprite.draw()
        
    def boundary(self):
        return {'points': self.get_corners(),
                'type': 'polygon'}
    
    def get_corners(self):
        points = self.get_current()
        points = Rotate_Points(((points[0][0] + self.sprite.center_x,
                                 points[0][1] + self.sprite.center_y),
                                (points[1][0] + self.sprite.center_x,
                                 points[1][1] + self.sprite.center_y)),
                                self.sprite.angle, self.sprite.center_x,
                                self.sprite.center_y)

        return arcade.get_points_for_thick_line(points[0][0], points[0][1],
                                                points[1][0], points[1][1],
                                                self._thickness)
    def get_current(self):
        x = (self._x2 + self._x1) / 2
        y = (self._y2 + self._y1) / 2
                        
        return (self._x1 - x, self._y1 - y), (self._x2 - x, self._y2 - y)
    
    def update(self, x = None, y = None, angle = None):
                
        if x is None: x = self.sprite.center_x
        if y is None: y = self.sprite.center_y
        if angle is None: angle = self.sprite.angle
                
        self.shape = arcade.create_lines_with_colors(
            self.get_current(), [self._color1, self._color2],
            line_width = self._thickness)
        
        self.sprite = arcade.ShapeElementList()
        self.sprite.append(self.shape)
        
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.angle = angle
        
        if self.pymunk.engine is not None:
            self.pymunk.engine.refresh(self)
            
    def get_moment(self, mass):
        points = self.get_current()
        
        return pymunk.moment_for_poly(mass, arcade.get_points_for_thick_line(
            points[0][0], points[0][1], points[1][0], points[1][1],
            self._thickness))
    
    def get_shape(self, body):
        points = self.get_current()
        
        return pymunk.Poly(body, arcade.get_points_for_thick_line(
            points[0][0], points[0][1], points[1][0], points[1][1],
            self._thickness))
    
    def _get_points(self):
        return ((self._x1, self._y1), (self._x2, self._y2))
    
    def _set_points(self, value: arcade.PointList):        
        self._x1 = value[0][0]
        self._y1 = value[0][1]
        self._x2 = value[1][0]
        self._y2 = value[1][1]
                
        self.update((self._x2 + self._x1) / 2, (self._y2 + self._y1) / 2)
        
    points = property(_get_points, _set_points)
    
    def _get_x1(self):
        return self._x1
    
    def _set_x1(self, value: float):
        if self._x1 is not value:
            self._x1 = value
                
            self.update(x = (self._x2 + self._x1) / 2)
        
    x1 = property(_get_x1, _set_x1)
    
    def _get_y1(self):
        return self._y1
    
    def _set_y1(self, value: float):
        if self._y1 is not value:
            self._y1 = value
        
            self.update(y = (self._y2 + self._y1) / 2)
                
    y1 = property(_get_y1, _set_y1)
    
    def _get_x2(self):
        return self._x2
    
    def _set_x2(self, value: float):
        if self._x2 is not value:
            self._x2 = value
        
            self.update(x = (self._x2 + self._x1) / 2)
        
    x2 = property(_get_x2, _set_x2)
    
    def _get_y2(self):
        return self._y2
    
    def _set_y2(self, value: float):
        if self._y2 is not value:
            self._y2 = value
        
            self.update(y = (self._y2 + self._y1) / 2)
        
    y2 = property(_get_y2, _set_y2)
    
    def _get_color(self):
        if self._color1 == self._color2:
            return self._color1
        
        return self._color1, self._color2
    
    def _set_color(self, value: arcade.Color):
        if self._color1 is not value or self._color2 is not value:
            self._color1 = value
            self._color2 = value
        
            self.update()
        
    color = property(_get_color, _set_color)
    
    def _get_color1(self):
        return self._color1
    
    def _set_color1(self, value: arcade.Color):
        if self._color1 is not value:
            self._color1 = value
        
            self.update()
        
    color1 = property(_get_color1, _set_color1)
    
    def _get_color2(self):
        return self._color2
    
    def _set_color2(self, value: arcade.Color):
        if self._color2 is not value:
            self._color2 = value
        
            self.update()
        
    color2 = property(_get_color2, _set_color2)    
    
    def _get_thickness(self):
        return self._thickness
    
    def _set_thickness(self, value: float):
        if self._thickness is not value:
            self._thickness = value
        
            self.update()
        
    thickness = property(_get_thickness, _set_thickness)

    def _get_top(self):
        return Top_Of_Points(self.get_corners())
    
    def _set_top(self, value: float):
        distance = value - self.top
        
        self.sprite.center_y += distance
            
    top = property(_get_top, _set_top)
    
    def _get_bottom(self):
        return Bottom_Of_Points(self.get_corners())
    
    def _set_bottom(self, value: float):
        distance = value - self.bottom
        
        self.sprite.center_y += distance
            
    bottom = property(_get_bottom, _set_bottom)
    
    def _get_left(self):
        return Left_Of_Points(self.get_corners())
    
    def _set_left(self, value: float):
        distance = value - self.left
        
        self.sprite.center_x += distance
            
    left = property(_get_left, _set_left)
    
    def _get_right(self):
        return Right_Of_Points(self.get_corners())
    
    def _set_right(self, value: float):
        distance = value - self.right
        
        self.sprite.center_x += distance
            
    right = property(_get_right, _set_right)
    
class Position:
    
    def __init__(self, point, shape):
        self.array = list(point)
        self.shape = shape
        
    def __getitem__(self, key):
        return self.array[key]    
        
    def __setitem__(self, key, value):
        self.array[key] = value
        
        if key == 0:
            self.shape.update(x = Center_X_Of_Points(self.shape.points))
            
        elif key == 1:
            self.shape.update(y = Center_Y_Of_Points(self.shape.points))
            
    def __iter__(self):
        return iter(self.array)
    
    def __str__(self):
        return str(self.array)
    
    def __repr__(self):
        return repr(self.array)
    
    def __len__(self):
        return len(self.array)
    
class Positions(Position):
    
    def __init__(self, points, shape):
        self.array = [Position(point, shape) for point in points]
        self.shape = shape
        
    def __setitem__(self, key, value):
        self.array[key] = value
        self.shape.update(Center_X_Of_Points(self.shape.points),
                          Center_Y_Of_Points(self.shape.points))
    
class Strip(Base):
    
    def __init__(self,
                 points: arcade.PointList = ((0, 0), (100, 100), (150, 50)),
                 color: arcade.Color = (0, 0, 0), thickness: float = 1,
                 rotation: float = 0):

        self.points = Positions(points, self)
        self._color = color
        self._thickness = thickness
        self.pymunk = Pymunk()
        self.array = None

        self.update(Center_X_Of_Points(self._points),
                    Center_Y_Of_Points(self._points), rotation)
        
    def draw(self):
        self.sprite.program['Angle'] = self.sprite._angle
        self.sprite.draw()
        
    def boundary(self):
        return {'points': self.get_corners(),
                'type': 'polygon'}
    
    def get_moment(self, mass):
        return pymunk.moment_for_poly(mass, self.get_current())
    
    def get_shape(self, body):
        return pymunk.Poly(body, self.get_current())
    
    def get_corners(self):
        """
        I don't know how to get all corners of the strip. The strip
        collision isn't accurate. Is there an Arcade function similar to
        get_points_from_thick_line that applies to line strips?
        """
        positions = []
        
        for point in self.get_current():
            position = (point[0] + self.sprite.center_x,
                        point[1] + self.sprite.center_y)
                    
            positions.append(position)
        
        return Rotate_Points(positions, self.sprite.angle,
                             self.sprite.center_x, self.sprite.center_y)
    
    def get_current(self):
        x = Center_X_Of_Points(self._points)
        y = Center_Y_Of_Points(self._points)        
        
        positions = []
        
        for point in self._points:
            positions.append([point[0] - x, point[1] - y])
            
        return positions
    
    def update(self, x = None, y = None, angle = None):
        
        if x is None: x = self.sprite.center_x
        if y is None: y = self.sprite.center_y
        if angle is None: angle = self.sprite.angle
            
        self.shape = arcade.create_line_strip(self.get_current(), self._color,
                                              self._thickness)
        
        self.sprite = arcade.ShapeElementList()
        self.sprite.append(self.shape)
        
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.angle = angle
        
        if self.pymunk.engine is not None:
            self.pymunk.engine.refresh(self)        
    
    def _get_points(self):
        return self._points
    
    def _set_points(self, value: arcade.PointList):
        self._points = Positions(value, self)
        
        self.update(Center_X_Of_Points(self._points),
                    Center_Y_Of_Points(self._points))
    
    points = property(_get_points, _set_points)    
    
    def _get_top(self):
        return Top_Of_Points(self.get_corners())
    
    def _set_top(self, value: float):
        distance = value - self.top
        
        self.sprite.center_y += distance
            
    top = property(_get_top, _set_top)
    
    def _get_bottom(self):
        return Bottom_Of_Points(self.get_corners())
    
    def _set_bottom(self, value: float):
        distance = value - self.bottom
        
        self.sprite.center_y += distance
            
    bottom = property(_get_bottom, _set_bottom)
    
    def _get_left(self):
        return Left_Of_Points(self.get_corners())
    
    def _set_left(self, value: float):
        distance = value - self.left
        
        self.sprite.center_x += distance
            
    left = property(_get_left, _set_left)
    
    def _get_right(self):
        return Right_Of_Points(self.get_corners())
    
    def _set_right(self, value: float):
        distance = value - self.right
        
        self.sprite.center_x += distance
            
    right = property(_get_right, _set_right)
    
    def _get_color(self):
        return self._color
    
    def _set_color(self, value: arcade.Color):
        if self._color is not value:
            self._color = value
            
            self.update()
            
    color = property(_get_color, _set_color)
    
    def _get_thickness(self):
        return self._thickness
    
    def _set_thickness(self, value: bool):
        if self._thickness is not value:
            self._thickness = value
            
            self.update()
            
    thickness = property(_get_thickness, _set_thickness)
        
class Shape(Base):
    
    def __init__(self,
                 points: arcade.PointList = ((0, 0), (100, 200), (150, 100), (90, 10)),
                 color: arcade.Color = (0, 0, 0), outline: float = 0,
                 rotation: float = 0):

        self._points = Positions(points, self)
        self._color = color
        self._outline = outline
        self.pymunk = Pymunk()
        self.array = None
        
        self.update(Center_X_Of_Points(self._points),
                    Center_Y_Of_Points(self._points), rotation)
        
    def draw(self):
        self.sprite.program['Angle'] = self.sprite._angle
        self.sprite.draw()
        
    def boundary(self):
        return {'points': self.get_corners(),
                'type': 'polygon'}
    
    def get_corners(self):
        positions = []
        
        for point in self.get_current():
            position = (point[0] + self.sprite.center_x,
                        point[1] + self.sprite.center_y)
                    
            positions.append(position)        
        
        return Rotate_Points(positions, self.sprite.angle,
                             self.sprite.center_x, self.sprite.center_y)
    
    def get_current(self):        
        positions = []
        
        x = Center_X_Of_Points(self._points)
        y = Center_Y_Of_Points(self._points)        
        
        for point in self._points:
            positions.append([point[0] - x, point[1] - y])
            
        return positions
    
    def update(self, x = None, y = None, angle = None):
        
        if x is None: x = self.sprite.center_x
        if y is None: y = self.sprite.center_y
        if angle is None: angle = self.sprite.angle
            
        if self.outline:
            self.shape = arcade.create_line_loop(self.get_current(),
                                                 self._color, self._outline)
        else:
            self.shape = arcade.create_polygon(self.get_current(),
                                               self._color)
        
        self.sprite = arcade.ShapeElementList()
        self.sprite.append(self.shape)
        
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.angle = angle
        
        if self.pymunk.engine is not None:
            self.pymunk.engine.refresh(self)        
        
    def get_moment(self, mass):
        return pymunk.moment_for_poly(mass, self.get_current())
    
    def get_shape(self, body):
        return pymunk.Poly(body, self.get_current())
    
    def _get_points(self):
        return self._points
    
    def _set_points(self, value: arcade.PointList):
        self._points = Positions(value, self)
        
        self.update(Center_X_Of_Points(self._points),
                    Center_Y_Of_Points(self._points))
    
    def _get_top(self):
        return Top_Of_Points(self.get_corners())
    
    def _set_top(self, value: float):
        distance = value - self.top
        
        self.sprite.center_y += distance
            
    top = property(_get_top, _set_top)
    
    def _get_bottom(self):
        return Bottom_Of_Points(self.get_corners())
    
    def _set_bottom(self, value: float):
        distance = value - self.bottom
        
        self.sprite.center_y += distance
            
    bottom = property(_get_bottom, _set_bottom)
    
    def _get_left(self):
        return Left_Of_Points(self.get_corners())
    
    def _set_left(self, value: float):
        distance = value - self.left
        
        self.sprite.center_x += distance
            
    left = property(_get_left, _set_left)
    
    def _get_right(self):
        return Right_Of_Points(self.get_corners())
    
    def _set_right(self, value: float):
        distance = value - self.right
        
        self.sprite.center_x += distance
            
    right = property(_get_right, _set_right)
    
    def _get_color(self):
        return self._color
    
    def _set_color(self, value: arcade.Color):
        if self._color is not value:
            self._color = value
            
            self.update()
            
    color = property(_get_color, _set_color)
    
    def _get_outline(self):
        return self._outline
    
    def _set_outline(self, value: bool):
        if self._outline is not value:
            self._outline = value
            
            self.update()
            
    outline = property(_get_outline, _set_outline)
        
class Circle(Base):
    
    def __init__(self, x: float = 100, y: float = 100, size: float = 50,
                 color: arcade.Color = (0, 0, 0), outline: float = 0,
                 segments: int = 32):

        self._size = size
        self._color1 = color
        self._color2 = color
        self._outline = outline
        self._segments = segments
        self.pymunk = Pymunk()
        self.array = None

        self.update(x, y, 0)
        
    def draw(self):
        self.sprite.draw()
        
    def boundary(self):
        return {'points': self.get_corners(),
                'type': 'polygon'}
    
    def get_corners(self):
        positions = []
        
        for index in range(1, self._segments):
            x, y = Direction(self._size / 2, index * 360 / self._segments)
            point = [self.sprite.center_x + x, self.sprite.center_y + y]
            
            positions.append(point)
            
        return positions
    
    def get_current(self):
        positions = []
        
        for index in range(1, self._segments):
            x, y = Direction(self._size / 2, index * 360 / self._segments)
            
            positions.append((x, y))
            
        return positions        
        
    def update(self, x = None, y = None, angle = None):
        
        if x is None: x = self.sprite.center_x
        if y is None: y = self.sprite.center_y
        if angle is None: angle = self.sprite.angle
        
        if self._outline:
            self.shape = arcade.create_line_loop(self.get_current(),
                                                 self._color1, self._outline)            
        else:
            self.shape = arcade.create_ellipse_filled_with_colors(
                0, 0, self._size / 2, self._size / 2, self._color1,
                self._color2, num_segments = self._segments)            
        
        self.sprite = arcade.ShapeElementList()
        self.sprite.append(self.shape)
        
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.angle = angle
        
        if self.pymunk.engine is not None:
            self.pymunk.engine.refresh(self)        
    
    def get_moment(self, mass):
        return pymunk.moment_for_circle(mass, 0, self._size / 2)
    
    def get_shape(self, body):
        return pymunk.Circle(body, self._size / 2)
    
    def _get_top(self):
        return Top_Of_Points(self.get_corners())
    
    def _set_top(self, value: float):
        distance = value - self.top
        
        self.sprite.center_y += distance
            
    top = property(_get_top, _set_top)
    
    def _get_bottom(self):
        return Bottom_Of_Points(self.get_corners())
    
    def _set_bottom(self, value: float):
        distance = value - self.bottom
        
        self.sprite.center_y += distance
            
    bottom = property(_get_bottom, _set_bottom)
    
    def _get_left(self):
        return Left_Of_Points(self.get_corners())
    
    def _set_left(self, value: float):
        distance = value - self.left
        
        self.sprite.center_x += distance
            
    left = property(_get_left, _set_left)
    
    def _get_right(self):
        return Right_Of_Points(self.get_corners())
    
    def _set_right(self, value: float):
        distance = value - self.right
        
        self.sprite.center_x += distance
            
    right = property(_get_right, _set_right)
    
    def _get_size(self):
        return self._size
    
    def _set_size(self, value: float):
        if self._size is not value:
            self._size = value
            
        self.update()
            
    size = property(_get_size, _set_size)
    
    def _get_color(self):
        if self._color1 == self._color2:
            return self._color1
        
        return self._color1, self._color2
    
    def _set_color(self, value: arcade.Color):
        
        if not self._color1 == self._color2 == value:
            self._color1 = value
            self._color2 = value       
        
            self.update()
            
    color = property(_get_color, _set_color)
    
    def _get_color1(self):
        return self._color1
    
    def _set_color1(self, value: arcade.Color):
        if self._color1 is not value:
            self._color1 = value
        
            self.update()
        
    color1 = property(_get_color1, _set_color1)
    
    def _get_color2(self):
        return self._color2
    
    def _set_color2(self, value: arcade.Color):
        if self._color2 is not value:
            self._color2 = value
        
            self.update()
        
    color2 = property(_get_color2, _set_color2)
    
    def _get_outline(self):
        return self._outline
    
    def _set_outline(self, value: float):
        if self._outline is not value:
            self._outline = value
        
            self.update()
        
    outline = property(_get_outline, _set_outline)
    
    def _get_segments(self):
        return self._segments
    
    def _set_segments(self, value: float):
        if self._segments is not value:
            self._segments = value
        
            self.update()
        
    segments = property(_get_segments, _set_segments)

class Box(Base):
    
    def __init__(self, x: float = 100, y: float = 100, width: float = 50,
                 height: float = 30, color: arcade.Color = (0, 0, 0),
                 outline: float = 0, rotation: float = 0):

        self._width = width
        self._height = height
        self._color1 = color
        self._color2 = color
        self._color3 = color
        self._color4 = color
        self._outline = outline
        self.pymunk = Pymunk()
        self.array = None

        self.update(x, y, rotation)
        
    def draw(self):
        self.sprite.program['Angle'] = self.sprite._angle
        self.sprite.draw()
        
    def boundary(self):
        return {'points': self.get_corners(),
                'type': 'polygon'}
    
    def get_corners(self):
        return arcade.get_rectangle_points(self.sprite.center_x,
                                           self.sprite.center_y, self._width,
                                           self._height, self.sprite.angle)
    
    def update(self, x = None, y = None, angle = None):
        
        if x is None: x = self.sprite.center_x
        if y is None: y = self.sprite.center_y
        if angle is None: angle = self.sprite.angle
        
        if self._outline:
            self.shape = arcade.create_rectangle_outline(0, 0, self._width,
                                                         self._height,
                                                         self._color1,
                                                         self._outline)
        else:
            self.shape = arcade.create_rectangle_filled_with_colors(
                arcade.get_rectangle_points(0, 0, self._width, self._height),
                (self._color1, self._color2, self._color3, self._color4))            
        
        self.sprite = arcade.ShapeElementList()
        self.sprite.append(self.shape)
        
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.angle = angle
        
        if self.pymunk.engine is not None:
            self.pymunk.engine.refresh(self)        
        
    def get_moment(self, mass):
        return pymunk.moment_for_box(mass, (self._width, self._height))
    
    def get_shape(self, body):
        return pymunk.Poly.create_box(body, (self._width, self._height))
    
    def _get_top(self):
        return Top_Of_Points(self.get_corners())
    
    def _set_top(self, value: float):
        distance = value - self.top
        
        self.sprite.center_y += distance
        
    top = property(_get_top, _set_top)
    
    def _get_bottom(self):
        return Bottom_Of_Points(self.get_corners())
    
    def _set_bottom(self, value: float):
        distance = value - self.bottom
        
        self.sprite.center_y += distance
        
    bottom = property(_get_bottom, _set_bottom)
    
    def _get_left(self):
        return Left_Of_Points(self.get_corners())
    
    def _set_left(self, value: float):
        distance = value - self.left
        
        self.sprite.center_x += distance
        
    left = property(_get_left, _set_left)
    
    def _get_right(self):
        return Right_Of_Points(self.get_corners())
    
    def _set_right(self, value: float):
        distance = value - self.right
        
        self.sprite.center_x += distance
        
    right = property(_get_right, _set_right)
    
    def _get_width(self):
        return self._width
    
    def _set_width(self, value: float):
        if self._width is not value:
            self._width = value
            
            self.update()
    
    width = property(_get_width, _set_width)
    
    def _get_height(self):
        return self._height
    
    def _set_height(self, value: float):
        if self._height is not value:
            self._height = value
            
            self.update()
    
    height = property(_get_height, _set_height)
    
    def _get_color(self):
        if self._color1 == self._color2 == self.color3 == self.color4:
            return self._color1
        
        return self._color1, self._color2, self._color3, self._color4
    
    def _set_color(self, value: arcade.Color):
        if (not self._color1 == self._color2 == self._color3 == self._color4 ==
            value):
            
            self._color1 = value
            self._color2 = value
            self._color3 = value
            self._color4 = value            
        
            self.update()
        
    color = property(_get_color, _set_color)
    
    def _get_color1(self):
        return self._color1
    
    def _set_color1(self, value: arcade.Color):
        if self._color1 is not value:
            self._color1 = value
        
            self.update()
        
    color1 = property(_get_color1, _set_color1)
    
    def _get_color2(self):
        return self._color2
    
    def _set_color2(self, value: arcade.Color):
        if self._color2 is not value:
            self._color2 = value
        
            self.update()
            
    color2 = property(_get_color2, _set_color2)
            
    def _get_color3(self):
        return self._color3
    
    def _set_color3(self, value: arcade.Color):
        if self._color3 is not value:
            self._color3 = value
        
            self.update()
            
    color3 = property(_get_color3, _set_color3)
            
    def _get_color4(self):
        return self._color4
    
    def _set_color4(self, value: arcade.Color):
        if self._color4 is not value:
            self._color4 = value
        
            self.update()
            
    color4 = property(_get_color4, _set_color4)
    
    def _get_outline(self):
        return self._outline
    
    def _set_outline(self, value: float):
        if self._outline is not value:
            self._outline = value
            
            self.update()
    
    outline = property(_get_outline, _set_outline)
                
class Image(Base):
    
    def __init__(self, name: str = arcade.resources.image_key_blue,
                 x: float = 100, y: float = 100,
                 flip_horizontally: bool = False,
                 flip_vertically: bool = False,
                 flip_diagonally: bool = False,
                 rotation: float = 0, collision: str = 'simple',
                 detail: float = 4.5, alpha: float = 255):
        
        if collision == 'box':
            collide = 'None'
            
        else:
            collide = collision.capitalize()
            
        self.sprite = arcade.Sprite(name, center_x = x, center_y = y,
                                    flipped_horizontally = flip_horizontally,
                                    flipped_vertically = flip_vertically,
                                    flipped_diagonally = flip_diagonally,
                                    hit_box_algorithm = collide,
                                    hit_box_detail = detail)

        self.sprite.angle = rotation
                        
        self.name = name
        self.alpha = alpha        
        self.pymunk = Pymunk()
        self.array = None
        
    def get_moment(self, mass):
        return pymunk.moment_for_poly(mass, self.sprite.get_hit_box())
    
    def get_shape(self, body):
        return pymunk.Poly(body, self.sprite.get_hit_box())
        
    def get_corners(self):
        return self.sprite.get_adjusted_hit_box()

    def boundary(self):
        return {'points': self.get_corners(),
                'type': 'polygon'}
    
    def draw(self):
        self.sprite.draw()
    
    def _get_top(self):
        return self.sprite.top
    
    def _set_top(self, value: float):
        self.sprite.top = value
            
    top = property(_get_top, _set_top)
    
    def _get_bottom(self):
        return self.sprite.bottom
    
    def _set_bottom(self, value: float):
        self.sprite.bottom = value
            
    bottom = property(_get_bottom, _set_bottom)
    
    def _get_left(self):
        return self.sprite.left
    
    def _set_left(self, value: float):
        self.sprite.left = value
            
    left = property(_get_left, _set_left)
    
    def _get_right(self):
        return self.sprite.right
    
    def _set_right(self, value: float):
        self.sprite.right = value
            
    right = property(_get_right, _set_right)
    
    def _get_width(self):
        return self.sprite.width
    
    def _set_width(self, value: float):
        self.sprite.width = value
            
    width = property(_get_width, _set_width)
    
    def _get_height(self):
        return self.sprite.height
    
    def _set_height(self, value: float):
        self.sprite.height = value
            
    height = property(_get_height, _set_height)
    
    def _get_alpha(self):
        return self.sprite.alpha
    
    def _set_alpha(self, value: float):
        self.sprite.alpha = value
            
    alpha = property(_get_alpha, _set_alpha)
    
    def _get_color(self):
        return self.sprite.color
    
    def _set_color(self, value: float):
        self.sprite.color = value
            
    color = property(_get_color, _set_color)
    
    def _get_collision(self):
        if self.sprite._hit_box_algorithm == 'None':
            return 'box'
            
        return self.sprite._hit_box_algorithm.lower()
    
    def _set_collision(self, value: str):
        if self.collision is not value:
            self.sprite._point_list_cache = None
            self.sprite.points = None
            self.sprite.texture._hit_box_points = None        
        
            if value == 'box':
                self.sprite._texture._hit_box_algorithm = 'None'
            
            else:
                self.sprite._texture._hit_box_algorithm = value.capitalize()
            
    collision = property(_get_collision, _set_collision)
    
    def _get_detail(self):
        return self.sprite.texture._hit_box_detail
    
    def _set_detail(self, value: float):
        if self.detail is not value:
            self.sprite._point_list_cache = None
            self.sprite.points = None
            self.sprite.texture._hit_box_points = None        
            self.sprite.texture._hit_box_detail = value
            
    detail = property(_get_detail, _set_detail)
    
text_id = 0
                
class Text(Base):
    
    def __init__(self, content: str = 'hello', x: float = 100, y: float = 100,
                 color: arcade.Color = (0, 0, 0), size: float = 40,
                 rotation: float = 0):

        self._content = content
        self._color = color
        self._size = size
        self.pymunk = Pymunk()
        self.array = None

        self.update(x, y, rotation)
        
    def draw(self):
        self.sprite.draw()
        
    def boundary(self):
        return {'points': self.get_corners(),
                'type': 'polygon'}
    
    def get_corners(self):
        return self.sprite.get_adjusted_hit_box()
    
    def update(self, x = None, y = None, angle = None):
        global text_id
        
        if x is None: x = self.sprite.center_x
        if y is None: y = self.sprite.center_y
        if angle is None: angle = self.sprite.angle
                
        self.sprite = arcade.draw_text(self._content, x, y, self._color,
                                       self._size, rotation = angle,
                                       align = 'center', anchor_x = 'center',
                                       anchor_y = 'center', bold = text_id)
        text_id += 1
        
        if self.pymunk.engine is not None:
            self.pymunk.engine.refresh(self)        
        
    def get_moment(self, mass):
        return pymunk.moment_for_poly(mass, self.sprite.get_hit_box())
    
    def get_shape(self, body):
        return pymunk.Poly(body, self.sprite.get_hit_box())    
        
    def clear(self):
        self.content = ''
    
    def _get_content(self):
        return self._content

    def _set_content(self, text: str):
        if not text == self._content:
            self._content = text
        
            self.update()

    content = property(_get_content, _set_content)
    
    def _get_color(self):
        return self._color
    
    def _set_color(self, value: arcade.Color):
        self._color = value

        self.update()

    color = property(_get_color, _set_color)
    
    def _get_size(self):
        return self._size
    
    def _set_size(self, value: float):
        self._size = value

        self.update()

    size = property(_get_size, _set_size)
        
    def _get_width(self):
        return self.sprite.width
    
    def _set_width(self, value: float):
        self.sprite.width = value
        
    width = property(_get_width, _set_width)
    
    def _get_height(self):
        return self.sprite.height
    
    def _set_height(self, value: float):
        self.sprite.height = value
        
    height = property(_get_height, _set_height)    

    def _get_top(self):
        return self.sprite.top
    
    def _set_top(self, value: float):
        self.sprite.top = value
        
    top = property(_get_top, _set_top)
    
    def _get_bottom(self):
        return self.sprite.bottom
    
    def _set_bottom(self, value: float):
        self.sprite.bottom = value
        
    bottom = property(_get_bottom, _set_bottom)
    
    def _get_left(self):
        return self.sprite.left
    
    def _set_left(self, value: float):
        self.sprite.left = value
        
    left = property(_get_left, _set_left)
    
    def _get_right(self):
        return self.sprite.right
    
    def _set_right(self, value: float):
        self.sprite.right = value
        
    right = property(_get_right, _set_right)