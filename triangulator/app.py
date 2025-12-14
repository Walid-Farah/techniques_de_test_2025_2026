import os
from flask import Flask, jsonify, Response
import requests
from triangulator.client import PointSetManagerClient
from triangulator.algorithm import triangulate
from triangulator.serialization import serialize_triangles


app = Flask(__name__)

# Configuration
POINTSET_MANAGER_URL = os.environ.get(
    'POINTSET_MANAGER_URL',
    'http://localhost:5000'
)

pointset_client = PointSetManagerClient(POINTSET_MANAGER_URL)


@app.route('/triangulation/<pointset_id>', methods=['GET'])
def get_triangulation(pointset_id: str):
    """Calcule la triangulation pour un ensemble de points (PointSet).
    
    parametres:
        pointset_id: UUID de l'ensemble de points.
    
    Retourne:
        Représentation binaire des triangles ou une erreur JSON.
    """
    # Valider le format de l'UUID
    if not pointset_id or len(pointset_id) != 36:
        return jsonify({
            'code': 'INVALID_ID',
            'message': 'Invalid PointSetID format'
        }), 400
    
    # Recuperer le PointSet depuis le PointSetManager
    try:
        points = pointset_client.get_pointset(pointset_id)
    except requests.HTTPError as e:
        if hasattr(e, 'response') and e.response is not None:
            if e.response.status_code == 404:
                return jsonify({
                    'code': 'NOT_FOUND',
                    'message': f'PointSet {pointset_id} not found'
                }), 404
            elif e.response.status_code == 400:
                return jsonify({
                    'code': 'BAD_REQUEST',
                    'message': 'Invalid request to PointSetManager'
                }), 400
        
        return jsonify({
            'code': 'SERVICE_UNAVAILABLE',
            'message': 'PointSetManager is unavailable'
        }), 503
    except ValueError as e:
        return jsonify({
            'code': 'INVALID_DATA',
            'message': f'Invalid PointSet data: {str(e)}'
        }), 500
    
    # Valider le nombre de points
    if len(points) < 3:
        return jsonify({
            'code': 'INSUFFICIENT_POINTS',
            'message': f'Need at least 3 points, got {len(points)}'
        }), 400
    
    # Calculer la triangulation
    try:
        triangles = triangulate(points)
    except ValueError as e:
        return jsonify({
            'code': 'TRIANGULATION_FAILED',
            'message': f'Triangulation failed: {str(e)}'
        }), 500
    
    # Sérialiser et retourner le résultat
    try:
        binary_data = serialize_triangles(points, triangles)
        return Response(binary_data, mimetype='application/octet-stream')
    except Exception as e:
        return jsonify({
            'code': 'SERIALIZATION_FAILED',
            'message': f'Failed to serialize result: {str(e)}'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'code': 'NOT_FOUND',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'code': 'INTERNAL_ERROR',
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)