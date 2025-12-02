import math
from typing import Tuple
from triangulator.models import Point



def sont_colineaires(points):
    if len(points) < 3:
        return True  

    x1, y1 = points[0]
    x2, y2 = points[1]

    for (xi, yi) in points[2:]:
        det = (x2 - x1) * (yi - y1) - (y2 - y1) * (xi - x1)
        if det != 0:
            return False
    return True


def duplication_point(points):
    unique_points = set(points)
    if len(unique_points) < len(points):
        return True
    else:
        return False
    

def distance(p1: Point, p2: Point) -> float:
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.sqrt(dx * dx + dy * dy)


def circumcircle(p1: Point, p2: Point, p3: Point) -> Tuple[Point, float]:
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    
    # if abs(d) < 1e-10:
    # if abs(d) == 0:
    #     raise ValueError("Points are collinear")
    if sont_colineaires((p1,p2,p3)):
        raise ValueError("Points are collinear")


    ux = ((ax * ax + ay * ay) * (by - cy) + 
          (bx * bx + by * by) * (cy - ay) + 
          (cx * cx + cy * cy) * (ay - by)) / d
    
    uy = ((ax * ax + ay * ay) * (cx - bx) + 
          (bx * bx + by * by) * (ax - cx) + 
          (cx * cx + cy * cy) * (bx - ax)) / d
    
    center = (ux, uy)
    radius = distance(center, p1)
    
    return center, radius


def point_in_circumcircle(point: Point, p1: Point, p2: Point, p3: Point) -> bool:
    try:
        center, radius = circumcircle(p1, p2, p3)
        return distance(point, center) < radius - 1e-10
    except ValueError:
        return False





# points=[(1,2), (3,6), (5,10), (7,14)]
# print(point_in_circumcircle(points[0],points[1],points[2],points[3]))
# print(circumcircle(points[1],points[2],points[3]))