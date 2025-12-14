import struct
from typing import List, Tuple
from triangulator.models import Point, Triangle

def serialize_pointset(points: List[Point]) -> bytes:
    """
    Convertir les points en format binaires
    
    paramétres:
        points: liste de points
    
    Retourne:
        Une representation binaire des points
    """
    num_points = len(points)
    data = struct.pack('<I', num_points)
    
    for x, y in points:
        data += struct.pack('<ff', x, y)
    
    return data


def deserialize_pointset(data: bytes) -> List[Point]:
    """
    C'est l'opération inverse de serialize_pointset
    
    parametres:
        data: Données binaires représentant des pointss.
    
    Retourne:
        Une liste de points.
    
    """
    if len(data) < 4:
        raise ValueError("Data too short to contain point count")
    
    num_points = struct.unpack('<I', data[:4])[0]
    expected_length = 4 + num_points * 8
    
    if len(data) != expected_length:
        raise ValueError(
            f"Invalid data length: expected {expected_length}, got {len(data)}"
        )
    
    points = []
    offset = 4
    
    for _ in range(num_points):
        x, y = struct.unpack('<ff', data[offset:offset + 8])
        points.append((x, y))
        offset += 8
    
    return points


def serialize_triangles(vertices: List[Point], triangles: List[Triangle]) -> bytes:
    """
    Convertit une triangulation (sommets + triangles) en format binaire
    
    paramétres:
        vertices: Liste des sommets (points) de la triangulation
        triangles:  Liste des triangles et les indices référencent les sommets dans la liste
    
    Retourne:
        Données binaires représentant la triangulation.
    """
    # Part 1: Vertices (PointSet format)
    data = serialize_pointset(vertices)
    
    # Part 2: Triangles
    num_triangles = len(triangles)
    data += struct.pack('<I', num_triangles)
    
    for i, j, k in triangles:
        data += struct.pack('<III', i, j, k)
    
    return data


def deserialize_triangles(data: bytes) -> Tuple[List[Point], List[Triangle]]:
    """
    Convertit des données binaires en une triangulation (sommets + triangles). C'est l'opération inverse de serialize_triangles.
    
    paramétres:
        data: Données binaires représentant une triangulation.
    
    Retourne:
        Un tuple contenant la liste des sommets et la liste des triangles.
    
    """
    if len(data) < 4:
        raise ValueError("Data too short")
    
    # Partie 1: lire points
    num_vertices = struct.unpack('<I', data[:4])[0]
    vertices_end = 4 + num_vertices * 8
    
    if len(data) < vertices_end:
        raise ValueError("Data too short for vertices")
    
    vertices = deserialize_pointset(data[:vertices_end])
    
    # Partie 2: lire triangles
    if len(data) < vertices_end + 4:
        raise ValueError("Data too short for triangle count")
    
    num_triangles = struct.unpack('<I', data[vertices_end:vertices_end + 4])[0]
    expected_length = vertices_end + 4 + num_triangles * 12
    
    if len(data) != expected_length:
        raise ValueError(
            f"Invalid data length: expected {expected_length}, got {len(data)}"
        )
    
    triangles = []
    offset = vertices_end + 4
    
    for _ in range(num_triangles):
        i, j, k = struct.unpack('<III', data[offset:offset + 12])
        
        # Validate indices
        if i >= num_vertices or j >= num_vertices or k >= num_vertices:
            raise ValueError(f"Triangle index out of bounds: ({i}, {j}, {k})")
        
        triangles.append((i, j, k))
        offset += 12
    
    return vertices, triangles


