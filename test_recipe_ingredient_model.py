"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Recipe, Ingredient, Receipe_Ingredient, User_View_Receipe

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///recipes-test"


# Now we can import app

from app import app, get_ingredient, get_receipe_ingredient

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class RecipeModelTestCase(TestCase):
    """Test user model."""

    def setUp(self):
        """Create test client, add sample data."""

        Receipe_Ingredient.query.delete()
        User_View_Receipe.query.delete()
        Recipe.query.delete()
        Ingredient.query.delete()
        User.query.delete()
        self.client = app.test_client()
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u.id = 5555
        db.session.add(u)
        db.session.commit()
        recipe = Recipe(
            name = 'Pasta and Seafood',
            colories = 320,
            rating = 4.5,
            cost = 34,
            time_to_cook = 120,
            image = 'pasta.jpg'
        )
        recipe.id = 1234
        db.session.add(recipe)
        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_recipe_model(self):
        self.assertEqual(Recipe.query.get(1234).name,'Pasta and Seafood')

    def test_recipe_ingredient(self):

        ingredient1 = Ingredient(
            name = 'sugar'
        )

        ingredient2 = Ingredient(
            name = 'salt'
        )

        ingredient1.id = 3333
        ingredient2.id = 4444
        db.session.add(ingredient1)
        db.session.add(ingredient2)
        db.session.commit()

        self.assertEqual(Ingredient.query.get(3333),ingredient1)
        self.assertEqual(Ingredient.query.get(4444),ingredient2)
        self.assertEqual(Ingredient.query.get(3333).name,'sugar')
        self.assertEqual(Ingredient.query.get(4444).name,'salt')

        ri1 = Receipe_Ingredient(
            receipe_id = 1234,
            ingredient_id = 3333,
            unit = 'tsp',
            amount = 2,
            original = '2 tsp sugar',
            calorie = 40
        )

        ri2 = Receipe_Ingredient(
            receipe_id = 1234,
            ingredient_id = 4444,
            unit = 'tsp',
            amount = 1,
            original = '1 tsp salt',
            calorie = 0
        )
        recipe = Recipe.query.get(1234)
        recipe.ingredients = [ri1, ri2]
        db.session.add(recipe)
        db.session.commit()

        self.assertEqual(len(recipe.ingredients),2)
        self.assertEqual(recipe.ingredients[0].original, '2 tsp sugar')
        self.assertEqual(recipe.ingredients[1].original, '1 tsp salt')
    
    def test_user_view_recipe(self):
        recipe = Recipe.query.get(1234)
        user = User.query.get(5555)
        recipe.viewer = [user]
        db.session.add(recipe)
        db.session.commit()
        self.assertEqual(user.viewed_recipes,[recipe])
        #self.assertEqual(user.viewed_recipes[0],recipe)
