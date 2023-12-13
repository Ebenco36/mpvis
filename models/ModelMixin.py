from database.db import db
from datetime import datetime


class ModelMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)