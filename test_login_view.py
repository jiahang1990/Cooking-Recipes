"""Login View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_login_view.py


import os
from unittest import TestCase

from models import db, User, Recipe, Receipe_Ingredient, User_View_Receipe, Ingredient

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///recipes-test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

#db.create_all()

class recipe_view(TestCase):

    def setUp(self):
        """Create test client, add sample data."""

        db.create_all()
        User.query.delete()
        self.client = app.test_client()
        u = User.register(
            "testuser",
            "password",
            "test@test.com"
        )
        u.id = 5555
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_login_get(self):
        """Test login view page"""
        with self.client as c:
            resp = c.get('/login')
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<button class = 'btn btn-info'>Login</button>", html)
            self.assertIn("<a href='/signup' class = 'btn btn-primary'>Signup</a>", html)

    def test_login_post(self):
        """Test login view page"""
        with self.client as c:
            resp = c.post('/login', data = {'username':'testuser','password':'password'})
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("The CSRF token is missing", html)

    def test_signup_get(self):
        """Test login view page"""
        with self.client as c:
            resp = c.get('/signup')
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Login</a>", html)
            self.assertIn("<button class = 'btn btn-primary'>Signup</button>", html)

    def test_signup_post(self):
        """Test signup view page"""
        with self.client as c:
            resp = c.post('/signup', data = {'username':'testsignupuser','password':'password','email':'user@gmail.com'})
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("The CSRF token is missing", html)

        with self.client as c:
            app.config['WTF_CSRF_ENABLED'] = False
            resp = c.post('/signup', data = {'username':'testsignupuser','password':'password','email':'user@gmail.com'})
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 302)

        with self.client as c:
            app.config['WTF_CSRF_ENABLED'] = False
            resp = c.post('/signup', data = {'username':'testsignupuser2','password':'password','email':'user2@gmail.com'}, follow_redirects = True)
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('testsignupuser2', html)
            self.assertIn('Logout', html)
            self.assertIn('<img src =',html)
            self.assertIn('<p>Name:',html)
            self.assertIn('<p>Health score:',html)
            self.assertIn('<p>Price per serving:',html)
            resp = c.post('/signup', data = {'username':'testsignupuser2','password':'password','email':'usertest@gmail.com'}, follow_redirects = True)
            html = resp.get_data(as_text = True)
            self.assertIn('This username already exsits, please login', html)
            resp = c.post('/signup', data = {'username':'testsignupusertest','password':'password','email':'user2@gmail.com'}, follow_redirects = True)
            html = resp.get_data(as_text = True)
            self.assertIn('This email already exists', html)