from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models import user


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.time_cook = data['time_cook']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.owner = {}

    @staticmethod
    def validate_recipe(recipeForm):
        is_valid = True
        if recipeForm['name'] == "":
            flash(" You must put recipe name")
            is_valid = False
        if recipeForm['description'] == "":
            flash(" You must put recipe description")
            is_valid = False
        if recipeForm['instructions'] == "":
            flash(" You must put recipe instructions")
            is_valid = False
        if len(recipeForm['name']) < 3:
            flash('name must be greater than 3 characters')
            is_valid = False
        if len(recipeForm['description']) < 3:
            flash('description must be greater than 3 characters')
            is_valid = False
        if len(recipeForm['instructions']) < 3:
            flash('instructions must be greater than 3 characters')
            is_valid = False
        if recipeForm['date_made'] == "":
            flash('Please enter a date')
            is_valid = False
        if 'time_cook' not in recipeForm:
            flash('Pleas select the cook time')
            is_valid = False
        return is_valid

    @classmethod
    def add_recipe(cls, data):
        print(data, " dta before add")
        query = "INSERT INTO recipes (name, description, instructions, date_made,time_cook,created_at, updated_at, user_id) VALUES(%(name)s, %(description)s, %(instructions)s, %(date_made)s,%(time_cook)s, NOW(), NOW(),%(user_id)s)"
        result = connectToMySQL('recipes_schema').query_db(query, data)
        return result

    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def edit_recipe(cls, data):
        print(data, " data before update")
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made=%(date_made)s, time_cook= %(time_cook)s, updated_at=NOW() WHERE recipes.id = %(id)s"
        return connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def all_recipes_with_users(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL('recipes_schema').query_db(query)

        # parse the data

        all_recipes = []

        for row in results:
            one_recipe = cls(row)

            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']

            }
            one_recipe.owner = user.User(user_data)
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def get_recipe_with_owner(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s"
        results = connectToMySQL('recipes_schema').query_db(query, data)

        one_recipe = cls(results[0])

        user_data = {
            "id": results[0]['users.id'],
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at']

        }

        one_recipe.owner = user.User(user_data)
        print(one_recipe, " one recipe from database")
        return one_recipe
