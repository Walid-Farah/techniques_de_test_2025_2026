from typing import List, Tuple

Point = Tuple[float, float]
Triangle = Tuple[int, int, int]


class PointSet:
    def __init__(self, points: List[Point]):
        self.points = points
    
    def __len__(self) -> int:
        return len(self.points)
    
    def __getitem__(self, index: int) -> Point:
        return self.points[index]


class Triangles:
    def __init__(self, vertices: List[Point], triangles: List[Triangle]):
        self.vertices = vertices
        self.triangles = triangles
    
    def __len__(self) -> int:
        return len(self.triangles)