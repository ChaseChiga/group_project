from flask import render_template, redirect, request, session, flash

from group_project.flask_app.models.article import Article
from group_project.flask_app.models.user import User


from group_project.flask_app import app
from datetime import datetime


from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register_user():
    if not User.validate_new_user(request.form):
        return redirect("/create/account")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print(pw_hash)

    data = {
        
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,
    }

    user_id = User.register(data)
    session["user_id"] = user_id

    flash("Registration successful!", "success")

    return redirect("/")


@app.route("/create/account")
def create_account():
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
 
    login_data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(login_data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password")
        return redirect("/")

    session["user_id"] = user_in_db.id
    session["first_name"] = user_in_db.first_name
    session["last_name"] = user_in_db.last_name

    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


