from typing import List
from triangulator.models import Point, Triangle
from triangulator.geometry import point_in_circumcircle, sont_colineaires, duplication_point


def triangulate(points: List[Point]) -> List[Triangle]:
    """
    Calcule la triangulation de Delaunay d'un ensemble de points en 2D en utilisant l'algorithme de Bowyer-Watson.
    
    :param points: Liste des points à trianguler, minimum 3 points, les points ne doivent pas être dupliqués et les points ne doivent pas être tous colinéaires
    :return: Liste des triangles formant la triangulation, chaque triangle est un tuple (i, j, k) d'indices, les indices référencent les points dans la liste d'entrée
    """
    if duplication_point(points):
        raise ValueError("point existant deja")
    
    if len(points) < 3:
        raise ValueError(f"il faut au moins 3 points dans ce cas tu as donné: {len(points)}")

    if sont_colineaires(points):
        raise ValueError("point colineaire impossible de faire une triangulation")
    
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    
    dx = max_x - min_x
    dy = max_y - min_y
    delta_max = max(dx, dy)
    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2
    
    p1 = (mid_x - 20 * delta_max, mid_y - delta_max)
    p2 = (mid_x, mid_y + 20 * delta_max)
    p3 = (mid_x + 20 * delta_max, mid_y - delta_max)
    
    all_points = list(points) + [p1, p2, p3]
    n = len(points)
    
    triangles = [(n, n + 1, n + 2)]
    
    for i in range(n):
        point = points[i]
        bad_triangles = []
        
        for tri in triangles:
            if point_in_circumcircle(
                point,
                all_points[tri[0]],
                all_points[tri[1]],
                all_points[tri[2]]
            ):
                bad_triangles.append(tri)
        
        polygon = []
        for tri in bad_triangles:
            for edge in [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]:
                shared = False
                for other_tri in bad_triangles:
                    if other_tri == tri:
                        continue
                    if (edge in [(other_tri[0], other_tri[1]), 
                                 (other_tri[1], other_tri[2]), 
                                 (other_tri[2], other_tri[0])] or
                        (edge[1], edge[0]) in [(other_tri[0], other_tri[1]), 
                                                (other_tri[1], other_tri[2]), 
                                                (other_tri[2], other_tri[0])]):
                        shared = True
                        break
                
                if not shared:
                    polygon.append(edge)
        
        for tri in bad_triangles:
            triangles.remove(tri)
        
        for edge in polygon:
            triangles.append((edge[0], edge[1], i))
    
    final_triangles = []
    for tri in triangles:
        if tri[0] < n and tri[1] < n and tri[2] < n:
            final_triangles.append(tri)
    
    return final_triangles


