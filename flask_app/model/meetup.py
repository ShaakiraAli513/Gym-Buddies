from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.model import user
from flask_bcrypt import Bcrypt
from flask_app import app
from flask import flash
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Meetup:
    DB = "gymbuddy"

    def __init__(self, data):
        self.id = data['id']
        self.gym_name = data['gym_name']
        self.focus = data['focus']
        self.comments = data['comments']
        self.meet_date = data['meet_date']
        self.meet_time = data['meet_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.posted_by = None
        self.buddies = []


    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO meetups (gym_name, focus, comments, meet_date, meet_time, user_id) 
        VALUES (%(gym_name)s, %(focus)s, %(comments)s, %(meet_date)s, %(meet_time)s, %(user_id)s);
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print("CREATE MEET QUERY-->", results)
        return results


    @classmethod
    def user_meets(cls, data):
        #get all the meets for one user
        query = """
                SELECT * FROM meetups 
                JOIN users 
                ON users.id = meetups.user_id
                WHERE users.id = %(id)s;
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print("GET ONLY USERS MEETS QUERY--->", results)
        user_meetups = []
        
        for one_rep in results:
            for key in one_rep.keys():
                print (key)
            this_meetup = cls(one_rep)
            rep_data ={
                "id" : one_rep['users.id'],
                "first_name" : one_rep['first_name'],
                "last_name" :one_rep['last_name'],
                "email" : one_rep['email'],
                "age" : one_rep['age'],
                "password" : one_rep['password'],
                "created_at" : one_rep['users.created_at'],
                "updated_at" : one_rep['users.updated_at']
            }
            user_obj = user.User(rep_data)
            this_meetup.buddies = user_obj
            user_meetups.append(this_meetup)
        return user_meetups


    @classmethod
    def get_one_meet(cls, data):
        # get one meetup
        query = "SELECT * FROM meetups WHERE id= %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        print("GET ONE MEET QUERY -->", results)
        return cls(results[0])


    @classmethod
    def view_a_meet(cls,data):
        # view a single meet for a selected user
        query = """
        SELECT * FROM meetups JOIN users ON meetups.user_id = users.id
        WHERE meetups.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query,data)
        preworkout = cls(results[0])
        
        for gainz in results:
            buff_quads = {
                "id" :gainz["users.id"],
                "first_name" :gainz["first_name"],
                "last_name" :gainz["last_name"],
                "email" :gainz["email"],
                "age" : gainz["age"],
                "password" :gainz["password"],
                "created_at" :gainz["users.created_at"],
                "updated_at" :gainz["users.updated_at"]
            }
        preworkout.dumbell = user.User(buff_quads)
        return preworkout




    @classmethod
    def update_meet(cls, user_data):
        data ={
        "gym_name":user_data['gym_name'],
        "focus" : user_data['focus'],
        "comments" : user_data['comments'],
        "meet_date" : user_data['meet_date'],
        "meet_time" : user_data['meet_time'],
        "id" :user_data['id']
        
    }
        
        query = """
        UPDATE meetups SET gym_name=%(gym_name)s, focus =  %(focus)s, comments = %(comments)s, meet_date=%(meet_date)s, meet_time=%(meet_time)s WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query,data)
        print("UPDATE MEET QUERY--->",results)
        return results



    @classmethod
    def delete_meet(cls, data):
        query = "DELETE FROM meetups WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        print("DELETED MEET QUERY--->", results)
        return results


    @classmethod
    def buds_community(cls):
        #get meets from everyone
        query = """
                SELECT * FROM meetups 
                JOIN users 
                ON users.id = meetups.user_id;
                """
        results = connectToMySQL(cls.DB).query_db(query)
        print("GET ALL MEETS QUERY--->", results)
        community_gyms = []
        
        for a_bud in results:
            buff_up = cls(a_bud)
            buddy_data ={
                "id" : a_bud['users.id'],
                "first_name" : a_bud['first_name'],
                "last_name" :a_bud['last_name'],
                "email" : a_bud['email'],
                "age" : a_bud['age'],
                "password" : a_bud['password'],
                "created_at" : a_bud['users.created_at'],
                "updated_at" : a_bud['users.updated_at']
            }
            user_obj = user.User(buddy_data)
            buff_up.posted_by = user_obj
            community_gyms.append(buff_up)
        return community_gyms


    @staticmethod
    def validate_meetup(new_meetup):
        is_valid = True
        if len(new_meetup['gym_name']) < 3 :
            flash("Gym Name is too short.")
            is_valid = False
        if "focus" not in new_meetup :
            flash("Must choose one.")
            is_valid = False
        if len(new_meetup['comments']) < 3:
            flash("comment is too short.")
            is_valid = False
        if "meet_date" not in new_meetup :
            flash("Must choose a date")
            is_valid = False
        return is_valid