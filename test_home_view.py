"""Home View tests."""

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

class home_view(TestCase):

    def setUp(self):
        """Create test client, add sample data."""

        #db.drop_all()
        db.create_all()
        Recipe_Ingredient.query.delete()
        User_View_Recipe.query.delete()
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

    def test_home_route_anomous_user(self):
        """Test recipe view page"""
        with self.client as c:
            resp = c.get('/')
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Login', html)
            self.assertIn('Signup', html)

    def test_home_route_login_user(self):
        """Test recipe view page"""
        with self.client as c:
            with c.session_transaction() as sess:
                user = User.query.get(5555)
                sess[CURR_USER_KEY] = user.id
                
            resp = c.get('/')
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('testuser', html)
            self.assertIn('Logout', html)
            self.assertIn('<img src =',html)
            self.assertIn('<p>Name:',html)

