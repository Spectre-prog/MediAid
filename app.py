from flask import Flask, flash, session, render_template, redirect, url_for, request, jsonify
from config import Config #importing infos from the file named config.py
from models import db, User#importing infos from the file named model.py

app = Flask(__name__, template_folder='template', static_folder='static')
app.config.from_object(Config) #loads the db details from the config class in config.py

db.init_app(app) #connects the sqlalchemy to the project(app)