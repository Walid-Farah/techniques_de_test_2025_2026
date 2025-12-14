import requests
from typing import List
from triangulator.models import Point
from triangulator.serialization import deserialize_pointset


class PointSetManagerClient:
    """Client pour l'API PointSetManager."""
    
    def __init__(self, base_url: str):
        """IInitialise le client.

        parametres:
            base_url: URL de base du service PointSetManager.
        """
        self.base_url = base_url.rstrip('/')
    
    def get_pointset(self, pointset_id: str) -> List[Point]:
        """Récupère un ensemble de points (PointSet) via son identifiant.

        parametres:
            pointset_id: UUID de l'ensemble de points.

        Retourne:
            Une liste de points.

        Raises:
            requests.HTTPError: Si la requête échoue (timeout, erreur de connexion, etc.).
            ValueError: Si le format de la réponse est invalide.
        """
        url = f"{self.base_url}/pointset/{pointset_id}"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
        except requests.Timeout:
            raise requests.HTTPError("PointSetManager timeout", response=None)
        except requests.ConnectionError:
            raise requests.HTTPError("PointSetManager unreachable", response=None)
        
        if response.status_code == 200:
            return deserialize_pointset(response.content)
        
        raise requests.HTTPError(f"Unexpected status: {response.status_code}")
