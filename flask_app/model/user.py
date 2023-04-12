from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.model import meetup
from flask_bcrypt import Bcrypt
from flask_app import app
from flask import flash
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "gymbuddy"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.age = data['age']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.buds = []



    @classmethod
    def create(cls, user_data):
        data ={
        "first_name":user_data['first_name'],
        "last_name": user_data['last_name'],
        "email": user_data['email'],
        "age" : user_data['age'],
        "password": bcrypt.generate_password_hash(user_data['password'])
    }
        query = """
        INSERT INTO users (first_name, last_name, email, age, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(age)s, %(password)s);
        """
        id = connectToMySQL(cls.DB).query_db(query, data)
        print("CREATE USER QUERY-->", id)
        return id



    @classmethod
    def get_id(cls, data):
        query = "SELECT * FROM users WHERE id= %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        print("GET_ID QUERY -->", results)
        return cls(results[0])


    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email= %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        print("GET_EMAIL QUERY -->", results)
        if results == ():
            return False
        return cls(results[0])



    @staticmethod
    def validate_create(user):
        is_valid = True
        if len(user['email']) < 6:
            flash("email is too short.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("email not in correct format!")
            is_valid = False
        data ={
                "email": user['email']
            }
        user_in_db = User.get_email(data)
        if user_in_db:
            flash("Email already taken.")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name is too short!")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name is too short!")
            is_valid = False
        if len(user['password']) < 8:
            flash("password too short!")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("passwords do not match!")
            is_valid = False
        if int(user['age']) < 18:
            flash("Must be 18 or older to join.")
            is_valid = False
        return is_valid
