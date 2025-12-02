import pytest
import struct
# import unittest
from unittest.mock import Mock, patch
from triangulator.app import app
from requests import HTTPError


@pytest.fixture
def client():
    """Creation d'un client test."""
    app.config['TESTING'] = False
    app.config["PROPAGATE_EXCEPTIONS"] = False
    with app.test_client() as client:
        yield client


def test_api_triangulate_success(client):
    """Test requete triangulation avec succes"""
    points = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    
    with patch('triangulator.app.pointset_client.get_pointset') as mock_get:
        mock_get.return_value = points
        
        response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
        
        assert response.status_code == 200
        assert response.content_type == 'application/octet-stream'
        assert len(response.data) > 0


def test_api_triangulate_invalid_id_format(client):
    """Test aevc une UUID invalide"""
    response = client.get('/triangulation/invalid-id')
    
    assert response.status_code == 400
    assert response.json['code'] == 'INVALID_ID'


def test_api_triangulate_empty_id(client):
    """Test avec un ID vide"""
    response = client.get('/triangulation/')
    
    assert response.status_code == 404


def test_api_triangulate_pointset_not_found(client):
    """Test avec un Pointset qui n'existe pas."""
    from requests import HTTPError
    from unittest.mock import Mock
    
    with patch('triangulator.app.pointset_client.get_pointset') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        error = HTTPError()
        error.response = mock_response
        mock_get.side_effect = error
        
        response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
        
        assert response.status_code == 404
        assert response.json['code'] == 'NOT_FOUND'

def test_api_pointsetmanager_unreachable(client):
    """Test Pointsetmanager est unreachable (n'est pas atteints)"""
    from requests import HTTPError
    
    with patch('triangulator.app.pointset_client.get_pointset') as mock_get:
        mock_get.side_effect = HTTPError("PointSetManager unreachable")
        
        response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
        
        assert response.status_code == 503
        assert response.json['code'] == 'SERVICE_UNAVAILABLE'


def test_api_triangulate_insufficient_points(client):
    """Test avec moins de 3 points"""
    points = [(0.0, 0.0), (1.0, 1.0)]
    
    with patch('triangulator.app.pointset_client.get_pointset') as mock_get:
        mock_get.return_value = points
        
        response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
        
        assert response.status_code == 400
        assert response.json['code'] == 'INSUFFICIENT_POINTS'



def test_api_triangulate_collinear_points(client):
    with patch('triangulator.app.pointset_client.get_pointset', side_effect=Exception("boom")):
        
        response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')

        assert response.status_code == 500
        assert response.json['code'] == 'INTERNAL_ERROR'
        assert response.json['message'] == 'Internal server error'


def test_api_response_binary_format(client):
    """Test avec un format binaire valide"""
    points = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    
    with patch('triangulator.app.pointset_client.get_pointset') as mock_get:
        mock_get.return_value = points
        
        response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
        
        data = response.data
        assert len(data) >= 4
        vertex_count = struct.unpack('<I', data[:4])[0]
        assert vertex_count == 3


def test_app_bad_request_from_pointsetmanager(client):
    with patch('triangulator.app.pointset_client.get_pointset') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 400
        
        error = HTTPError()
        error.response = mock_response
        mock_get.side_effect = error
        
        # Faire la requête
        response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
        
        # Vérifications
        assert response.status_code == 400
        assert response.json['code'] == 'BAD_REQUEST'
        assert 'Invalid request to PointSetManager' in response.json['message']


def test_app_invalid_pointset_data(client):
    """Test quand les données du PointSet sont invalides (ValueError)."""
    with patch('triangulator.app.pointset_client.get_pointset') as mock_get:
        # Simuler une ValueError lors de la désérialisation
        mock_get.side_effect = ValueError("Invalid binary format: corrupted data")
        
        # Faire la requête
        response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
        
        # Vérifications
        assert response.status_code == 500
        assert response.json['code'] == 'INVALID_DATA'
        assert 'Invalid PointSet data' in response.json['message']
        assert 'corrupted data' in response.json['message']



def test_app_triangulation_failed(client):
    """Test quand la triangulation échoue (points colinéaires par exemple)."""
    # Points colinéaires qui vont faire échouer la triangulation
    collinear_points = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]
    
    with patch('triangulator.app.pointset_client.get_pointset') as mock_get:
        mock_get.return_value = collinear_points
        
        # Faire la requête
        response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
        
        # Vérifications
        assert response.status_code == 500
        assert response.json['code'] == 'TRIANGULATION_FAILED'
        assert 'Triangulation failed' in response.json['message']
        assert 'point colineaire impossible de faire une triangulation' in response.json['message'].lower()



def test_app_serialization_failed(client):
    """Test quand la sérialisation du résultat échoue."""
    # Points valides pour la triangulation
    valid_points = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    
    with patch('triangulator.app.pointset_client.get_pointset') as mock_get:
        mock_get.return_value = valid_points
        
        # Faire échouer la sérialisation
        with patch('triangulator.app.serialize_triangles') as mock_serialize:
            mock_serialize.side_effect = Exception("Serialization error: memory issue")
            
            # Faire la requête
            response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
            
            # Vérifications
            assert response.status_code == 500
            assert response.json['code'] == 'SERIALIZATION_FAILED'
            assert 'Failed to serialize result' in response.json['message']
            assert 'memory issue' in response.json['message']
            