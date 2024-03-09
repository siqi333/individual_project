from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import mysql.connector
import connect
import re
from flask import url_for
from flask import session
from flask_hashing import Hashing
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'HelloWorld'
hashing = Hashing(app)  #create an instance of hashing

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/images')

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    # dbconn = connection.cursor(dictionary=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/administrator")
def administrator():
    return render_template("Administrator.html")

@app.route("/pestcontroller")
def pestcontroller():
    return render_template("PestController.html")

@app.route("/staff")
def staff():
    return render_template("Staff.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form.get("username")
        userpassword = request.form.get("password")
        role = request.form.get("role")
        cursor = getCursor()
        cursor.execute('select u.user_id, u.user_name, u.password_hash, r.role_name from user u left join role r on u.role_id = r.role_id where u.user_name = %s;', (username,))
        
        account = cursor.fetchone()
        if account is not None:
            password = account[2]
            if hashing.check_value(password, userpassword, salt='emma_use_salt'):
            # If account exists in accounts table 
            # Create session data, we can access this data in other routes
                if role != account[3]:
                    msg = 'Invalid role'
                    return render_template('index.html', msg=msg)
                
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['role'] = account[3]

                
                # Redirect to home page
                if account[3] == "Administrator":
                    return redirect(url_for('administrator'))
                if account[3] == "Pest Controller":
                    return redirect(url_for('pestcontroller'))
                if account[3] == "Staff":
                    return redirect(url_for('staff'))
            else:
                #password incorrect
                msg = 'Incorrect password!'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST" and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # variables for regist info
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        role = request.form.get("role")
        # check if account exist in database
        cursor = getCursor()
        cursor.execute('select user_name from user where user_name = %s;', (username,))
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
            cursor.execute('insert into user(user_name, password_hash, role_id) values (%s, %s, %s)', (username, hashed, role))
            msg = 'You have successfully registered!'
            return render_template("index.html", msg=msg)
        return render_template("index.html", msg=msg)
    else:
        msg = 'please attend the page'
        return render_template("register.html", msg=msg)


@app.route("/staffedit", methods=["GET", "POST"])
def staffedit():
    if request.method == "POST":
        staffnumber = request.form.get("staffnumber")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        workphonenumber = request.form.get("workphonenumber")
        position = request.form.get("position")
        department = request.form.get("department")
        hiredate = request.form.get("hiredate")
        status = request.form.get("status")
        user_id = session['id']

        # check if the staff already exists
        cursor = getCursor()
        cursor.execute('select staff_number from staff_profile where user_id = %s;', (user_id,))
        account = cursor.fetchone()
        if account is None:
            print(user_id, staffnumber, firstname, lastname, email, workphonenumber, hiredate, position, department, status)
            cursor.execute(
                'insert into staff_profile(user_id, staff_number, first_name, last_name, email, phone, hire_date, position, department, status) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', 
                (user_id, staffnumber, firstname, lastname, email, workphonenumber, hiredate, position, department, status)
            )
            return redirect(url_for('staff'))
        
        cursor = getCursor()
        cursor.execute(
            'update staff_profile set staff_number = %s, first_name = %s, last_name = %s, email = %s, phone = %s, position = %s, department = %s, hire_date = %s, status = %s where user_id = %s;',
            (staffnumber, firstname, lastname, email, workphonenumber, position, department, hiredate, status, user_id)
        )
        return redirect(url_for('staff'))
    
    cursor = getCursor()
    cursor.execute(
        'select staff_number, first_name, last_name, email, phone, position, department, hire_date, status from staff_profile where user_id = %s;',
        (session['id'],)
    )
    account = cursor.fetchone()
    return render_template("staffedit.html", account=account)

@app.route("/guideadd", methods=["GET", "POST"])
def guideadd():
    if request.method == "POST":
        description = request.form.get("description")
        distribution = request.form.get("distribution")
        size = request.form.get("size")
        droppings = request.form.get("droppings")
        footprints = request.form.get("footprints")
        impacts = request.form.get("impacts")
        controlmethods = request.form.get("controlmethods")
        primaryimage = request.files["primaryimage"]
        secondaryimage = request.files["secondaryimage"]

        sf1 = secure_filename(primaryimage.filename)
        sf2 = secure_filename(secondaryimage.filename)

        filepath1 = os.path.join(UPLOAD_FOLDER, sf1)
        filepath2 = os.path.join(UPLOAD_FOLDER, sf2)

        primaryimage.save(filepath1)
        secondaryimage.save(filepath2)

        cursor = getCursor()
        cursor.execute(
            "insert into animal_guide(description, distribution, size, droppings, footprints, impacts, control_methods, primary_image, secondary_image) values (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
            (description, distribution, size, droppings, footprints, impacts, controlmethods, sf1, sf2)
        )
        return redirect(url_for('guide'))
    return render_template("guideadd.html")

# show the guide
@app.route("/guide")
def guide():
    cursor = getCursor()
    cursor.execute(
        "select animal_id, description, primary_image, secondary_image from animal_guide;"
    )
    guide = cursor.fetchall()
    return render_template("PestGuide.html", guide=guide)

if __name__ == "__main__":
    app.run()