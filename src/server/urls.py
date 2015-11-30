from flask import Flask
app = Flask(__name__)


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

###########
#Login API#
###########
@app.route("/login", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def login():
	pass

@app.route("/logout", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def logout():
	pass


##########
#User API#
##########
@app.route("/user/create", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def user_create():
	pass

@app.route("/user/get", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def user_get():
	pass

@app.route("/user/update", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def user_update():
	pass

@app.route("/user/delete", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def user_delete():
	pass

@app.route("/user/addbook", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def user_delete():
	pass

@app.route("/user/deletebook", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def user_delete():
	pass

@app.route("/user/updatebook", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def user_delete():
	pass

@app.route("/user/addmovie", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def user_delete():
	pass

@app.route("/user/deletemovie", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def user_delete():
	pass

@app.route("/user/updatemovie", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def user_delete():
	pass

##########
#Book API#
##########
@app.route("/book/create", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def book_create():
	pass

@app.route("/book/get", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def book_get():
	pass

@app.route("/book/update", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def book_update():
	pass

@app.route("/book/delete", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def book_delete():
	pass

@app.route("/book/search", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def book_all():
	pass

###########
#Movie API#
###########
@app.route("/movie/create", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def book_create():
	pass

@app.route("/movie/get", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def book_get():
	pass

@app.route("/movie/update", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def book_update():
	pass

@app.route("/movie/delete", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def book_delete():
	pass

@app.route("/movie/search", methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://locahost:3000')
def book_all():
	pass

if __name__ == "__main__":
    app.run()
