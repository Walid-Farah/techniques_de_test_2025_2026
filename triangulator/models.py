from typing import List, Tuple

Point = Tuple[float, float]
Triangle = Tuple[int, int, int]


class PointSet:
    """
    Représente une collection de points dans un espace 2D.
    """

    def __init__(self, points: List[Point]):
        """
        Initialise l'ensemble de points.

        parametres:
            points (List[Point]): Une liste de tuples représentant les coordonnées (x, y).
        """
        self.points = points
    
    def __len__(self) -> int:
        """
        Retourne: Le nombre total de points.
        """
        return len(self.points)
    
    def __getitem__(self, index: int) -> Point:
        """
        Permet l'accès à un point par son index.

        parametres:
            index: La position du point dans la liste.

        Retourne:
            Le tuple (x, y) correspondant à l'index.
        """
        return self.points[index]


class Triangles:
    """
    Représente un maillage composé de sommets et de triangles reliant ces sommets.
    """

    def __init__(self, vertices: List[Point], triangles: List[Triangle]):
        """
        Initialise la structure de triangles.

        parametres:
            vertices: La liste des sommets (points 2D).
            triangles: La liste des triangles, où chaque triangle est défini par 3 indices pointant vers 'vertices'.
        """
        self.vertices = vertices
        self.triangles = triangles
    
    def __len__(self) -> int:
        """
        Retourne le nombre de triangles définis.
        """
        return len(self.triangles)