from __init__ import app
from flask import jsonify,render_template

from src.controllers.user import user_api
from src.controllers.board import board_api
#from src.controllers.board import 
from src.controllers.validators.exception import CustomException


# socket imports
# from flask_socketio import SocketIO, emit
# import time
# socketio = SocketIO(app)

# @app.route('/')                                                                 
# def index():                                                                    
#     return render_template('index.html')

# thread = None                                                                   


# def background_thread():                                                        
#     while True:                                                                 
#         socketio.emit('message', {'goodbye': "Goodbye"})                        
#         time.sleep(5)                                                           


# @socketio.on('connect')                                                         
# def connect():                                                                  
#     global thread                                                               
#     if thread is None:                                                          
#         thread = socketio.start_background_task(target=background_thread)


@app.errorhandler(CustomException)
def own_error(error):
    response = jsonify({'msg': error.message})
    response.status_code = 500
    return response


app.register_blueprint(user_api)
app.register_blueprint(board_api)


# socketio.run(app, debug=True)

app.run(debug = True)