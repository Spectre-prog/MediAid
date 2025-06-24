from flask_sqlalchemy import SQLAlchemy
from datetime import datetime #to be able to get the time a user uploads a particular insurance doc

db = SQLAlchemy() #initializing

class User(db.Model): #creating a model named user in my postresql to store users login details
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100)) #max 100 characters
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(20))


class InsuranceDocument(db.Model): #creating a model to store the details of insurance docs the user uploads
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(200))
    file_url = db.Column(db.String(500))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

user = db.relationship('User', backref='documents') #this allows easy access btw users and their docs