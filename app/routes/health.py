from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health():
    """Health endpoint.

    Contract preserved: { success, database } with HTTP 200/503.
    """
    # Render Health Checks require HTTP 200 with a stable JSON response.
    try:
        from app.extensions import db
        with db.engine.connect():
            pass

        return jsonify({
            "success": True,
            "status": "healthy",
        }), 200
    except Exception:
        # Keep a consistent JSON shape; do not leak internals.
        return jsonify({
            "success": False,
            "status": "unhealthy",
        }), 503



