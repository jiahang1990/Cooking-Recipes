from flask import Flask, redirect, request, render_template, flash, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Recipe, Ingredient, Product, Recipe_Ingredient
from forms import UserAddForm, LoginForm, UserEditForm
import requests
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql:///recipes-app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] =os.environ.get('SECRET_KEY','secret') 

connect_db(app)
db.create_all()

CURR_USER_KEY = 'curr_user'
API_KEY = 'e513efac6a474bdcb825b99430ce9444'
#API_KEY = '1b579a9b11e746dcbddac1e89608d2d5'
RECEIPE_DEFAULT_IMG = '/static/images/recipe_default.gif'

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
    return render_template('home.html', user = g.user, recipes = recipes)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            do_login(user)
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
        do_login(user)
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
    view_recipe = Recipe.query.get(recipe_id)
    response = requests.get(f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}&includeNutrition=false')
    recipe = response.json()
    if g.user:
        if view_recipe:
            view_recipe.viewer.append(g.user)
        else:
            response = requests.get(f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}&includeNutrition=false')
            recipe = response.json()
            view_recipe = Recipe(
                id = recipe['id'],
                name = recipe['title'],
                image = recipe.get('image',RECEIPE_DEFAULT_IMG),
                viewer = [g.user]
            )
            ingredients = get_ingredient(recipe)
            view_recipe.ingredients = get_recipe_ingredient(recipe)
            db.session.add_all(ingredients)
            db.session.add(view_recipe)
            db.session.commit()
    else:
        if view_recipe:
            view_recipe.viewer.append(g.user)
        else:
            view_recipe = Recipe(
                id = recipe['id'],
                name = recipe['title'],
                image = recipe.get('image',RECEIPE_DEFAULT_IMG),
                viewer = []
            )
            ingredients = get_ingredient(recipe)
            view_recipe.ingredients = get_recipe_ingredient(recipe)
            db.session.add_all(ingredients)
            db.session.add(view_recipe)
            db.session.commit()
    return render_template('recipe.html', user = g.user, recipe = recipe)

@app.route('/search')
def search():
    search_type = request.args.get('type')
    search_term = request.args.get('term')
    response = requests.get(f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&query={search_term}')
    recipes = response.json()['results']
    return render_template('home.html', user = g.user, recipes = recipes)


def get_ingredient(recipe):
    ingredient_ids = [ingredient['id'] for ingredient in recipe['extendedIngredients']]
    ingredient_ids = list(set(ingredient_ids))
    ingredients = []
    for id in ingredient_ids:
        new_ingredient = Ingredient.query.get(id)
        if not new_ingredient:  
            response = requests.get(f'https://api.spoonacular.com/food/ingredients/{id}/information?apiKey={API_KEY}')
            data = response.json()
            new_ingredient = Ingredient(
                id = data['id'],
                name = data['name']
            )
        ingredients.append(new_ingredient)
    return ingredients

def get_recipe_ingredient(recipe):
    recipe_ingredients = []
    for ingredient in recipe['extendedIngredients']:
        recipe_ingredient = Recipe_Ingredient(
            recipe_id = recipe['id'],
            ingredient_id = ingredient['id'],
            original = ingredient['original']
        )
        recipe_ingredients.append(recipe_ingredient)
    return recipe_ingredients