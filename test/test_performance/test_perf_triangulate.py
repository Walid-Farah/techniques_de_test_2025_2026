import time
import random
import pytest

@pytest.mark.performance
def test_perf_triangulate_10_points():
    """Test avec 10 points"""
    
    points = [(random.random(), random.random()) for _ in range(10)]
    
    start = time.time()
    # triangles = triangulate(points)
    triangulate(points)
    duration = time.time() - start
    
    print(f"\nTriangulation de 10 points: {duration:.6f}s")
    assert duration < 0.1


@pytest.mark.performance
def test_perf_triangulate_100_points():
    """Test avec 100 points"""
    
    points = [(random.random() * 100, random.random() * 100) for _ in range(100)]
    
    start = time.time()
    triangulate(points)
    duration = time.time() - start
    
    print(f"\nTriangulation de 100 points: {duration:.6f}s")
    assert duration < 1.0


@pytest.mark.performance
def test_perf_triangulate_1000_points():
    """Test avec 1000 points"""
    
    points = [(random.random() * 1000, random.random() * 1000) for _ in range(1000)]
    
    start = time.time()
    triangulate(points)
    duration = time.time() - start
    
    print(f"\nTriangulation de 1000 points: {duration:.6f}s")
    assert duration < 12.0


@pytest.mark.performance
def test_perf_serialize_pointset_large():
    """Test seralisation avec 10000 points"""
    
    points = [(float(i), float(i * 2)) for i in range(10000)]
    
    start = time.time()
    serialize_pointset(points)
    duration = time.time() - start
    
    print(f"\nSérialisation de 10000 points: {duration:.6f}s")
    assert duration < 0.5


@pytest.mark.performance
def test_perf_deserialize_pointset_large():
    """Test deseralisation avec 10000 points"""
    
    points = [(float(i), float(i * 2)) for i in range(10000)]
    binary = serialize_pointset(points)
    
    start = time.time()
    deserialize_pointset(binary)
    duration = time.time() - start
    
    print(f"\nDésérialisation de 10000 points: {duration:.6f}s")
    assert duration < 0.5


@pytest.mark.performance
def test_perf_serialize_triangles_large():
    """Serialisation triangles"""
    
    vertices = [(float(i), float(i * 2)) for i in range(1000)]

    triangles = [(i, i + 1, i + 2) for i in range(0, 997, 3)]
    
    start = time.time()
    serialize_triangles(vertices, triangles)
    duration = time.time() - start
    
    print(f"\nSérialisation de {len(triangles)} triangles: {duration:.6f}s")
    assert duration < 0.5


@pytest.mark.performance
def test_perf_roundtrip_large():
    """Test complet avec serialisation et déserialisation"""
    
    vertices = [(float(i), float(i * 2)) for i in range(1000)]
    triangles = [(i, i + 1, i + 2) for i in range(0, 997, 3)]
    
    start = time.time()
    binary = serialize_triangles(vertices, triangles)
    deserialize_triangles(binary)
    duration = time.time() - start
    
    print(f"\nTemps: {duration:.6f}s")
    assert duration < 1.0