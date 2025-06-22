import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()


SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  #this is to connect the project to the cloud postgresql database
SQLALCHEMY_TRACK_MODIFICATIONS = False

cloudinary.config(
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key = os.getenv('CLOUDINARY_API_KEY'),
    api_secret = os.getenv('CLOUDINARY_API_SECRET_KEY')
) #nb: i made this because normal sql database like postgresql cannot store very large files so this is the real storage for the files why the sql is acting like a notebook