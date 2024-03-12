from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
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
app.secret_key = 'emma_seesion_key'
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
    # if session['loggedin'] == True:
    #     return render_template("Administrator.html")
    # else:
    #     return redirect(url_for('login'))
    cursor = getCursor()
    cursor.execute(
		'select * from staff_profile;'
	)
    staff_rows = cursor.fetchall()
    cursor.execute(
		'select * from controller_profile;'
	)
    pestcon_rows = cursor.fetchall()
    return render_template("Administrator.html", staff_rows=staff_rows, pestcon_rows=pestcon_rows)

@app.route("/pestcontroller")
def pestcontroller():
    cursor = getCursor()
    cursor.execute(
		'select * from controller_profile;'
	)
    pestcon_rows = cursor.fetchall()
    return render_template("PestController.html", pestcon_rows=pestcon_rows)

@app.route("/staff")
def staff():
    cursor = getCursor()
    cursor.execute(
		'select * from staff_profile;'
	)
    staff_rows = cursor.fetchall()
    cursor.execute(
		'select * from controller_profile;'
	)
    pestcon_rows = cursor.fetchall()
    return render_template("staff.html", staff_rows=staff_rows, pestcon_rows=pestcon_rows)

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

@app.route("/guideupdate", methods=["POST"])
def guideupdate():
    description = request.form.get("description")
    distribution = request.form.get("distribution")
    size = request.form.get("size")
    droppings = request.form.get("droppings")
    footprints = request.form.get("footprints")
    impacts = request.form.get("impacts")
    controlmethods = request.form.get("controlmethods")
    primaryimage = request.files["primaryimage"]
    secondaryimage = request.files["secondaryimage"]
    animal_id = request.files.get("animal_id")

    sf1 = secure_filename(primaryimage.filename)
    sf2 = secure_filename(secondaryimage.filename)

    filepath1 = os.path.join(UPLOAD_FOLDER, sf1)
    filepath2 = os.path.join(UPLOAD_FOLDER, sf2)

    primaryimage.save(filepath1)
    secondaryimage.save(filepath2)

    cursor = getCursor()
    cursor.execute(
		"update animal_guide set description = %s,distribution = %s,size = %s,droppings = %s,footprints = %s,impacts = %s,control_methods = %s,primary_image = %s,secondary_image = %s where animal_id=%s;",
        (description, distribution, size, droppings, footprints, impacts, controlmethods, sf1, sf2, animal_id)
    )
    return redirect(url_for('guide_manage'))

# show the guide
@app.route("/guide")
def guide():
    cursor = getCursor()
    cursor.execute(
        "select animal_id, description, primary_image, secondary_image from animal_guide;"
    )
    guide = cursor.fetchall()
    return render_template("PestGuide.html", guide=guide)

@app.route("/guidedetail")
def guidedetail():
    animal_id = request.args.get('animal_id')
    cursor = getCursor()
    cursor.execute(
        "select * from animal_guide where animal_id = %s;",
        (animal_id,)
    )
    guide = cursor.fetchone()
    return render_template("PestGuideDetail.html", guide=guide)

@app.route("/guide_manage")
def guide_manage():
    cursor = getCursor()
    cursor.execute(
        "select animal_id, description, primary_image, secondary_image from animal_guide;"
    )
    guide = cursor.fetchall()
    return render_template("pest_guide_manage.html", guide=guide)

@app.route('/delete_guide/<guide_id>', methods=['POST'])
def delete_guide(guide_id):
    cursor = getCursor()
    cursor.execute(
		"delete from animal_guide where animal_id=%s;", (guide_id,)
    )
    return redirect(url_for('guide_manage'))

@app.route("/guidedetail_manage")
def guidedetail_manage():
    animal_id = request.args.get('animal_id')
    cursor = getCursor()
    cursor.execute(
        "select * from animal_guide where animal_id = %s;",
        (animal_id,)
    )
    guide = cursor.fetchone()
    return render_template("pest_guide_detail_manage.html", guide=guide)

# update controller profile
@app.route("/update_profile", methods=["GET","POST"])
def update_profile():
    cursor = getCursor()
    # cursor = connection.cursor(dictionary=True)
    
    if request.method == "POST":
        # Extract data from form submission
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        address = request.form.get('address')
        email = request.form.get('email')
        phone = request.form.get('phone')
        date_joined = request.form.get('datejoined')
        # date_joined_str = f"str_to_date('{date_joined}','%Y%m%d')"
        status = request.form.get('status')
        controller_id = request.form.get('pestcontrolleridnumber')
        user_id = session['id']

        # check if profile existing
        cursor = getCursor()
        cursor.execute(
			'select 1 from controller_profile where controller_id=%s;', (controller_id,)
        )
        profile = cursor.fetchone()
        if profile is None:
            cursor.execute(
				'insert into controller_profile values (%s, %s, %s, %s, %s, %s, %s, %s, %s);',
                (controller_id, user_id, first_name, last_name, address, email, phone, date_joined, status)
            )
            msg = 'profile not exist, added as new'
            return render_template('PestController.html', msg2=msg)
        
        # Update profile in database
        update_query = """
        UPDATE controller_profile
        SET first_name = %s, last_name = %s, address = %s, email = %s, phone = %s, date_joined = %s, status = %s
        WHERE controller_id = %s
        """
        cursor.execute(update_query, (first_name, last_name, address, email, phone, date_joined, status, controller_id))
        connection.commit()
        msg = 'Proifle updated'
        return render_template('PestController.html', msg2=msg)
        
    # Handle GET request
    else:
        # Fetch the existing profile data
        select_query = "SELECT * FROM controller_profile WHERE controller_id = %s"
        cursor.execute(select_query, (controller_id,))
        profile = cursor.fetchone()
        
        if profile:
            # Render the form with profile data
            return render_template('PestController.html')
        else:
            return "Profile not found", 404

# update admin profile
@app.route("/update_profile_admin", methods=["GET","POST"])
def update_profile_admin():
    cursor = getCursor()
    # cursor = connection.cursor(dictionary=True)
    
    if request.method == "POST":
        # Extract data from form submission
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        address = request.form.get('address')
        email = request.form.get('email')
        phone = request.form.get('phone')
        date_joined = request.form.get('datejoined')
        status = request.form.get('status')
        admin_id = request.form.get('adminid')
        user_id = session['id']

        # check if profile existing
        cursor = getCursor()
        cursor.execute(
			'select 1 from admin_profile where admin_id=%s;', (admin_id,)
        )
        profile = cursor.fetchone()
        if profile is None:
            cursor.execute(
				'insert into admin_profile values (%s, %s, %s, %s, %s, %s, %s, %s, %s);',
                (admin_id, user_id, first_name, last_name, address, email, phone, date_joined, status)
            )
            msg = 'profile not exist, added as new'
            return render_template('Administrator.html', msg2=msg)
        
        # Update profile in database
        update_query = """
        UPDATE admin_profile
        SET first_name = %s, last_name = %s, address = %s, email = %s, phone = %s, date_joined = %s, status = %s
        WHERE admin_id = %s
        """
        cursor.execute(update_query, (first_name, last_name, address, email, phone, date_joined, status, admin_id))
        connection.commit()
        msg = 'Proifle updated'
        return render_template('Administrator.html', msg2=msg)

@app.route("/pestcon_update_profile_by_others", methods=["GET","POST"])
def pestcon_update_profile_by_others():
    cursor = getCursor()
    # cursor = connection.cursor(dictionary=True)
    
    if request.method == "POST":
        # Extract data from form submission
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        address = request.form.get('address')
        email = request.form.get('email')
        phone = request.form.get('phone')
        date_joined = request.form.get('datejoined')
        date_joined_str = f"str_to_date('{date_joined}','%Y%m%d')"
        status = request.form.get('status')
        controller_id = request.form.get('pestcontrolleridnumber')
        user_id = request.form.get('pestcontrolleruserid')

        # check if profile existing
        cursor = getCursor()
        cursor.execute(
			'select 1 from controller_profile where controller_id=%s;', (controller_id,)
        )
        profile = cursor.fetchone()
        if profile is None:
            cursor.execute(
				'insert into controller_profile values (%s, %s, %s, %s, %s, %s, %s, %s, %s);',
                (controller_id, user_id, first_name, last_name, address, email, phone, date_joined, status)
            )
            msg = 'profile not exist, added as new'
            flash('profile not exist, added as new')
            return redirect(url_for('administrator'))
        
        # Update profile in database
        update_query = """
        UPDATE controller_profile
        SET first_name = %s, last_name = %s, address = %s, email = %s, phone = %s, date_joined = %s, status = %s
        WHERE controller_id = %s
        """
        cursor.execute(update_query, (first_name, last_name, address, email, phone, date_joined, status, controller_id))
        connection.commit()
        msg = 'Proifle updated'
        flash('Proifle updated')
        return redirect(url_for('administrator'))

@app.route("/staff_update_profile_by_others", methods=["GET", "POST"])
def staff_update_profile_by_others():
    if request.method == "POST":
        msg = ''
        staffnumber = request.form.get("staffnumber")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        workphonenumber = request.form.get("workphonenumber")
        position = request.form.get("position")
        department = request.form.get("department")
        hiredate = request.form.get("hiredate")
        status = request.form.get("status")
        user_id = request.form.get("staff_user")

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
            flash('profile not exist, added as new')
            return redirect(url_for('administrator'))
        
        cursor = getCursor()
        cursor.execute(
            'update staff_profile set staff_number = %s, first_name = %s, last_name = %s, email = %s, phone = %s, position = %s, department = %s, hire_date = %s, status = %s where user_id = %s;',
            (staffnumber, firstname, lastname, email, workphonenumber, position, department, hiredate, status, user_id)
        )
        flash('Proifle updated')
        return redirect(url_for('administrator'))
    
    cursor = getCursor()
    cursor.execute(
        'select staff_number, first_name, last_name, email, phone, position, department, hire_date, status from staff_profile where user_id = %s;',
        (session['id'],)
    )
    account = cursor.fetchone()
    return render_template("staffedit.html", account=account)

@app.route('/delete_controller/<controller_id>', methods=['POST'])
def delete_controller(controller_id):
    cursor = getCursor()
    cursor.execute(
		"delete from controller_profile where controller_id=%s;", (controller_id,)
    )
    return redirect(url_for('administrator'))

@app.route('/delete_staff/<staff_id>', methods=['POST'])
def delete_staff(staff_id):
    cursor = getCursor()
    cursor.execute(
		"delete from staff_profile where staff_id=%s;", (staff_id,)
    )
    return redirect(url_for('administrator'))

# change password for all roles
@app.route('/changePassword', methods=['POST'])
def change_password():
    current_user = session['id']
    cursor = getCursor()
    cursor.execute(
		"select a.password_hash from user a where user_id=%s;", (current_user,)
    )
    real_current_password = cursor.fetchone()
    
    current_password = request.form.get("currentPassword")
    new_password = request.form.get("newPassword")
    confirm_new_password = request.form.get("confirmNewPassword")
    hashed_current_password = hashing.hash_value(current_password, salt='emma_use_salt')


    if new_password != confirm_new_password:
        msg = 'Please enter same new passowrd'
    # elif not hashing.check_value(real_current_password, current_password, salt='emma_use_salt'):
    elif real_current_password[0] != hashed_current_password:
        msg = 'Old password error'
    else:
        hashed_password = hashing.hash_value(new_password, salt='emma_use_salt')
        cursor.execute(
            "update user a set a.password_hash=%s where user_id=%s;", (hashed_password, current_user, )
        )
        msg = 'Update password succeed'

    return render_template('index.html', msg=msg)

if __name__ == "__main__":
    app.run()