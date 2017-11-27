from __init__ import app
from flask import jsonify

from src.controllers.user import user_api
from src.controllers.board import board_api
#from src.controllers.board import 
from src.controllers.validators.exception import CustomException


@app.errorhandler(CustomException)
def own_error(error):
    response = jsonify({'msg': error.message})
    response.status_code = 500
    return response


app.register_blueprint(user_api)
app.register_blueprint(board_api)




app.run(debug = True)