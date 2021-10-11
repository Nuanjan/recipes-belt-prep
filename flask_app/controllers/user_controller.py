from flask.helpers import flash
from flask_app import app
from flask import redirect, render_template, session, request, url_for
from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt,


@app.route('/')
def index():
    isShow = ""
    if 'isShow' in session:
        isShow = session["isShow"]
    return render_template('index.html', isShow=isShow)


@app.route('/register-login', methods=['POST'])
def register_user():
    session['isShow'] = request.form['which_form']
    if request.form['which_form'] == "register":
        if not User.validate_user(request.form):
            return redirect('/')
        hashed_password = bcrypt.generate_password_hash(
            request.form['password'])
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['e_mail'],
            "password": hashed_password
        }
        if not User.add_user(data):
            return redirect('/')
        session['user_id'] = User.add_user(data)
        return redirect('/user_dashboard')
    elif request.form['which_form'] == "login":
        data = {"email": request.form['e_mail']}
        # check if email exist in database
        user_in_db = User.get_user_by_email(data)
        validation_data = {
            "user_in_db": user_in_db,
            "password": request.form["password"]
        }
        if not User.validate_login_user(validation_data):
            return redirect('/')
        elif not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            print(bcrypt.check_password_hash(
                user_in_db.password, request.form['password']))
            flash("Invalid user/password")
            return redirect('/')
        session['isShow'] = request.form['which_form']
        session['user_id'] = user_in_db.id
        return redirect('/user_dashboard')


@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' in session:
        data = {
            "id": session['user_id']
        }
        one_user = User.get_user_by_id(data)
        user_recipes = User.get_user_with_recipes(data)
        return render_template('user_dashboard.html', user_recipes=user_recipes, one_user=one_user)
    else:
        return redirect('/forbidden')


@app.route('/logout')
def log_out():
    session.clear()
    return redirect('/')


@app.route('/forbidden')
def unauthorize():
    return render_template('forbidden.html')
