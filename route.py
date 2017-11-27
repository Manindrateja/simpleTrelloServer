# from flask import jsonify, Blueprint, redirect, url_for, request, render_template
# from __init__ import User

# blu_print = Blueprint('test', __name__)

# @blu_print.route('/<b>')

# def hello_world1(b):
# 	a = {"a": 'Hello World' + b}
#   	return jsonify(a);

# @blu_print.route('/<b>/<c>')
# def print_a(b,c):
# 	print "blue print" 
# 	return jsonify({b: c})


# @blu_print.route('/post/<name>/<email>/<username>')
# def getPosts(name,email,username):
# 	#User(name = 'name', email = 'email' ).save()
# 	User.objects.create(**{'name' : name, 'email': email, 'username': username})
# 	return jsonify({'name' : name, 'email': email, 'username': username})

# @blu_print.route('/allposts')
# def getAllPosts():
# 	r =[]
# 	for user in User.objects.all():
# 		r.append({
# 				'name': user.name,
# 				'email': user.email,
# 				'username': user.username,
# 				'id': user.id.__str__()
# 			})
# 	return jsonify(r)

# @blu_print.route('/postbyID/<pid>')
# def getPostsById(pid):
# 	user = User.objects(id==pid).first()
# 	r = {
# 			'name': user.name,
# 			'email': user.email,
# 			'username': user.username,
# 			'id': user.id.__str__()
# 			}
# 	return jsonify(r)


# @blu_print.route('/success/<name>')
# def success(name):
#    return 'welcome %s' % name

# @blu_print.route('/login',methods = ['POST', 'GET'])
# def login():
#    if request.method == 'POST':
#       user = request.form['nm']
#       return redirect(url_for('test.success',name = user))
#    else:
#       #user = request.args.get('nm', 'll')
#       #return redirect(url_for('test.success',name = user))
#       return render_template('login.html')

# if __name__ == '__main__':
#    app.run(debug = True)


