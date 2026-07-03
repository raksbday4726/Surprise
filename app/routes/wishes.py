import os
import uuid
import logging

from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)


from app.extensions import db
from app.models.wishes import Wish
from app.models.uploads import Upload

wishes_bp = Blueprint('wishes', __name__)


def allowed_file(filename):
    """Check if the file has an allowed extension."""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']


@wishes_bp.route('/wishes', methods=['GET'])
def get_wishes():
    """Retrieve all active wishes from the database, ordered by newest first."""
    try:
        # Keep index-friendly predicate: status + created_at.
        wishes = (
            Wish.query.filter(Wish.status == 'active')
            .order_by(Wish.created_at.desc())
            .limit(100)
            .all()
        )
        wishes_list = [w.to_dict() for w in wishes]
        return jsonify({
            "success": True,
            "message": "Wishes retrieved successfully",
            "data": {
                "wishes": wishes_list
            }
        }), 200
    except Exception:
        logger.exception("Failed to retrieve wishes")
        # Do not leak internal exception strings to clients.
        return jsonify({
            "success": False,
            "message": "Database is temporarily unavailable.",
            "errors": ["internal_error"]
        }), 500


@wishes_bp.route('/wishes', methods=['POST'])
def create_wish():
    """Create a new wish, handling optional photo uploads."""
    visitor_name = request.form.get('visitor_name', '').strip()
    wish_message = request.form.get('wish_message', '').strip()

    errors = []

    # 1. Validation: visitor_name (2-100 characters)
    if not visitor_name:
        errors.append("Visitor name is required.")
    elif len(visitor_name) < 2 or len(visitor_name) > 100:
        errors.append("Visitor name must be between 2 and 100 characters.")

    # 2. Validation: wish_message (max 300 characters)
    if not wish_message:
        errors.append("Wish message is required.")
    elif len(wish_message) > 300:
        errors.append("Wish message cannot exceed 300 characters.")

    # 3. File upload and validation
    photo_file = request.files.get('photo')
    saved_filepath = None
    stored_name = None
    photo_filename = None
    photo_url = None

    if photo_file and photo_file.filename != '':
        if not allowed_file(photo_file.filename):
            errors.append("Invalid file type. Allowed formats: PNG, JPG, JPEG, WEBP.")
        elif photo_file.content_type not in {'image/png', 'image/jpeg', 'image/jpg', 'image/webp'}:
            errors.append("Invalid MIME type. Executable or system files are strictly rejected.")
        else:
            try:
                photo_file.seek(0, os.SEEK_END)
                file_size = photo_file.tell()
                photo_file.seek(0)

                if file_size > 5 * 1024 * 1024:
                    errors.append("File size exceeds the 5MB maximum limit.")
            except Exception:
                errors.append("Unable to determine file size.")

        if not errors:
            original_name = secure_filename(photo_file.filename)
            if '.' not in original_name:
                errors.append("Invalid file name.")
            else:
                ext = original_name.rsplit('.', 1)[1].lower()
                photo_filename = original_name
                stored_name = f"{uuid.uuid4().hex}.{ext}"

                upload_dir = current_app.config['UPLOAD_FOLDER']
                os.makedirs(upload_dir, exist_ok=True)

                saved_filepath = os.path.join(upload_dir, stored_name)
                try:
                    photo_file.save(saved_filepath)
                    # Single source of truth: upload serving endpoint is under /api
                    photo_url = f"{request.url_root.rstrip('/')}/api/uploads/{stored_name}"

                except Exception:
                    errors.append("Failed to save uploaded file.")



    if errors:
        if saved_filepath and os.path.exists(saved_filepath):
            try:
                os.remove(saved_filepath)
            except OSError:
                pass
        logger.warning("Upload validation failed")
        return jsonify({
            "success": False,
            "message": "Validation failed",
            "errors": errors
        }), 400


    # 4. Save to MySQL database
    # Important: DB changes are wrapped in a single transaction.
    try:
        new_upload = None
        if 'file_size' in locals() and photo_url and stored_name:
            new_upload = Upload(
                original_name=photo_filename,
                stored_name=stored_name,
                mime_type=photo_file.content_type,
                file_size=file_size,
            )
            db.session.add(new_upload)

        new_wish = Wish(
            visitor_name=visitor_name,
            wish_message=wish_message,
            photo_filename=photo_filename,
            photo_url=photo_url,
            status='active'
        )
        db.session.add(new_wish)

        db.session.commit()

        logger.info("Upload success")
        return jsonify({
            "success": True,
            "message": "Wish created successfully",
            "data": new_wish.to_dict()
        }), 201


    except Exception:
        logger.exception("Upload DB failure")
        db.session.rollback()
        if saved_filepath and os.path.exists(saved_filepath):
            try:
                os.remove(saved_filepath)
            except OSError:
                pass
        return jsonify({
            "success": False,
            "message": "Database error: unable to save wish.",
            "errors": ["internal_error"]
        }), 500





@wishes_bp.route('/uploads/<filename>', methods=['GET'])
def serve_upload(filename):
    """Serve uploaded images securely, validating files exist."""
    upload_dir = current_app.config['UPLOAD_FOLDER']

    safe_filename = secure_filename(filename)

    # Prevent path traversal attempts that might normalize into an empty/changed name.
    if not safe_filename or safe_filename != filename:
        return jsonify({
            "success": False,
            "message": "File not found",
            "errors": ["The requested photo does not exist on this server."]
        }), 404

    full_path = os.path.join(upload_dir, safe_filename)
    if not os.path.exists(full_path):
        return jsonify({
            "success": False,
            "message": "File not found",
            "errors": ["The requested photo does not exist on this server."]
        }), 404

    return send_from_directory(upload_dir, safe_filename)


