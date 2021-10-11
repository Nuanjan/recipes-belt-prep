from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


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
