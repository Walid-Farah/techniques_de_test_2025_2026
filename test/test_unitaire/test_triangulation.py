import struct
import pytest
from triangulator.serialization import serialize_triangles, deserialize_triangles, serialize_pointset, deserialize_pointset
from triangulator.algorithm import triangulate
from triangulator.geometry import duplication_point,sont_colineaires, point_in_circumcircle


def test_point_in_circumcircle():
    points=[(1,2), (3,6), (5,10), (7,14)]
    assert not point_in_circumcircle(points[0],points[1],points[2],points[3])


def test_pointset_serialization_empty():
    """Test serialisation avec 0 point"""
    points = []
    binary = serialize_pointset(points)
    
    assert len(binary) == 4
    assert struct.unpack('<I', binary[:4])[0] == 0


def test_pointset_serialization_single_point():
    """Test serialisation avec 1 point"""
    points = [(1.5, 2.0)]
    binary = serialize_pointset(points)
    
    assert len(binary) == 12  # 4 + 8
    assert struct.unpack('<I', binary[:4])[0] == 1
    x, y = struct.unpack('<ff', binary[4:12])
    assert abs(x - 1.5) < 1e-6
    assert abs(y - 2.0) < 1e-6


def test_pointset_serialization_multiple_points():
    """Test serialisation avec 3 point"""
    points = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    binary = serialize_pointset(points)
    
    assert len(binary) == 4 + 3 * 8
    assert struct.unpack('<I', binary[:4])[0] == 3


def test_pointset_deserialization_valid():
    """Test deserialisation"""
    # 2 points: (1.0, 2.0) et (3.0, 4.0)
    binary = struct.pack('<I', 2) + struct.pack('<ff', 1.0, 2.0) + struct.pack('<ff', 3.0, 4.0)
    points = deserialize_pointset(binary)
    
    assert len(points) == 2
    assert abs(points[0][0] - 1.0) < 1e-6
    assert abs(points[0][1] - 2.0) < 1e-6
    assert abs(points[1][0] - 3.0) < 1e-6
    assert abs(points[1][1] - 4.0) < 1e-6


def test_pointset_deserialization_invalid_length_too_short():
    """Test deserialization pas complet genere une erreur"""
    binary = struct.pack('<I', 2) + struct.pack('<ff', 1.0, 2.0)  # Missing second point
    
    with pytest.raises(ValueError, match="Invalid data length"):
        deserialize_pointset(binary)


def test_pointset_deserialization_invalid_length_too_long():
    """Test deserialisation on rajoutant une donnée"""
    binary = struct.pack('<I', 1) + struct.pack('<ff', 1.0, 2.0) + b'extra'
    
    with pytest.raises(ValueError, match="Invalid data length"):
        deserialize_pointset(binary)


def test_pointset_deserialization_too_short_for_count():
    """Test deserialisation qui correspond pas a un point trop petite"""
    binary = b'ab'
    
    with pytest.raises(ValueError, match="Data too short"):
        deserialize_pointset(binary)


def test_pointset_serialisation_deserialisation():
    """Test serialisation puis deserialisation."""
    original = [(1.5, 2.5), (3.7, 4.2), (-1.0, -2.0)]
    binary = serialize_pointset(original)
    restored = deserialize_pointset(binary)
    
    assert len(restored) == len(original)
    for orig, rest in zip(original, restored):
        assert abs(orig[0] - rest[0]) < 1e-6
        assert abs(orig[1] - rest[1]) < 1e-6


def test_pointset_extreme_values():
    """Test avec des valeurs extremes"""
    points = [(1e10, 1e-10), (-1e10, -1e-10), (0.0, 0.0)]
    binary = serialize_pointset(points)
    restored = deserialize_pointset(binary)
    
    assert len(restored) == 3


def test_pointset_large_dataset():
    """Test serialization of large dataset."""
    points = [(float(i), float(i * 2)) for i in range(1000)]
    binary = serialize_pointset(points)
    restored = deserialize_pointset(binary)
    
    assert len(restored) == 1000


# triangulation serialize
def test_triangles_serialization_empty():
    """Test serialization with no triangles."""
    vertices = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    triangles = []
    
    binary = serialize_triangles(vertices, triangles)
    
    # 4 (vertex count) + 3*8 (vertices) + 4 (triangle count)
    assert len(binary) == 4 + 3 * 8 + 4
    
    # Check triangle count is 0
    triangle_count_offset = 4 + 3 * 8
    assert struct.unpack('<I', binary[triangle_count_offset:triangle_count_offset + 4])[0] == 0


def test_triangles_serialization_single_triangle():
    """Test serialization with single triangle."""
    vertices = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    triangles = [(0, 1, 2)]
    
    binary = serialize_triangles(vertices, triangles)
    
    # 4 + 3*8 + 4 + 1*12
    expected_length = 4 + 3 * 8 + 4 + 1 * 12
    assert len(binary) == expected_length


def test_triangles_serialization_multiple_triangles():
    """Test serialization with multiple triangles."""
    vertices = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    triangles = [(0, 1, 2), (0, 2, 3)]
    
    binary = serialize_triangles(vertices, triangles)
    
    expected_length = 4 + 4 * 8 + 4 + 2 * 12
    assert len(binary) == expected_length


def test_triangles_deserialization_valid():
    """Test deserialization un triangles"""
    vertices = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    triangles = [(0, 1, 2)]
    
    binary = serialize_triangles(vertices, triangles)
    restored_vertices, restored_triangles = deserialize_triangles(binary)
    
    assert len(restored_vertices) == 3
    assert len(restored_triangles) == 1
    assert restored_triangles[0] == (0, 1, 2)


def test_triangles_deserialization_invalid_indices():
    """Test deserialization with out-of-bounds indices."""
    # Manually create invalid data
    binary = struct.pack('<I', 3)  # 3 vertices
    binary += struct.pack('<ff', 0.0, 0.0)
    binary += struct.pack('<ff', 1.0, 0.0)
    binary += struct.pack('<ff', 0.5, 1.0)
    binary += struct.pack('<I', 1)  # 1 triangle
    binary += struct.pack('<III', 0, 1, 5)  # Index 5 is out of bounds!
    
    with pytest.raises(ValueError, match="out of bounds"):
        deserialize_triangles(binary)


def test_triangles_roundtrip():
    """Test serialisation oui deserialisation."""
    vertices = [(1.0, 2.0), (3.0, 4.0), (5.0, 6.0), (7.0, 8.0)]
    triangles = [(0, 1, 2), (1, 2, 3)]
    
    binary = serialize_triangles(vertices, triangles)
    restored_vertices, restored_triangles = deserialize_triangles(binary)
    
    assert len(restored_vertices) == len(vertices)
    assert len(restored_triangles) == len(triangles)
    
    for orig, rest in zip(triangles, restored_triangles):
        assert orig == rest


def test_triangles_deserialization_too_short():
    """Test deserialisation donnée pas complete"""
    binary = b'abc'
    
    with pytest.raises(ValueError, match="too short"):
        deserialize_triangles(binary)


def test_triangles_duplicate_indices():
    """Test triangle with duplicate indices."""
    vertices = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    triangles = [(0, 0, 0)]  # Degenerate triangle
    
    binary = serialize_triangles(vertices, triangles)
    restored_vertices, restored_triangles = deserialize_triangles(binary)
    
    # Should deserialize successfully (validation is algorithm's job)
    assert restored_triangles[0] == (0, 0, 0)


def test_triangles_structure_validation():
    """Test that structure is correctly validated."""
    vertices = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    triangles = [(0, 1, 2)]
    
    binary = serialize_triangles(vertices, triangles)
    
    # Manually check structure
    num_vertices = struct.unpack('<I', binary[:4])[0]
    assert num_vertices == 3
    
    triangle_offset = 4 + 3 * 8
    num_triangles = struct.unpack('<I', binary[triangle_offset:triangle_offset + 4])[0]
    assert num_triangles == 1


#geometry


def test_triangulation_points_inf_3():
    serie_de_points=[[],[(1,1)],[(1,1),(2,2)]]
    for points in serie_de_points:
        with pytest.raises(ValueError):
            triangulate(points)


def test_cas_points_colineaires():
    points = [(1,2), (3,6), (5,10), (7,14),(4,8)]
    assert sont_colineaires(points)
    points = [(1,2), (3,6), (5,10), (7,14),(4,18)]
    assert not sont_colineaires(points)
    points = [(1,2), (3,6)]
    assert sont_colineaires(points)
    
    

def test_triangulation_points_colineaires():
    points = [(1,2), (3,6), (5,10), (7,14),(4,8)]
    with pytest.raises(ValueError):
        triangulate(points)


def test_point_duplicate():
    points=[(0,0),(0,0)]
    assert duplication_point(points)
    points=[(0,0),(0,1)]
    assert not duplication_point(points)


def test_triangulate_3_point():
    points=[(0,0),(0,1),(1,0)]
    assert len(triangulate(points))==1


def test_triangulate_4_points():
    points=[(0,0),(0,1),(1,0),(0.5,0.5)]
    assert 2<=len(triangulate(points))<=3


def test_triangulate_10_points():
    points = [
        (0.1, 0.2), (0.9, 0.1), (0.8, 0.9), (0.2, 0.8),
        (0.5, 0.5), (0.3, 0.3), (0.7, 0.3), (0.7, 0.7),
        (0.3, 0.7), (0.5, 0.1)
    ]
    triangles = triangulate(points)
    
    assert len(triangles) >= 6


def test_point_existant():
    points=[(0,0),(0,0)]
    with pytest.raises(ValueError):
        triangulate(points)


def test_deserialize_triangles_empty_after_count():
    binary = struct.pack('<I', 5)
    
    with pytest.raises(ValueError, match="Data too short for vertices"):
        deserialize_triangles(binary)


def test_deserialize_triangles_missing_triangle_count():
    """Test avec vertices complets mais pas de nombre de triangles."""
    # 2 vertices complets mais pas de triangle count
    binary = struct.pack('<I', 2)  # 2 vertices
    binary += struct.pack('<ff', 0.0, 0.0)  # 1er vertex
    binary += struct.pack('<ff', 1.0, 1.0)  # 2ème vertex
    # Manque les 4 bytes du triangle count
    
    with pytest.raises(ValueError, match="Data too short for triangle count"):
        deserialize_triangles(binary)



def test_deserialize_triangles_truncated_triangle_data():
    """Test avec triangles incomplets (manque des indices)."""
    # 2 vertices, 2 triangles annoncés mais seulement 1 triangle fourni
    binary = struct.pack('<I', 2)  # 2 vertices
    binary += struct.pack('<ff', 0.0, 0.0)  # Vertex 0
    binary += struct.pack('<ff', 1.0, 0.0)  # Vertex 1
    binary += struct.pack('<I', 2)  # 2 triangles annoncés
    binary += struct.pack('<III', 0, 1, 0)  # Seulement 1 triangle (12 bytes)
    # Manque le 2ème triangle (12 bytes supplémentaires attendus)
    
    with pytest.raises(ValueError, match="Invalid data length: expected"):
        deserialize_triangles(binary)