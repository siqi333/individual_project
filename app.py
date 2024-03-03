from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

app = Flask(__name__)

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
def register_user():
    if request.method == "POST":
        # registe
        username = request.form.get("username")
        password = request.form.get("password")
        # ...
        return render_template("registed.html")
    else:
        return render_template("register.html")

if __name__ == "__main__":
    app.run()