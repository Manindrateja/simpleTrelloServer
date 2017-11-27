from flask import jsonify, Blueprint, redirect, url_for, request, render_template

from src.repository import users
from src.controllers.validators import validators

user_api = Blueprint('user', __name__)


@user_api.route('/register',methods = ['POST', 'GET'])
def registerUser():
    if request.method == 'POST':
        # validators.validateRegister(request.json)
        return jsonify(users.register(request.json))
	
@user_api.route('/getAllUser', methods = ['GET'])
def getAllUsers():
    return jsonify(users.getAllUsers())

@user_api.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        return jsonify(users.login(request.json));



