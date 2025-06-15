import os
from dotenv import load_dotenv

load_dotenv()

class Config: #this is to connect the project to the cloud postgresql database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False