from flask import Flask
from flask_mongoengine import MongoEngine

from abc import ABCMeta
from datetime import datetime

app = Flask(__name__)

app.config.from_object('config')