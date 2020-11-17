from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType

db = SQLAlchemy()
USER_DEFAULT_IMG = '/static/images/profile_default.jpg'
RECIPE_DEFAULT_IMG = '/static/images/recipe_default.gif'
bcrypt = Bcrypt()

class User(db.Model):
    """Table to store user information"""

    GENDER = [
        ('Male','M'),
        ('Female','F')
    ]
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    email = db.Column(db.String(256), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    image = db.Column(db.String, default = USER_DEFAULT_IMG)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    gender = db.Column(ChoiceType(GENDER))
    age = db.Column(db.Integer)

    viewed_recipes = db.relationship(
        "Recipe",
        secondary = "users_view_recipes",
        backref = 'viewer'
    )

    liked_recipes = db.relationship(
        "Recipe",
        secondary = "users_like_recipes",
        backref = 'liker'
    )

    owned_recipes = db.relationship(
        "Recipe",
        secondary = "users_own_recipes",
        backref = 'owner'
    )
    
    @classmethod
    def register(cls, username, password, email):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username = username,
            password = hashed_utf8,
            email = email
        )
        db.session.add(user)
        return user
        
    @classmethod
    def authenticate(cls, username, password):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = User.query.filter_by(username = username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Recipe(db.Model):
    """Table to store different recipe"""

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    calories = db.Column(db.Float)
    rating = db.Column(db.Float)
    cost = db.Column(db.Float)
    time_to_cook = db.Column(db.Float)
    image = db.Column(db.String, default = RECIPE_DEFAULT_IMG)
    instructions = db.Column(MutableList.as_mutable(PickleType), default = [])

    ingredients = db.relationship(
        "Recipe_Ingredient",
        backref = 'recipes'
    )

    products = db.relationship(
        "Recipe_Product",
        backref = 'recipes'
    )

class Ingredient(db.Model):
    """Table to store different ingredients"""

    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, unique = True, nullable = False)

    recipes = db.relationship(
        "Recipe_Ingredient",
        backref = 'ingredients'
    )


class Product(db.Model):
    """Table to store different products"""

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, unique = True, nullable = False)

class User_View_Recipe(db.Model):
    """Table to store user viewed recipe relationship"""

    __tablename__ = 'users_view_recipes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key = True)
    rating = db.Column(db.Integer)

class User_Like_Recipe(db.Model):
    """Table to store user liked recipe relationship"""

    __tablename__ = 'users_like_recipes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key = True)
    rating = db.Column(db.Integer)

class User_Own_Recipe(db.Model):
    """Table to store user owned recipe relationship"""

    __tablename__ = 'users_own_recipes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key = True)
    time_to_cook = db.Column(db.Float)
    cost = db.Column(db.Float)

class Recipe_Ingredient(db.Model):
    """Table to store recipe ingredient relationship"""

    __tablename__ = 'recipes_ingredients'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    unit = db.Column(db.String)
    amount = db.Column(db.Float)
    original = db.Column(db.String)
    calorie = db.Column(db.Integer)

class Recipe_Product(db.Model):
    """Table to store recipe product relationship"""

    __tablename__ = 'recipes_products'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key = True)
    unit = db.Column(db.String)
    amount = db.Column(db.Float)
    calorie = db.Column(db.Integer)

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)
