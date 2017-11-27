from flask_cors import CORS
from flask import Flask
# from flask_mongoengine import MongoEngine
from src.models.base import db




# from abc import ABCMeta
# from datetime import datetime

app = Flask(__name__)

# CORS for application
CORS(app)

app.config.from_object('config')

db.init_app(app)


from src.controllers.user import user_api

app.register_blueprint(user_api)

