import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///mediaid.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    
cloudinary.config(
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key = os.getenv('CLOUDINARY_API_KEY'),
    api_secret = os.getenv('CLOUDINARY_API_SECRET_KEY')
)