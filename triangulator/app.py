import os
from flask import Flask, jsonify, Response


app = Flask(__name__)

# Configuration
POINTSET_MANAGER_URL = os.environ.get(
    'POINTSET_MANAGER_URL',
    'http://localhost:5000'
)



@app.route('/triangulation/<pointset_id>', methods=['GET'])
def get_triangulation():
    return jsonify({"message": "Pas encore implemanter"}), 501


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