from flask import jsonify, Blueprint, redirect, url_for, request, render_template

# from src.models.boards import Board,List,Task

from src.repository import users


board_api = Blueprint('board', __name__)

@board_api.route('/createBoard', methods = ['POST'])
def createBoard():
	print 'createBoard called'
	board = users.createBoard(request.json.get('name'), request.headers.get('token'))
	# board = {}
	# # print request.json.get('name')
	# # print request.headers.get('token')
	# board['name'] = request.json.get('name')
	# board['owner'] = users.getUserByToken(request.headers.get('token'))
	# board = Board.objects.create(**board)
	
	return jsonify(board)

@board_api.route('/getAllBoards', methods = ['GET'])
def getAllBoards():
	boards = users.getAllBoards(request.headers.get('token'))
	# user = users.getUserByToken(request.headers.get('token'))
	# boards = Board.objects.filter(owner = user).all()
	# return jsonify([ board.transform() for board in boards ])
	return jsonify(boards)

@board_api.route('/createList', methods = ['POST'])
def createList():
	new_list = users.createList(request.json.get('name'), request.json.get('boardId'))
	return jsonify(new_list)

@board_api.route('/getBoard/<boardId>', methods= ['GET'])
def getBoard(boardId):
	board = users.getBoard(boardId, request.headers.get('token'))
	return jsonify(board)

@board_api.route('/createTask', methods = ['POST'])
def createTask():
	task = {}
	task['name'] = request.json.get('name')
	# task['title'] = request.json.get('title')
	task['assignedTo'] = request.json.get('assignedTo')
	task['description'] = request.json.get('description')
	task = users.createTask(task, request.headers.get('token'), request.json.get('listId'))
	return jsonify(task)

@board_api.route('/updateTask', methods = ['POST', 'PUT'])
def updateTask():
	task = {}
	task['id'] = request.json.get('id')
	task['name'] = request.json.get('name')
	# task['title'] = request.json.get('title')
	task['assignedTo'] = request.json.get('assignedTo')
	task['description'] = request.json.get('description')
	task['orderNumber'] = request.json.get('orderNumber')
	task = users.updateTask(task, request.headers.get('token'))
	return jsonify(task)


@board_api.route('/reorderTask', methods = ['POST', 'PUT'])
def reOrderTasks():
	return jsonify(users.reOrderTasks(request.json.get('tasks'), request.json.get('listId')))

@board_api.route('/reorderlists', methods = ['POST', 'PUT'])
def reOrderList():
	return jsonify(users.reOrderlists(request.json.get('lists'), request.json.get('boardId')))

@board_api.route('/moveTask', methods = ['POST', 'PUT'])
def moveTask():
	return users.moveTask(request.json.get('id'), request.json.get('fromlistId'), request.json.get('tolistId'), request.json.get('fromOrdernumber'), request.json.get('toOrderNumber'))	


@board_api.route('/addMember', methods = ['POST'])
def addMember():
	return jsonify(users.addMember(request.json.get('boardId'),request.json.get('userId')))

@board_api.route('/removeMember', methods = ['POST'])
def removeMember():
	return jsonify(users.removeMember(request.json.get('boardId'),request.json.get('userId')))


@board_api.route('/deleteBoard', methods = ['POST'])
def deleteBoard():
	return jsonify(users.deleteBoard(request.json.get('boardId'),request.headers.get('token')))

@board_api.route('/deleteTask', methods = ['POST'])
def deleteTask():
	return jsonify(users.deleteTask(request.json.get('taskId'), request.json.get('listId')))

@board_api.route('/deleteList', methods = ['POST'])
def deleteList():
	return jsonify(users.deleteList(request.json.get('listId'), request.json.get('boardId')))

@board_api.route('/sortList', methods = ['POST'])
def sortList():
	if users.sortList(request.json.get('boardId'),request.json.get('lists')):
		return jsonify('success')
	return 'error'

@board_api.route('/sortTask', methods = ['POST'])
def sortTasklist():
	if users.sortTasklist(request.json.get('listId'),request.json.get('tasklists'),request.json.get('boardId')):
		return jsonify('success')
	return 'error'

@board_api.route('/moveSortTask', methods = ['POST'])
def moveSortTask():
	if users.moveSortTask(request.json.get('fromlistId'),request.json.get('to'),request.json.get('id'),request.json.get('boardId')):
		return jsonify('success')
	return 'error'
	
@board_api.route('/saveBoard', methods = ['POST'])
def saveBoard():
	if users.saveBoard(request.json.get('id'), request.json.get('lists'), request.json.get('listIds')):
		return jsonify('success')
	return 'error'

@board_api.route('/checkBoardChange', methods = ['POST', 'GET'])
def checkBoardChange():
	return jsonify(users.checkBoardChange(request.json))

