from __future__ import annotations

from datetime import datetime

from app.extensions import db


class Wish(db.Model):
    """Wish entry submitted by a visitor.

    Notes:
        - Serialization contract must remain compatible with the existing frontend.
        - Schema is intentionally preserved (no column/type/index changes).
    """

    __tablename__ = 'wishes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    visitor_name = db.Column(db.String(100), nullable=False)
    wish_message = db.Column(db.String(300), nullable=False)

    photo_filename = db.Column(db.String(255), nullable=True)
    photo_url = db.Column(db.String(255), nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )
    status = db.Column(
        db.String(20),
        nullable=False,
        default='active',
        index=True,
    )

    def __repr__(self) -> str:
        return (
            f"<Wish id={self.id!r} name={self.visitor_name!r} "
            f"status={self.status!r} created_at={self.created_at!r}>"
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize model to a dictionary compatible with existing frontend."""
        # Frontend expects keys: id, name, message, photo_url, createdAt
        if self.created_at:
            day = self.created_at.day
            month_name = self.created_at.strftime('%B')
            year = self.created_at.year
            formatted_date = f"{day} {month_name} {year}"
        else:
            formatted_date = ''

        return {
            'id': self.id,
            'name': self.visitor_name,
            'message': self.wish_message,
            'photo_url': self.photo_url,
            'createdAt': formatted_date,
        }


