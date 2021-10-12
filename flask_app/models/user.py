# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask import flash
import re
from flask_app.models import recipe

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{8,}\Z')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.recipes = []

    @staticmethod
    def validate_user(userFormData):
        is_valid = True  # we assume this is true
        if len(userFormData['first_name']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
        if len(userFormData['last_name']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False

        if len(userFormData['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if not PW_REGEX.match(userFormData['password']):
            flash("email must contain at least one digit")
            flash("email must contain at least one uppercase letter")
            flash("email must contain at least one lowercase letter")
            is_valid = False
        if userFormData['password'] != userFormData['confirm_password']:
            flash("Password and confirm password does not match")
            is_valid = False
        if not EMAIL_REGEX.match(userFormData['e_mail']):
            flash("Invalid email")
            is_valid = False
        data = {"email": userFormData['e_mail']}
        if User.get_user_by_email(data):
            flash("This Email already taken!")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login_user(data):
        is_valid = True
        if not data['user_in_db']:
            flash("Incorrect Email/Password")
            is_valid = False
        return is_valid

    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM users;"
    #     # make sure to call the connectToMySQL function with the schema you are targeting.
    #     results = connectToMySQL('users_schema').query_db(query)
    #     # Create an empty list to append our instances of users
    #     users = []
    #     # Iterate over the db results and create instances of users with cls.
    #     for user in results:
    #         users.append(cls(user))
    #     return users

    @classmethod
    def add_user(cls, data):
        print('data from queries: ', data)
        query = "INSERT INTO users (first_name , last_name , email ,password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s ,%(password)s, NOW() , NOW());"
        return connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def get_user_with_recipes(cls, data):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE users.id = %(id)s"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        print(results[0])
        user = cls(results[0])

        for row in results:
            recipe_data = {
                "id": row['recipes.id'],
                "name": row['name'],
                "description": row['description'],
                "instructions": row['instructions'],
                "date_made": row['date_made'],
                "time_cook": row['time_cook'],
                "created_at": row['recipes.created_at'],
                "updated_at": row['recipes.updated_at'],
                "user_id": row['user_id']
            }
            user.recipes.append(recipe.Recipe(recipe_data))

        return user

    # @classmethod
    # def edit_user(cls, data):
    #     print(data, " this is data before query")
    #     query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE users.id = %(id)s"
    #     # data is a dictionary that will be passed into the save method from server.py
    #     # will return the id of that data that we just insert in

    #     return connectToMySQL('users_schema').query_db(query, data)

    # @classmethod
    # def delete_user(cls, data):
    #     query = "DELETE FROM users WHERE users.id = %(id)s;"
    #     return connectToMySQL('users_schema').query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('recipes_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s"
        result = connectToMySQL('recipes_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
