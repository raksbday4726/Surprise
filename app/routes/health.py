from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health():
    """Health endpoint.

    Contract preserved: { success, database } with HTTP 200/503.
    """
    try:
        from app.extensions import db

        # pool_pre_ping=True handles stale connections.
        with db.engine.connect():
            pass

        return jsonify({
            "success": True,
            "database": "connected",
        }), 200
    except Exception:
        return jsonify({
            "success": False,
            "database": "disconnected",
        }), 503


