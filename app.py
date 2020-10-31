from flask import Flask, redirect, render_template, flash, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Recipe, Ingredient, Product
from forms import UserAddForm, LoginForm, UserEditForm
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recepies-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] ='secret'

connect_db(app)
db.create_all()

CURR_USER_KEY = 'curr_user'
API_KEY = 'e513efac6a474bdcb825b99430ce9444'

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def home():
    response = requests.get(f'https://api.spoonacular.com/recipes/random?apiKey={API_KEY}&number=30')
    recipes = response.json()['recipes']
    if g.user:
        return render_template('user_home.html', user = g.user, recipes = recipes)
    else:
        return render_template('home.html', recipes = recipes)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            do_login(user)
            response = requests.get(f'https://api.spoonacular.com/recipes/random?apiKey={API_KEY}&number=30')
            recipes = response.json()['recipes']
            return redirect('/')
        else:
            flash('Username or password is not correct','danger')
            return render_template('login.html', form = form)
    return render_template('login.html', form = form)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserAddForm()
    if form.validate_on_submit():
        user = User.register(form.username.data, form.password.data, form.email.data)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('signup.html', form = form)
    return render_template('signup.html', form = form)

@app.route('/logout', methods = ['POST'])
def logout():
    do_logout()
    g.user = None
    return redirect('/')

@app.route('/recipes/<int:recipe_id>')
def recipe(recipe_id):
    response = requests.get(f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}&includeNutrition=false')
    recipe = response.json()
    return render_template('recipe.html', recipe = recipe)
    #return recipe