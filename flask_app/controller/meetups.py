from flask_app import app
from flask import Flask, render_template, redirect, request, session
from flask_app.model.user import User
from flask_app.model.meetup import Meetup





@app.route('/new-meetup')
def new_meetup():
    if "user_id" not in session:
        return ('/')
    data = {
        "id": session['user_id']
    }
    return render_template("meetups.html", logged_in_user = User.get_id(data))



@app.route('/create-meetup', methods=["POST"])
def create_meet():
    if "user_id" not in session:
        return('/')
    print("create_profile -->", request.form)
    for key,value in request.form.items():
        print (key,value)
    if not Meetup.validate_meetup(request.form):
        return redirect('/new-meetup')
    data ={
        "gym_name":request.form['gym_name'],
        "focus" : request.form['focus'],
        "comments" : request.form['comments'],
        "meet_date" : request.form['meet_date'],
        "meet_time" : request.form['meet_time'],
        "user_id" : session['user_id']
    }
    Meetup.create(data)
    return redirect("/view-profile")



@app.route('/edit-meet-up/<int:meetup_id>')
def edit_meet(meetup_id):
    if "user_id" not in session:
        return ('/')
    data = {
        "id": meetup_id
    }
    user_data = {
        "id": session["user_id"]
        }

    return render_template("edit-meet.html",logged_in_user = User.get_id(user_data), all_buds = Meetup.get_one_meet(data))



@app.route('/update-meetup/<int:id>', methods=["POST"])
def update_meetup(id):
    if "user_id" not in session:
        return ('/')
    print("update_meet -->", request.form)
    if not Meetup.validate_meetup(request.form):
        return redirect('/edit-meet-up/<int:tree_id>')
    id = Meetup.update_meet(request.form)
    # session['user_id'] = user_id
    return redirect('/view-profile')



@app.route('/delete-meetup/<int:id>')
def delete_meetup(id):
    if "user_id" not in session:
        return ('/')
    data = {
        "id": id
    }
    Meetup.delete_meet(data)
    return redirect('/view-profile')



@app.route('/view-profile')
def profile_page():
    if "user_id" not in session:
        return ('/')
    data = {
        "id": session['user_id']
    }
    return render_template("user-profile.html", logged_in_user = User.get_id(data), all_buds = Meetup.user_meets(data))


@app.route('/view-user-profile/<int:id>')
def user_profile_page(id):
    if "user_id" not in session:
        return ('/')
    if id == session["user_id"]:
        return redirect('/view-profile')
    
    data = {
        "id": id
    }
    # user_data = {
    #     "id": session['user_id']
    # }
    return render_template("other-user-profile.html", this_user = User.get_id(data), many_gains = Meetup.user_meets(data))



@app.route('/view-meet-up/<int:meetup_id>/<int:this_user_id>')
def view_meets(meetup_id, this_user_id):
    print("view a Users meet--->")
    if "user_id" not in session:
        return ('/')
    data = {
        "id": meetup_id
    }
    this_user_data = {
        "id": this_user_id
    }

    return render_template("view-meetup.html", this_user = User.get_id(this_user_data), this_meet = Meetup.get_one_meet(data))

# 