from flask_app import app
from flask import redirect, render_template, session, request, url_for
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route("/recipe/new")
def recipe_new():
    if not 'user_id' in session:
        return render_template('forbidden.html')
    return render_template('new_recipe.html')


@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    if not 'user_id' in session:
        return render_template('forbidden.html')
    else:
        if not Recipe.validate_recipe(request.form):
            return redirect('/recipe/new')
        elif 'time_cook' in request.form:
            data = {
                'name': request.form['name'],
                'description': request.form['description'],
                'instructions': request.form['instructions'],
                'date_made': request.form['date_made'],
                'time_cook': request.form['time_cook'],
                "user_id": session['user_id']
            }
        session['table'] = "True"
        Recipe.add_recipe(data)
    return redirect('/user_dashboard')


@app.route('/recipe/<int:recipe_id>')
def get_recipe(recipe_id):
    if 'user_id' in session:
        data = {
            "id": recipe_id
        }
        user_data = {
            "id": session['user_id']
        }
        one_user = User.get_user_by_id(user_data)
        one_recipe = Recipe.get_recipe_by_id(data)
    return render_template('show_recipe.html', one_recipe=one_recipe, one_user=one_user)


@app.route('/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    data = {
        "id": recipe_id
    }
    one_recipe = Recipe.get_recipe_by_id(data)
    return render_template('edit_recipe.html', one_recipe=one_recipe)


@app.route('/edit_exist_recipe', methods=['POST'])
def edit_exist_recipe():
    if not 'user_id' in session:
        return render_template('forbidden.html')
    else:
        if not Recipe.validate_recipe(request.form):
            return redirect(f'/edit/{request.form["recipe_id"]}')
    data = {
        "id": request.form['recipe_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'time_cook': request.form['time_cook'],
        "user_id": session['user_id']
    }

    Recipe.edit_recipe(data)
    return redirect('/user_dashboard')


@app.route('/delete/<int:recipe_id>')
def delete(recipe_id):
    data = {
        "id": recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect('/user_dashboard')
