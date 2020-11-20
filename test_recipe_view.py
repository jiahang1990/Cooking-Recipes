"""Recipe View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_recipe_view.py


import os
from unittest import TestCase
#from flask_testing import TestCase

from models import db, User, Recipe, Recipe_Ingredient, User_View_Recipe, Ingredient

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///recipes-test"

# Now we can import app

from app import app, do_login, add_user_to_g, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

#db.create_all()

class recipe_view(TestCase):

    def setUp(self):
        """Create test client, add sample data."""

        db.create_all()
        Recipe_Ingredient.query.delete()
        User_View_Recipe.query.delete()
        Recipe.query.delete()
        Ingredient.query.delete()
        User.query.delete()
        self.client = app.test_client()
        self.app = app
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
            calories = 320,
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

    def test_recipe_route_anomous_user(self):
        """Test recipe view page"""
        with self.client as c:
            resp = c.get('/recipes/1234')
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Grilled Sea Bass with Thai Chili Sauce', html)
            self.assertIn('https://spoonacular.com/recipeImages/1234-556x370.jpeg', html)
            self.assertIn("<h1 class = 'text-center'>Ingredient</h1>", html)
            self.assertIn("<h1 class = 'text-center'>Instructions</h1>", html)
