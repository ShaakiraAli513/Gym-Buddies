from flask_app import app
from flask import Flask, render_template, redirect, request, session
from flask_app.model.user import User
from flask_app.model.meetup import Meetup

from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)

@app.route('/')
def home_page():
    return render_template("index.html")


@app.route('/new-user', methods=["POST"])
def create_user():
    print("create_user -->", request.form)
    if not User.validate_create(request.form):
        return redirect('/')
    user_id = User.create(request.form)
    session['user_id'] = user_id
    return redirect ('/dashboard')


@app.route('/dashboard')
def user_page():
    if "user_id" not in session:
        return ('/')
    data = {
        "id": session['user_id']
    }
    return render_template("user-dashboard.html", logged_in_user = User.get_id(data), all_the_buds = Meetup.buds_community())




@app.route('/return-user', methods=["POST"])
def login():
    print("login-->", request.form)
    data ={
        "email": request.form['return_email']
    }
    user_in_db = User.get_email(data)
    if not user_in_db:
        flash("Invalid Password/Email")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['return_password']):
        flash("Invalid Password/Email")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
