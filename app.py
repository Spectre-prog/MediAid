from flask import Flask, flash, session, render_template, redirect, url_for, request, jsonify
from cloudinary.uploader import upload
import config
from config import * #importing infos from the file named config.py
from models import db, User, InsuranceDocument #importing infos/models from the file named model.py

app = Flask(__name__, template_folder='template', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
 #loads the db details from the config class in config.py

db.init_app(app) #connects the sqlalchemy to the project(app)