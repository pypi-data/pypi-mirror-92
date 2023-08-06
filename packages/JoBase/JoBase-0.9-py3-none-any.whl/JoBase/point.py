import math, arcade

from .math import Angle
from .math import Distance
from .math import Direction

def Scale_X_Points(points: arcade.PointList, x_scale: float):
    
    for point in points:
        point[0] *= x_scale
        
    return points
        
def Scale_Y_Points(points: arcade.PointList, y_scale: float):
        
    for point in points:
        point[1] *= y_scale
        
    return points

def Scale_Points(points: arcade.PointList, scale: float):
        
    for point in points:
        point[0] *= scale
        point[1] *= scale
        
    return points    
            
def Rotate_Points(points: arcade.PointList, rotation: float, center_x: float,
                  center_y: float):
    
    points = [list(point) for point in points]
    
    for point in points:
        pos = arcade.rotate_point(point[0], point[1], center_x, center_y,
                                  rotation)
        point[0] = pos[0]
        point[1] = pos[1]
                
    return points
        
def Center_X_Of_Points(points: arcade.PointList):
    center_x = 0
    
    for point in points:
        center_x += point[0]
        
    center_x /= len(points)
    
    return center_x

def Center_Y_Of_Points(points: arcade.PointList):
    center_y = 0
    
    for point in points:
        center_y += point[1]
        
    center_y /= len(points)
    
    return center_y
            
def Left_Of_Points(points: arcade.PointList):
    left = 0
    
    for point in points:
        
        if not points.index(point) == 0:
            
            if point[0] < left:
                left = point[0]
                
        else:
            left = point[0]
            
    return left

def Top_Of_Points(points: arcade.PointList):
    top = 0
    
    for point in points:
        
        if not points.index(point) == 0:
            
            if point[1] > top:
                top = point[1]
                
        else:
            top = point[1]
            
    return top

def Right_Of_Points(points: arcade.PointList):
    right = 0  
    
    for point in points:
        
        if not points.index(point) == 0:
            
            if point[0] > right:
                right = point[0]
                
        else:
            right = point[0]
            
    return right

def Bottom_Of_Points(points: arcade.PointList):
    bottom = 0    
    
    for point in points:
        
        if not points.index(point) == 0:
            
            if point[1] < bottom:
                bottom = point[1]
                
        else:
            bottom = point[1]
            
    return bottom