from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health():
    # Lightweight DB check handled by SQLAlchemy connection attempt.
    # Kept minimal to avoid frontend/UI changes.
    try:
        from extensions import db
        conn = db.engine.connect()
        conn.close()
        return jsonify({
            "success": True,
            "database": "connected"
        }), 200
    except Exception:
        return jsonify({
            "success": False,
            "database": "disconnected"
        }), 503

