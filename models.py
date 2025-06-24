from flask_sqlalchemy import SQLAlchemy
from datetime import datetime #to be able to get the time a user uploads a particular insurance doc
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy() #initializing

class User(db.Model): #creating a model named user in my postresql to store users login details
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100)) #max 100 characters
    email = db.Column(db.String(40), unique=True)
    dob = db.Column(db.DateTime)
    phonenumber = db.Column(db.String(25))
    hashed_password = db.Column(db.Text)

    def __init__(self, name, email, dob, phonenumber, password):
        self.name = name
        self.email = email
        self.dob = dob
        self.phonenumber = phonenumber
        self.set_password(password)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

class InsuranceDocument(db.Model): #creating a model to store the details of insurance docs the user uploads
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(200))
    file_url = db.Column(db.String(500))
    upload_date = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc))

user = db.relationship('User', backref='documents') #this allows easy access btw users and their docs