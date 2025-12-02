import pytest
from unittest.mock import Mock,patch
from requests import HTTPError, Timeout, ConnectionError

@patch('triangulator.client.requests.get')
def test_get_pointset_success_simple(mock_get):
    points = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    binary = serialize_pointset(points)
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = binary
    mock_get.return_value = mock_response
    
    client = PointSetManagerClient("http://localhost:5000")
    result = client.get_pointset("test-id-123")
    
    assert len(result) == 3
    assert result[0] == (0.0, 0.0)
    assert result[1] == (1.0, 0.0)
    assert result[2] == (0.5, 1.0)


@patch('triangulator.client.requests.get')
def test_get_pointset_timeout(mock_get):
    mock_get.side_effect = Timeout()
    
    client = PointSetManagerClient("http://localhost:5000")
    
    with pytest.raises(HTTPError, match="timeout"):
        client.get_pointset("timeout-id")


@patch('triangulator.client.requests.get')
def test_get_pointset_network_unreachable(mock_get):
    """Test avec réseau non disponible."""
    mock_get.side_effect = ConnectionError("Network is unreachable")
    
    client = PointSetManagerClient("http://10.0.0.1")
    
    with pytest.raises(HTTPError, match="unreachable"):
        client.get_pointset("network-id")




@patch('triangulator.client.requests.get')
def test_get_pointset_unexpected_status_code(mock_get):
    """Test avec un code de statut inattendu (non 200, mais pas d'exception)."""
    mock_response = Mock()
    mock_response.status_code = 202  # Accepted (rare pour un GET de retourner 202)
    mock_get.return_value = mock_response
    
    client = PointSetManagerClient("http://localhost:5000")
    
    with pytest.raises(HTTPError, match="Unexpected status: 202"):
        client.get_pointset("weird-status-id")

