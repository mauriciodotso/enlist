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
    """Add book to user list.

    Method:
        POST

    Args:
        username (str): User's username
        token (str): User's session token
        book_id(ObjId): Book's id

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

        book = dbapi.books.get(request.json['book_id'])

        if not book:
            return jsonify(message="Couldn't find the specified book!"), 404

        try:
            dbapi.users.insert_book(request.json['username'], request.json['book_id'])
        except Exception:
            return jsonify(message="We had a problem processing your request! Try again later."), 500

        return  jsonify(message="Success! Book added."), 200
    except Exception:
        return jsonify(message="Error! Maybe missing args."), 400

@app.route("/user/deletebook", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def user_delete_book():
    pass

@app.route("/user/updatebook", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def user_update_book():
    """Update book status on user list.

    Method:
        POST

    Args:
        username (str): User's username
        token (str): User's session token
        book_id(ObjId): Book's id
        status:(int): Book's status

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

        book = dbapi.books.get(request.json['book_id'])

        if not book:
            return jsonify(message="Couldn't find the specified book!"), 404

        try:
            dbapi.users.update_book(request.json['username'], request.json['book_id'], request.json['status'])
        except Exception:
            return jsonify(message="We had a problem processing your request! Try again later."), 500

        return  jsonify(message="Success! Book updated."), 200
    except Exception:
        return jsonify(message="Error! Maybe missing args."), 400

@app.route("/user/addmovie", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def user_add_movie():
    """Add movie to user list.

    Method:
        POST

    Args:
        username (str): User's username
        token (str): User's session token
        movie_id(ObjId): Movie's id

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

        movie = dbapi.movies.get(request.json['movie_id'])

        if not movie:
            return jsonify(message="Couldn't find the specified movie!"), 404

        try:
            dbapi.users.insert_movie(request.json['username'], request.json['movie_id'])
        except Exception:
            return jsonify(message="We had a problem processing your request! Try again later."), 500

        return  jsonify(message="Success! Movie added."), 200
    except Exception:
        return jsonify(message="Error! Maybe missing args."), 400
    pass

@app.route("/user/deletemovie", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def user_delete_movie():
    pass

@app.route("/user/updatemovie", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def user_update_movie():
    """Update movie status on user list.

    Method:
        POST

    Args:
        username (str): User's username
        token (str): User's session token
        movie_id(ObjId): Movie's id
        status:(int): Movie's status

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

        movie = dbapi.movies.get(request.json['movie_id'])

        if not movie:
            return jsonify(message="Couldn't find the specified movie!"), 404

        try:
            dbapi.users.update_movie(request.json['username'], request.json['movie_id'], request.json['status'])
        except Exception:
            return jsonify(message="We had a problem processing your request! Try again later."), 500

        return  jsonify(message="Success! Movie updated."), 200
    except Exception:
        return jsonify(message="Error! Maybe missing args."), 400

##########
#Book API#
##########
@app.route("/book/create", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def book_create():
    """Creates a book.

    Method:
        POST

    Args:
        token(str): User's token
        title(str): Book's title
        year(date): Book's year
        edition(int): Book's edition
        cover(str): Book's cover url addres

    Returns:
        id(str): Created book Id
        201: If book is created

    Raises:
        403: If a invalid token is passed, or no token is passed, or invalid permission.
        400: If can't create book
    """
    try:
        if not has_permission(request.json['token'], 'Admin'):
            return jsonify(message="Access Denied"), 403

        #ToDo: Check if title and edition already exists.

        book = {'title': request.json['title'], 'year': request.json['year'], 'edition': request.json['edition'], 'cover': request.json['cover']}

        try:
            _id = dbapi.books.insert(book).inserted_id
        except Exception:
            return jsonify(message="We had a problem processing your request! Try again later."), 500

        return  jsonify(message="Success! Book created.", _id=str(_id)), 201
    except Exception:
        return "Error! Maybe missing args.", 400

@app.route("/book/get", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def book_get():
    """Returns a book according to the passed id.

    Method:
        POST

    Args:
        id(str): Book's id

    Returns:
        book(json): Return's a json object containing the book information.
        200: If book exists

    Raises:
        404: If no Book is found
    """
    try:
        try:
            book = dbapi.books.get(request.json['id'])

            if not book:
                return jsonify(message="Couldn't find the specified book!"), 404
        except Exception:
            return jsonify(message="We had a problem processing your request! Try again later."), 500

        return  jsonify(message="Success! Book found.", book=book), 201
    except Exception:
        return "Error! Maybe missing args.", 400

@app.route("/book/update", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def book_update():
    """Updates a book.

    Method:
        POST

    Args:
        token(str): User's token
        id(str): Book's id
        title(str): Book's title
        year(date): Book's year
        edition(int): Book's edition
        cover(str): Book's cover url addres

    Returns:
        200: If book is updated

    Raises:
        403: If a invalid token is passed, or no token is passed, or invalid permission.
        400: If can't update book
        404: If no Book is found
    """
    try:
        if not has_permission(request.json['token'], 'Admin'):
            return jsonify(message="Access Denied"), 403

        #ToDo: Check if title and edition already exists.

        book = dbapi.books.get(request.json['id'])

        if not book:
            return jsonify(message="Couldn't find the specified book!"), 404

        for arg in request.json:
            if arg in book:
                book[arg] = request.json[arg]

        try:
            dbapi.books.update(book)
        except Exception:
            return jsonify(message="We had a problem processing your request! Try again later."), 500

        return  jsonify(message="Success! Book updated."), 200
    except Exception:
        return "Error! Maybe missing args.", 400

@app.route("/book/delete", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def book_delete():
    #ToDo: Delete Book and each reference to that book in a User list?? or delete only id there is no reference??
    pass

@app.route("/book/search", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def book_all():
    """Get all books.

    Method:
        POST

    Args:
        title: (Optional[int]): Search books containing the specified title.
        limit: (Optional[int]): Limit the total books returned, default is 10.
        page: (Optional[int]): Especifies the page of books.

    Returns:
        json: Returns an array of books, with the next and last page if any.
            {
                'books': []
                'total': Total books
                'limit': Books per page
            }
    Raises:
        500: If the specified page does not exist.
    """
    try:
        page = 0
        limit = 10

        if 'page' in request.json:
            page = request.json['page']

        if 'limit' in request.json:
            limit = request.json['limit']

        try:
            if 'title' in request.json:
                results, total = dbapi.books.get_all_by_title(title, limit, page)
            else:
                results, total = dbapi.books.get_all(limit, page)

            for result in results:
                result['_id'] = str(result['_id'])
                result['datetime'] = result['datetime'].strftime("%m/%d/%Y %H:%M")

        except Exception:
            return jsonify(message="We had a problem processing your request! Try again later."), 500

        response = {'books': results, 'limit': limit, 'total': total}

        return json.dumps(response), 200
    except Exception:
        return "Error! Maybe missing args.", 400

###########
#Movie API#
###########
@app.route("/movie/create", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def movie_create():
    """Creates a movie.

    Method:
        POST

    Args:
        token(str): User's token
        title(str): Movie's title
        year(date): Movie's year
        cover(str): Movie's cover url addres

    Returns:
        id(str): Created movie Id
        201: If movie is created

    Raises:
        403: If a invalid token is passed, or no token is passed, or invalid permission.
        400: If can't create movie
    """
    try:
        if not has_permission(request.json['token'], 'Admin'):
            return jsonify(message="Access Denied"), 403

        #ToDo: Check if title and year already exists.

        movie = {'title': request.json['title'], 'year': request.json['year'], 'cover': request.json['cover']}

        try:
            _id = dbapi.movies.insert(movie).inserted_id
        except Exception:
            return jsonify(message="We had a problem processing your request! Try again later."), 500

        return  jsonify(message="Success! Movie created.", _id=str(_id)), 201
    except Exception:
        return "Error! Maybe missing args.", 400

@app.route("/movie/get", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def movie_get():
    """Returns a movie according to the passed id.

    Method:
        POST

    Args:
        id(str): Movie's id

    Returns:
        movie(json): Return's a json object containing the movie information.
        200: If movie exists

    Raises:
        404: If no Movie is found
    """
    try:
        try:
            movie = dbapi.movies.get(request.json['id'])

            if not movie:
                return jsonify(message="Couldn't find the specified movie!"), 404
        except Exception:
            return jsonify(message="We had a problem processing your request! Try again later."), 500

        return  jsonify(message="Success! Movie found.", movie=movie), 201
    except Exception:
        return "Error! Maybe missing args.", 400

@app.route("/movie/update", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def movie_update():
    """Updates a movie.

    Method:
        POST

    Args:
        token(str): User's token
        id(str): Movie's id
        title(str): Movie's title
        year(date): Movie's year
        cover(str): Movie's cover url addres

    Returns:
        200: If movie is updated

    Raises:
        403: If a invalid token is passed, or no token is passed, or invalid permission.
        400: If can't update movie
        404: If no Movie is found
    """
    try:
        if not has_permission(request.json['token'], 'Admin'):
            return jsonify(message="Access Denied"), 403

        #ToDo: Check if title and edition already exists.

        movie = dbapi.movies.get(request.json['id'])

        if not movie:
            return jsonify(message="Couldn't find the specified movie!"), 404

        for arg in request.json:
            if arg in movie:
                movie[arg] = request.json[arg]

        try:
            dbapi.movies.update(movie)
        except Exception:
            return jsonify(message="We had a problem processing your request! Try again later."), 500

        return  jsonify(message="Success! Movie updated."), 200
    except Exception:
        return "Error! Maybe missing args.", 400

@app.route("/movie/delete", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def movie_delete():
    #ToDo: Delete Movie and each reference to that movie in a User list?? or delete only id there is no reference??
    pass

@app.route("/movie/search", methods=['POST', 'OPTIONS'])
@crossdomain(origin=url)
def movie_all():
    """Get all movies.

    Method:
        POST

    Args:
        title: (Optional[int]): Search movies containing the specified title.
        limit: (Optional[int]): Limit the total movies returned, default is 10.
        page: (Optional[int]): Especifies the page of movies.

    Returns:
        json: Returns an array of movies, with the next and last page if any.
            {
                'movies': []
                'total': Total movies
                'limit': Movies per page
            }
    Raises:
        500: If the specified page does not exist.
    """
    try:
        page = 0
        limit = 10

        if 'page' in request.json:
            page = request.json['page']

        if 'limit' in request.json:
            limit = request.json['limit']

        try:
            if 'title' in request.json:
                results, total = dbapi.movies.get_all_by_title(title, limit, page)
            else:
                results, total = dbapi.movies.get_all(limit, page)

            for result in results:
                result['_id'] = str(result['_id'])
                result['datetime'] = result['datetime'].strftime("%m/%d/%Y %H:%M")

        except Exception:
            return jsonify(message="We had a problem processing your request! Try again later."), 500

        response = {'movies': results, 'limit': limit, 'total': total}

        return json.dumps(response), 200
    except Exception:
        return "Error! Maybe missing args.", 400

if __name__ == "__main__":
    app.run()
