from flask_app.config.mysqlconnector import MySQLConnection
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
regex = re.compile('[@_!#$%^&*()<>?/\\|}{~:]') #list of special characters

class User:

    DB = "group_project_schema"

    def __init__(self, data):
        
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def register(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"""
        result = MySQLConnection(cls.DB).query_db(query, data)
        return result
    
    @classmethod
    def get_by_email(cls, email):
        query = """SELECT
        *
        FROM
        users
        WHERE
        email = %(email)s
        ;"""
        results = MySQLConnection(cls.DB).query_db(query, {"email": email})
        if results:
            return User(results[0])
        else:
            return False
        
    @classmethod
    def get_by_id(cls, id):
        query = """SELECT
        *
        FROM
        users
        WHERE
        id = %(id)s
        ;"""
        results = MySQLConnection(cls.DB).query_db(query, {"id": id})
        return User(results[0])
    
    @staticmethod
    def validate_new_user(data):
        is_valid = True
        if len(data["email"]) < 1:
            flash("Email is required")
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash('Invalid email format')
            is_valid = False
        elif User.get_by_email(data['email']):
            flash("Email already registered")
            is_valid = False
        if len(data['first_name']) == 0:
            flash("First name must not be blank")
            is_valid = False    
        elif len(data['first_name']) < 2:
            flash("First name must be at least 2 characters long")
            is_valid = False
        if len(data['last_name']) == 0:
            flash("Last name must not be blank")
            is_valid = False
        elif len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters long")
            is_valid = False
        if len(data['password']) < 6:
            flash("Password must be longer than 5 characters")
            is_valid = False
        if data['password'] != data["confirm_password"]:
            flash("Passwords must match")
            is_valid = False
        if (regex.search(data['password']) == None): #this should search for special characters. None is if there aren't any
            flash("Password must include a special character")
            is_valid = False

        return is_valid
    
