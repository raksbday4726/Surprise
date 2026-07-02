from __future__ import annotations

from datetime import datetime

from app.extensions import db


class Upload(db.Model):
    """Uploaded file metadata stored in MySQL.

    Note:
        - Schema is intentionally preserved for Alembic/DB compatibility.
        - No relationship is introduced (no foreign keys in current schema).
    """

    __tablename__ = 'uploads'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_name = db.Column(db.String(255), nullable=False)
    stored_name = db.Column(db.String(255), nullable=False, unique=True)
    mime_type = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.BigInteger, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<Upload id={self.id!r} stored_name={self.stored_name!r} "
            f"mime_type={self.mime_type!r} file_size={self.file_size!r}>"
        )


