from app import db
from flask_login import UserMixin
from datetime import datetime


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    filepath = db.Column(db.Text, nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(100), nullable=False)
    private = db.Column(db.Boolean, default=False)
    downloads = db.Column(db.Integer, default=0)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)