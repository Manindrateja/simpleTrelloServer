from src.models.users import User,UserToken
from src.models.boards import Board,List,Task
from mongoengine.queryset.visitor import Q

from src.controllers.validators.exception import CustomException
from datetime import datetime

def getAllUsers():
	allusers = []
	users = User.objects.all()
	for user in users:
		allusers.append(user.transform())
	return allusers

def findUser(id):
	return User.objects(id = id).first()

def register(user):
	user = User.objects.create(**user)
	return user.transform()

def login(user):
	# print user['email'], user['password']
	user = User.objects(email = user['email'], password = user['password']).first()
	print user
	if not user:
		raise CustomException("Invalid credential")
	else:
		token = UserToken.objects.create(token = user.get_id(), user = user)
        return {
            'name': user.name,
            'email': user.email,
            'id': user.get_id(),
            'username': user.username,
            'token': token.token
        }

def getUserByToken(token):
	# userToken = UserToken.objects(token = token).first()
	userToken = UserToken.objects.filter(expiresAt__gt = datetime.now(), token = token).first()
	if userToken:
		return userToken.user
	else:
		raise CustomException("Invalid User")

def createBoard(name, token):
	board = {}
	board['name'] = name
	board['owner'] = getUserByToken(token)
	board = Board.objects.create(**board)
	return board.transform();

def getAllBoards(token):
	user = getUserByToken(token)
	boards = Board.objects.filter(Q(owner = user) | Q(members__in = [user])).all()
	return [ board.transform() for board in boards ]

def getBoard(id, token):
	# board = Board.objects(id = id).first()
	user = getUserByToken(token)
	board = Board.objects.filter(Q(id = id) & (Q(owner = user) | Q(members__in = [user]))).first()
	if board:
		return board.getAll()
	else:
		raise CustomException("No Board exists")

def getBoardById(id):
	board = Board.objects(id = id).first()
	if board:
		return board
	else:
		raise CustomException("No Board exists")

def getOrderNumberForList(board):
	return len(board.lists) + 1

def getOrderNumberForTask(listitem):
	return len(listitem.tasklists) + 1

def createList(name, boardId):
	boardlist = {}
	boardlist['name'] = name
	board = getBoardById(boardId)
	boardlist['orderNumber'] = getOrderNumberForList(board)
	new_list = List.objects.create(**boardlist)
	board.lists.append(new_list)
	board.save()
	return new_list.transform()

def getListById(id, error = True):
	listItem = List.objects(id = id).first()
	if listItem:
		return listItem
	else:
		raise CustomException("No list exists") if error else None

def createTask(task, token, listId):
	task['assignedTo'] = findUser(task['assignedTo'])
	task['createdBy'] = getUserByToken(token)
	listItem = getListById(listId)
	task['orderNumber'] = getOrderNumberForTask(listItem)
	task = Task.objects.create(**task)
	listItem.tasklists.append(task)
	listItem.save()
	return task.transform()

def updateTask(task, tokem):
	task['assignedTo'] = findUser(task['assignedTo'])
	task = Task.objects(id = task['id']).update(**task)
	return task

def getTaskbyId(id):
	task = Task.objects(id = id).first()
	return task

def moveTask(taskId, fromlistId, tolistId, fromOrdernumber, toOrdernumber):
	task = getTaskbyId(taskId)

	print fromOrdernumber, toOrdernumber
	
	fromList = List.objects.filter( id = fromlistId).first()
	tt = fromList.tasklists
	for item in tt:
		if item.orderNumber > fromOrdernumber:
			Task.objects(id = item.get_id()).update(orderNumber = item.orderNumber - 1)

	toList = List.objects.filter( id = tolistId).first()
	rr = toList.tasklists
	for item in rr:
		if item.orderNumber >= toOrdernumber:
			Task.objects(id = item.get_id()).update(orderNumber = item.orderNumber + 1)

	task.orderNumber = toOrdernumber;
	task.save()

	if List.objects(id = fromlistId).update_one(pull__tasklists = task):
		List.objects(id = tolistId).update_one(add_to_set__tasklists = task)
		return "success"

	return "error"

def reOrderTasks(tasks, listId):

	targetLists = List.objects.filter( id = listId).first()
	if targetLists:
		tt = targetLists.tasklists
		for item in tt:
			for item2 in tasks:
				if item.get_id() == item2['id']:
					Task.objects(id = item.get_id()).update(orderNumber = item2['orderNumber'])
		return "success"
	else:
		return "error"

def reOrderlists(lists, boardId):
	targetBoard = Board.objects.filter( id = boardId).first()
	if targetBoard:
		tt = targetBoard.lists
		for item in tt:
			for item2 in lists:
				print item.get_id(),item2['id']
				if item.get_id() == item2['id']:
					print item.get_id(),item2['orderNumber']
					List.objects(id = item.get_id()).update(orderNumber = item2['orderNumber'])
		return "success"
	else:
		return "error"

def addMember(boardId, userId):
	board = getBoardById(boardId)
	user = findUser(userId)
	board.members.append(user)
	board.save()
	return board.transform()


def removeMember(boardId, userId):
	# board = getBoardById(boardId)
	board = Board.objects.filter( id = boardId).first()
	user = findUser(userId)
	if Board.objects(id = boardId).update_one(pull__members = user):
		board.save()
		return "success"

	return "error"


def deleteBoard(boardId, token):
	user = getUserByToken(token)
	if Board.objects.filter(Q(owner = user) & Q(id = boardId)).all():
		return Board.objects.filter(Q(owner = user) & Q(id = boardId)).delete()
	else:
		return "error"

def deleteTask(taskId, listId):
	task = getTaskbyId(taskId)
	if List.objects(id = listId).update_one(pull__tasklists = task):
		return Task.objects.filter(id = taskId).delete()
	else:
		return "error"

def deleteList(listId, boardId):
	board = Board.objects.filter(id = boardId).all()
	if board:
		listItem = getListById(listId)
		Board.objects(id = boardId).update_one(pull__lists = listItem)
		return List.objects.filter(id = listId).delete()
	else:
		return "error"

def sortList(boardId, lists):
	board = Board.objects.filter(id = boardId).first()	
	if board:
		board.lists = [];
		for item in lists:
			itemD = getListById(item, error = False)
			if itemD:
				board.lists.append(itemD)
		board.save()
		return "success"
	else: 
		return "error"

def sortTasklist(listId, tasklists, boardId):
	targetLists = List.objects.filter( id = listId).first()
	board = Board.objects.filter(id = boardId).first();
	if targetLists:
		targetLists.tasklists = [];
		# targetLists.tasklists = Task.objects.filter(id__in = tasklists).all()
		for item in tasklists:
			task = Task.objects.filter(id = item).first()
			if task:
				targetLists.tasklists.append(task)
		targetLists.save()
		board.save()
		return "success"
	else:
		raise CustomException("Cannot Save the sort")

# def moveSortTask(froml, to):
# 	sortTasklist(froml['id'], froml['tasklists']);
# 	sortTasklist(to['id'], to['tasklists']);
# 	return "success"

def moveSortTask(fromlistId, to, taskId, boardId):
	task = getTaskbyId(taskId)
	board = Board.objects.filter(id = boardId).first();
	if List.objects(id = fromlistId).update_one(pull__tasklists = task):
		sortTasklist(to['id'], to['tasklists'], boardId);
		board.save()
		return "success"
	else:
		raise CustomException("Cannot Save the sort")

def saveBoard(boardId, lists, listIds):
	sortList(boardId, listIds)
	for item in lists:
		print item['id']
		sortTasklist(item['id'],item['tasklists'], boardId)

	return "success"	

def checkBoardChange(data):
	# print data
	board = Board.objects.filter(id = data['boardId']).first();
	# print data['time']
	# print board.get_updatedAt()
	if round(float(data['time'])) == round(float(board.get_updatedAt())):
		return "0"
	return "1"