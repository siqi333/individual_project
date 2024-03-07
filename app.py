from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import mysql.connector
import connect
import re
from flask_hashing import Hashing

app = Flask(__name__)
hashing = Hashing(app)  #create an instance of hashing

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor(dictionary=True)
    return dbconn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    # solving login here
    username = request.form.get("username")
    password = request.form.get("password")
    # ...
    return "Login Successful"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST" and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # variables for regist info
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        # check if account exist in database
        cursor = getCursor()
        cursor.execute('select 1 from secureaccount where username = %s', (username,))
        account = cursor.fetchone()
		# if account exist show error message, if not then verify characters
        if account:
            msg = 'account already exist'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # after verification, insert account info into database
            hashed = hashing.hash_value(password, salt='emma_use_salt')
            cursor.execute('insert into secureaccount values (null, %s, %s, %s)', (username, hashed, email,))
            msg = 'You have successfully registered!'
            return render_template("registed.html", msg=msg)
        return render_template("register.html", msg=msg)
    else:
        msg = 'please attend the page'
        return render_template("register.html", msg=msg)

if __name__ == "__main__":
    app.run()