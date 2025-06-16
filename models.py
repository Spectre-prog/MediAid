from flask_sqlalchemy import SQLAlchemy
from datetime import datetime #to be able to get the time a user uploads a particular insurance doc

db = SQLAlchemy() #initializing

class User(db.Model): #creating a model named user in my postresql
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100)) #max 100 characters
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(20))


class InsuranceDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    filename = db.Column(db.String(200))
    file_url = db.Column(db.String(500))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
