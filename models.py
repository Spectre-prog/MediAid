from flask_sqlalchemy import SQLAlchemy
from datetime import datetime #to be able to get the time a user uploads a particular insurance doc

db = SQLAlchemy() #initializing

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))  # <-- Add this line
    email = db.Column(db.String(120), unique=True, nullable=False)
    dob = db.Column(db.String(20))
    password = db.Column(db.String(128))
    language = db.Column(db.String(20)) #creating a model named user in my postresql



class InsuranceDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    filename = db.Column(db.String(200))
    file_url = db.Column(db.String(500))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
