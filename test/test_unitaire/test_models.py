from triangulator.models import PointSet,Triangles


def test_Pointset():
    points=[(0,0),(3,3)]
    pointset=PointSet(points)
    assert pointset.__len__()==2
    assert pointset.__getitem__(0)==(0,0)


def test_Triangles():
    points=[(0,0),(1,0),(0,1)]
    triangle=[(0,1,2)]
    triangles=Triangles(points,triangle)
    assert triangles.__len__()==1