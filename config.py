import os
import psycopg2
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  #this is to connect the project to the cloud postgresql database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

# cloudinary.config(
#     cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
#     api_key = os.getenv('CLOUDINARY_API_KEY'),
#     api_secret = os.getenv('CLOUDINARY_API_SECRET_KEY')
# ) #nb: i made this because normal sql database like postgresql cannot store very large files so this is the real storage for the files why the sql is acting like a notebook