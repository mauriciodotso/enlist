from flask import Flask, request, Response, make_response, request, current_app, jsonify
from functools import update_wrapper
from datetime import timedelta
from dbapi.api import DBAPI
from bson.objectid import ObjectId
import random
import string
import datetime
import json
import hmac
import hashlib

app = Flask(__name__)

url = "*"
dbapi = DBAPI()

######
#Test#
######
def test_database(database):
    global dbapi
    dbapi = DBAPI(database=database)

#######################
#Crossdomain decorator#
#######################
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def has_permission(token, user_id):
    session = dbapi.sessions.get(request.json['token']) 

    return session['user_id'] == user_id

###########
#Login API#
###########
def make_salt():
    salt = ""
    for i in range(5):
        salt = salt + random.choice(string.ascii_letters)
    return salt

def make_pw_hash(pw,salt=None):
    if salt == None:
        salt = make_salt();
    return hashlib.sha256(pw + salt).hexdigest()+","+ salt

def valid_user(username, password):
    user = dbapi.users.get(username)

    if not user:
        return False
    
    salt = user['password'].split(',')[1]
    
    return user['password'] == make_pw_hash(password, salt)

def generate_token(n):
    token = ""
    
    for i in xrange(n):
        token += random.choice(string.ascii_letters)

    return token

@app.route("/login", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def login():
        """Login.

        Method:
            POST
        
        Args:
            username (str): User's username
            password (str): User's password

        Returns:
            200: If user's was successfully logged in.
            str: A cookies is set with the token value.
                
        Raises:
            400: If the login failed.
            404: If a invalide user os password is passed
            500: Internal server problem.
        """
        try:
            if valid_user(request.json['username'], request.json['password']):
                token = generate_token(128)

                try:
                    dbapi.sessions.insert({'_id': token, 'username': request.json['username']})
                    user = dbapi.users.get(request.json['username'])
                except Exception:
                    return jsonify(message="We had a problem processing your request! Try again later."), 500
        

                return jsonify(token=token, message="Success!"), 200
            else:
                return jsonify(message="Invalid Login!"), 404
        except Exception:
            return jsonify(message="Error! Maybe missing args."), 400
        
        return response

@app.route("/logout", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def logout():
        """Logout.

        Method:
            POST
        
        Args:
            token (str): User's token

        Returns:
            200: If user is successfully logged out.
                
        Raises:
            400: If the logout failed.
            500: Internal server problem.
        """
        try:
            dbapi.sessions.remove(request.json['token'])
        except Exception:
            return jsonify(message="We had a problem processing your request! Try again later."), 500
        
        return jsonify(message="Success!"), 200

##########
#User API#
##########
@app.route("/user/create", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def user_create():
	"""Creates a user.
        
        Method:
            POST

        Args:
            username(str): User's username
            password(str): User's password
            
        Returns:
            201: If user is created 

        Raises:
            400: If can't create user
            409: If the username already exists
        """ 
        try:
            user_search = dbapi.users.get(request.json['username'])

            if user_search:
                    return jsonify(message="User already exists!"), 409

            password = make_pw_hash(request.json['password'])

            user = {'_id': request.json['username'], 'password': password, 'movies': [], 'books': []}

            try:
                dbapi.users.insert(user)
            except Exception:
                return jsonify("We had a problem processing your request! Try again later."), 500
            
            return  jsonify(message="Success! User created."), 201
        except Exception:
            return jsonify(message="Error! Maybe missing args."), 400

@app.route("/user/get", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def user_get():
        """Get specified user info.

        Method:
            POST
        
        Args:
            username (int): User's username
            token (str): User's session token

        Returns:
            json: Returns a json containing the user's information
                {
                    'username': 
                }
        Raises:
            403: If a invalid token is passed, or no token is passed, or invalid permission.
            404: If the specified Id does not exist.
        """
        pass

@app.route("/user/update", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def user_update():
        """Update specified user info.

        Method:
            POST
        
        Args:
            username (str): User's username
            token (str): User's session token
            password(Option[str]): User's updated password

        Returns:
            200: If User's info were updated

        Raises:
            403: If a invalid token is passed, or no token is passed, or invalid permission.
            404: If the specified Id does not exist.
            400: If the user was not updated.
        """
        try:
            user = dbapi.users.get(request.json['username'])
           
            if not has_permission(request.json['token'], request.json['username']):
                return jsonify(message="Access Denied"), 403
            
            if not user:
                return jsonify(message="Couldn't find the specified user!"), 404

            if 'password' in request.json:
                    user['password'] = make_pw_hash(request.json['password'])

            try:
                dbapi.users.update(user)
            except Exception:
                return jsonify(message="We had a problem processing your request! Try again later."), 500
            
            return  jsonify(message="Success! User updated."), 200
        except Exception:
            return jsonify(message="Error! Maybe missing args."), 400

@app.route("/user/delete", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def user_delete():
        """Delete specified user.

        Method:
            POST
        
        Args:
            username (str): User's username
            token (str): User's session token

        Returns:
            200: If the user was deleted

        Raises:
            403: If a invalid token is passed, or no token is passed or invalid permission.
            404: If the specified Id does not exist.
        """
        try:
            user = dbapi.users.get(request.json['_id'])

            if not has_permission(request.json['token'], request.json['username']):
                return jsonify(message="Access Denied"), 403
            
            if not user:
                return jsonify(message="Couldn't find the specified Id"), 404
           
            try:
                dbapi.users.remove(user['_id'])
                dbapi.sessions.remove_all({'username': user['username']})
            except Exception:
                return jsonify(message="We had a problem processing your request! Try again later."), 500
            
            return  jsonify(message="Success! User removed."), 200
        except Exception:
            return jsonify(message="Error! Maybe missing args."), 400

@app.route("/user/addbook", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def user_add_book():
	pass

@app.route("/user/deletebook", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def user_delete_book():
	pass

@app.route("/user/updatebook", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def user_update_book():
	pass

@app.route("/user/addmovie", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def user_add_movie():
	pass

@app.route("/user/deletemovie", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def user_delete_movie():
	pass

@app.route("/user/updatemovie", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def user_update_movie():
	pass

##########
#Book API#
##########
@app.route("/book/create", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def book_create():
	pass

@app.route("/book/get", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def book_get():
	pass

@app.route("/book/update", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def book_update():
	pass

@app.route("/book/delete", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def book_delete():
	pass

@app.route("/book/search", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def book_all():
	pass

###########
#Movie API#
###########
@app.route("/movie/create", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def movie_create():
	pass

@app.route("/movie/get", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def movie_get():
	pass

@app.route("/movie/update", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def movie_update():
	pass

@app.route("/movie/delete", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def movie_delete():
	pass

@app.route("/movie/search", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def movie_all():
	pass

if __name__ == "__main__":
    app.run()
