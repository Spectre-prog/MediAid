from flask import Flask, flash, session, render_template, redirect, url_for, request, jsonify
from cloudinary.uploader import upload
import config
from config import * # You imported everything in the config.py by using the *, which is causing the errors i face here, CyberCoder

from config import Config # this is the name of the class we needed to conect the SQLALCHEMY, the one Ugoeze named class Config:

from models import db, User, InsuranceDocument #importing infos/models from the file named model.py

app = Flask(__name__, template_folder='template', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI # I also added the Config to the SQLALCHEMY_DATABASE_URI, cause without it, the output i was having is an undefined error

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
 #loads the db details from the config class in config.py
 # I also changed the config in this line to Config using an uppercase C, as it was defined in the config.py

db.init_app(app) #connects the sqlalchemy to the project(app)

# So guys lemme know if i cause errors over there, also what is it supposed to display??? Mine just ran the code and wrote done, exited within 2.35 seconds