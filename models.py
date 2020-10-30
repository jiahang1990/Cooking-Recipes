from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy_utils.types.choice import ChoiceType

db = SQLAlchemy()
USER_DEFAULT_IMG = '/static/images/profile_default.jpg'
RECEIPE_DEFAULT_IMG = '/static/images/receipe_default.gif'
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

    liked_recipes = db.relationship(
        "Recipe",
        secondary = "users_like_receipes",
        backref = 'liker'
    )

    owned_recipes = db.relationship(
        "Recipe",
        secondary = "users_own_receipes",
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
    """Table to store different receipe"""

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    colories = db.Column(db.Float)
    rating = db.Column(db.Float)
    cost = db.Column(db.Float)
    time_to_cook = db.Column(db.Float)
    image = db.Column(db.Text)

    ingredients = db.relationship(
        "Ingredient",
        secondary = "receipes_ingredients",
        backref = 'recipes'
    )

    products = db.relationship(
        "Product",
        secondary = "receipes_products",
        backref = 'recipes'
    )

class Ingredient(db.Model):
    """Table to store different ingredients"""

    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, unique = True, nullable = False)


class Product(db.Model):
    """Table to store different products"""

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, unique = True, nullable = False)

class User_Like_Receipe(db.Model):
    """Table to store user liked receipe relationship"""

    __tablename__ = 'users_like_receipes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    receipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key = True)
    rating = db.Column(db.Integer)

class User_Own_Receipe(db.Model):
    """Table to store user owned receipe relationship"""

    __tablename__ = 'users_own_receipes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    receipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key = True)
    time_to_cook = db.Column(db.Float)
    cost = db.Column(db.Float)

class Receipe_Ingredient(db.Model):
    """Table to store receipe ingredient relationship"""

    __tablename__ = 'receipes_ingredients'
    receipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key = True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key = True)
    unit = db.Column(db.String)
    amount = db.Column(db.Float)
    calorie = db.Column(db.Integer)

class Receipe_Product(db.Model):
    """Table to store receipe product relationship"""

    __tablename__ = 'receipes_products'
    receipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key = True)
    unit = db.Column(db.String)
    amount = db.Column(db.Float)
    calorie = db.Column(db.Integer)

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)