from datetime import datetime
from extensions import db


class Upload(db.Model):
    __tablename__ = 'uploads'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_name = db.Column(db.String(255), nullable=False)
    stored_name = db.Column(db.String(255), nullable=False, unique=True)
    mime_type = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.BigInteger, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Wish(db.Model):
    __tablename__ = 'wishes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    visitor_name = db.Column(db.String(100), nullable=False)
    wish_message = db.Column(db.String(300), nullable=False)

    # Per spec
    photo_filename = db.Column(db.String(255), nullable=True)
    photo_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default='active', index=True)

    def to_dict(self):
        """Serialize model to a dictionary compatible with existing frontend."""
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
            'createdAt': formatted_date
        }

