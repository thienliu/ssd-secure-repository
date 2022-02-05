from app import db
from app.main.models import Base
from datetime import datetime

class File(Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    file_size = db.Column(db.Integer, nullable=False)
    file_hash = db.Column(db.String(256), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def formattedSize(self):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if self.file_size < 1024.0:
                return "%3.1f %s" % (self.file_size, x)
            self.file_size /= 1024.0