from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #initializing

class User(db.Model): #creating a model named user in my postresql
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100)) #max 100 characters
    email = db.Column(db.String(120), unique=True)