import math
from typing import Tuple,List
from triangulator.models import Point



def sont_colineaires(points:List[Point]):
    """
    Cette fonction détermine si les points sont collinéaires et renvoie True dans ce cas
    
    :param points: prends en parametre une liste de Point
    """
    if len(points) < 3:
        return True  

    x1, y1 = points[0]
    x2, y2 = points[1]

    for (xi, yi) in points[2:]:
        det = (x2 - x1) * (yi - y1) - (y2 - y1) * (xi - x1)
        if det != 0:
            return False
    return True


def duplication_point(points:List[Point]):
    """
    Cette fonction permet de déterminer si des points sont dupliqués et retourne True dans ce cas.
    
    :param points: prends en parametre une liste de Point
    """
    unique_points = set(points)
    if len(unique_points) < len(points):
        return True
    else:
        return False
    

def distance(p1: Point, p2: Point) -> float:
    """
    Cette fonction permet de calculer la distance entre 2 points.
    
    :param p1,p2: prend en paramétre 2 points 
    :rtype: retourne float (nombre réel)
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.sqrt(dx * dx + dy * dy)


def circumcircle(p1: Point, p2: Point, p3: Point) -> Tuple[Point, float]:
    """
    Calcule le cercle circonscrit d'un triangle (le cercle qui passe par les trois sommets du triangle).
    
    :param p1,p2,p3: prend en paramétre 3 points qui sont les sommets du triangles 
    :return: retourne le centre et le rayon du cercle 
    """
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
    
    centre = (ux, uy)
    rayon = distance(centre, p1)
    
    return centre, rayon


def point_in_circumcircle(point: Point, p1: Point, p2: Point, p3: Point) -> bool:
    """
    Cette fonction permet de  déterminer si un point se trouve dans le cercle circonscrit d'un triangle.
    
    :param point: Le point à tester pour savoir s'il se trouve dans le cercle ou non
    :param p1,p2,p3: Prend en paramétre 3 points qui sont les sommets du triangles
    :return: retourne True si le point est dans le cercle et False si le point est a l'exterieur du cercle 

    Remarque si les points sont collinéaire dans ce cas la fonction retourne False
    """
    try:
        centre, rayon = circumcircle(p1, p2, p3)
        print(centre, rayon)
        return distance(point, centre) < rayon - 1e-10
    except ValueError:
        return False





points=[(0.5,0.5), (2,0), (0,2), (-2,0)]
print(point_in_circumcircle(points[0],points[1],points[2],points[3]))
# print(circumcircle(points[1],points[2],points[3]))