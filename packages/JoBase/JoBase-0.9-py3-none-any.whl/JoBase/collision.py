import math, warnings, arcade

from arcade import PointList

def collide(type1: dict, type2: dict):
    # The code below checks every combination of collision.
    
    if type1['type'] == 'none' or type2['type'] == 'none':
        warnings.warn("You entered a shape that doesn't have collision.")
        
    elif type1['type'] == 'point' and type2['type'] == 'point':
        
        return rect_to_point_collision(type1['x'], type1['y'], type2['x'],
                                       type2['y'])
    
    elif type1['type'] == 'polygon' and type2['type'] == 'polygon':
        
        return polygon_to_polygon_collision(type1['points'], type2['points'])
    
    elif type1['type'] == 'point' and type2['type'] == 'polygon':
        
        return point_to_polygon_collision(type1['x'], type1['y'],
                                          type2['points'])
    
    elif type1['type'] == 'polygon' and type2['type'] == 'point':
        
        return point_to_polygon_collision(type2['x'], type2['y'],
                                          type1['points'])
    
    elif type1['type'] == 'list' and type2['type'] == 'list':
        
        return list_to_list_collision(type1['list'], type2['list'])
        
    elif (type1['type'] == 'list' and type2['type'] == 'point' or
          type1['type'] == 'list' and type2['type'] == 'polygon'):
        
        return list_to_object_collision(type1['list'], type2)
    
    elif (type1['type'] == 'point' and type2['type'] == 'list' or
          type1['type'] == 'polygon' and type2['type'] == 'list'):
                
        return list_to_object_collision(type2['list'], type1)
    
def point_to_point_collision(x1: float, y1: float, x2: float, y2: float):
    return x1 == x2 and y1 == y2

def polygon_to_polygon_collision(points1: PointList, points2: PointList):
    return arcade.are_polygons_intersecting(points1, points2)

def point_to_polygon_collision(x1: float, y1: float, points2: PointList):
    return arcade.is_point_in_polygon(x1, y1, points2)

def list_to_object_collision(list1: list, boundary2: dict):
    for boundary in list1:
        if collide(boundary, boundary2):
            return True
        
def list_to_list_collision(list1: list, list2: list):
    for boundary1 in list1:
        for boundary2 in list2:
            if collide(boundary1, boundary2):
                return True