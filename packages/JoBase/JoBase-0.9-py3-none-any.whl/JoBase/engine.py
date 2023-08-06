import arcade, pymunk, math

from .setup import SCREEN

from .draw import Point
from .draw import Line
from .draw import Strip
from .draw import Shape
from .draw import Circle
from .draw import Box
from .draw import Image
from .draw import Text
from .draw import Positions
from .draw import Position
from .draw import Pymunk

from .math import Distance
from .math import Direction
from .math import Angle

DYNAMIC = pymunk.Body.DYNAMIC
STATIC = pymunk.Body.STATIC
KINEMATIC = pymunk.Body.KINEMATIC
INFINITE = pymunk.inf

sprites = [Point, Line, Strip, Shape, Circle, Box, Image, Text]

class Engine:
    
    def __init__(self, x_gravity: float = 0, y_gravity: float = -1000, damping: float = 1):
        
        SCREEN.engines.append(self)
        self.space = pymunk.Space()
        self.space.gravity = (x_gravity, y_gravity)
        self.space.damping = damping
        self.space.collision_slop = 1
        self.sprites = []
        self.joints = []
        
    def add(self, sprite, mass: float = 1, body: int = DYNAMIC,
            elasticity: float = None, moment = None, friction: float = 0.2,
            max_x_speed: float = 0, max_y_speed: float = 0):
        
        group = type(sprite)
        
        def velocity(body, gravity, damping, dt):
            pymunk.Body.update_velocity(body, gravity, damping, dt)

            if sprite.max_x_speed:
                speed = body.velocity.x
                
                if abs(speed) > sprite.max_x_speed:
                    speed = sprite.max_x_speed * math.copysign(1, speed)
                    body.velocity = pymunk.Vec2d(speed, body.velocity.y)

            if sprite.max_y_speed:
                speed = body.velocity.y
                
                if abs(speed) > sprite.max_y_speed:
                    speed = sprite.max_y_speed * math.copysign(1, speed)
                    body.velocity = pymunk.Vec2d(body.velocity.x, speed)        
        
        if group in sprites:
            
            sprite.pymunk.moment = moment
            
            if moment is None:
                moment = sprite.get_moment(mass)

            pymunk_body = pymunk.Body(mass, moment, body)
            pymunk_body.position = pymunk.Vec2d(sprite.x, sprite.y)
            pymunk_body.angle = math.radians(sprite.rotation)

            if body == DYNAMIC:
                pymunk_body.velocity_func = velocity
                
            pymunk_shape = sprite.get_shape(pymunk_body)
                        
            if elasticity is not None:
                pymunk_shape.elasticity = elasticity
            
            pymunk_shape.friction = friction
            
            self.space.add(pymunk_body, pymunk_shape)
            self.sprites.append(sprite)
        
            sprite.pymunk.shape = pymunk_shape
            sprite.pymunk.body = pymunk_body
            sprite.pymunk.engine = self
            sprite.pymunk.max_x_speed = max_x_speed
            sprite.pymunk.max_y_speed = max_y_speed
            
        elif group in joints:
            self.space.add(sprite.joint)
            self.joints.append(sprite)
        
    def remove(self, sprite):
        self.space.remove(sprite.pymunk.body, sprite.pymunk.shape)
        
    def refresh(self, sprite):
        
        mass = sprite.pymunk.body.mass
        moment = sprite.pymunk.moment
        body = sprite.pymunk.body.body_type
        
        if moment is None:
            moment = sprite.get_moment(mass)

        pymunk_body = pymunk.Body(mass, moment, body)
        pymunk_body.position = pymunk.Vec2d(sprite.x, sprite.y)
        pymunk_body.angle = sprite.rotation
        
        if body == DYNAMIC:
            pymunk_body.velocity_func = sprite.pymunk.body.velocity_func
        
        pymunk_shape = sprite.get_shape(pymunk_body)
        pymunk_shape.elasticity = sprite.pymunk.shape.elasticity
        pymunk_shape.friction = sprite.pymunk.shape.friction
        
        self.space.remove(sprite.pymunk.body, sprite.pymunk.shape)
        self.space.add(pymunk_body, pymunk_shape)
    
        sprite.pymunk.shape = pymunk_shape
        sprite.pymunk.body = pymunk_body

    def update(self):
        for sprite in self.sprites:
            sprite.sprite.center_x = sprite.pymunk.shape.body.position.x
            sprite.sprite.center_y = sprite.pymunk.shape.body.position.y
            sprite.sprite.angle = math.degrees(sprite.pymunk.shape.body.angle)
                
        for joint in self.joints:
            if type(joint) == Groove_Joint:
                x1, y1 = Direction(joint.a, Angle(joint.joint.a.position.x,
                                                  joint.joint.a.position.y,
                                                  joint.joint.b.position.x,
                                                  joint.joint.b.position.y))
                
                x2, y2 = Direction(joint.b, Angle(joint.joint.a.position.x,
                                                  joint.joint.a.position.y,
                                                  joint.joint.b.position.x,
                                                  joint.joint.b.position.y))
                x1 += joint.joint.a.position.x
                y1 += joint.joint.a.position.y
                x2 += joint.joint.a.position.x
                y2 += joint.joint.a.position.y
                
                joint.points = ((x1, y1), (x2, y2))
                                
            else:
                joint.points = ((joint.joint.a.position.x,
                                 joint.joint.a.position.y),
                                (joint.joint.b.position.x,
                                 joint.joint.b.position.y))
                        
        self.space.step(1 / SCREEN.rate)
        
    def collide(self, type1, type2):
        query = self.space.shape_query(type1.pymunk.shape)
        
        for item in query:
            if type2.pymunk.shape == item.shape:
                return True
            
        return False
    
class Joint(Line):
    
    def __init__(self, sprite1, sprite2, thickness, color):
        
        if sprite1.pymunk.engine is None or sprite2.pymunk.engine is None:
            raise Exception('Both sprites should be added to an Engine.')
        
        if sprite1.pymunk.engine is not sprite2.pymunk.engine:
            raise Exception('Both sprites should have the same Engine.')
        
        self._x1 = sprite1.x
        self._y1 = sprite1.y
        self._x2 = sprite2.x
        self._y2 = sprite2.y
        self._thickness = thickness
        self._color1 = color
        self._color2 = color
        self.pymunk = Pymunk()
        
        self.update(0, 0, 0)
    
class Pin_Joint(Joint):
    
    def __init__(self, sprite1, sprite2, thickness: float = 1,
                 color: arcade.Color = (0, 0, 0)):
        
        super().__init__(sprite1, sprite2, thickness, color)
        
        self.joint = pymunk.PinJoint(sprite1.pymunk.shape.body,
                                     sprite2.pymunk.shape.body)
        
class Spring_Joint(Joint):
    
    def __init__(self, sprite1, sprite2, length: float = 100,
                 stiffness: float = 300, damping: float = 30,
                 thickness: float = 1, color: arcade.Color = (0, 0, 0)):
        
        super().__init__(sprite1, sprite2, thickness, color)
        
        self.joint = pymunk.DampedSpring(sprite1.pymunk.shape.body,
                                         sprite2.pymunk.shape.body, (0, 0),
                                         (0, 0), length, stiffness, damping)
        
class Gear_Joint(Joint):
    
    def __init__(self, sprite1, sprite2, angle: float = 1, ratio: float = 1,
                 thickness: float = 1, color: arcade.Color = (0, 0, 0)):
        
        super().__init__(sprite1, sprite2, thickness, color)
        
        self.joint = pymunk.GearJoint(sprite1.pymunk.shape.body,
                                      sprite2.pymunk.shape.body, angle, ratio)
        
class Groove_Joint(Joint):
    
    def __init__(self, sprite1, sprite2, min_x: float = 100, min_y: float = 100,
                 max_x: float = 200, max_y: float = 200, thickness: float = 1,
                 color: arcade.Color = (0, 0, 0)):
        
        super().__init__(sprite1, sprite2, thickness, color)
        
        self.joint = pymunk.GrooveJoint(sprite1.pymunk.shape.body,
                                        sprite2.pymunk.shape.body,
                                        (min_x, min_y), (max_x, max_y), (0, 0))
        self.a = Distance(0, 0, min_x, min_y)
        self.b = Distance(0, 0, max_x, max_y)
        
class Pivot_Joint(Joint):
    
    def __init__(self, sprite1, sprite2, pivot_x: float = 100,
                 pivot_y: float = 100, thickness: float = 1,
                 color: arcade.Color = (0, 0, 0)):
        
        super().__init__(sprite1, sprite2, thickness, color)
        
        self.joint = pymunk.PivotJoint(sprite1.pymunk.shape.body,
                                       sprite2.pymunk.shape.body,
                                       (pivot_x, pivot_y))
        
class Motor_Joint(Joint):
    
    def __init__(self, sprite1, sprite2, speed: float = 5,
                 thickness: float = 1, color: arcade.Color = (0, 0, 0)):
        
        super().__init__(sprite1, sprite2, thickness, color)
        
        self.joint = pymunk.SimpleMotor(sprite1.pymunk.shape.body,
                                        sprite2.pymunk.shape.body, speed)
            
joints = [Pin_Joint, Spring_Joint, Gear_Joint, Groove_Joint, Pivot_Joint,
          Motor_Joint]