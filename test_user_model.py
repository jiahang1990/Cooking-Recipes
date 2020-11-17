"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User

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

db.create_all()


class UserModelTestCase(TestCase):
    """Test user model."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
        
    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(User.query.filter_by(username = "testuser").first(), u)
        self.assertEqual(User.query.filter_by(username = "testuser").first().email, "test@test.com")

    def test_invalid_username_signup(self):
        invalid = User.register(None, "password", "testinvalid@gmail.com")
        uid = 1234
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = User.register("testtest", "password", None)
        uid = 1234
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.register("testtest", "", "email@email.com")
        
        with self.assertRaises(ValueError) as context:
            User.register("testtest", None, "email@email.com")

    def test_auth(self):

        u1 = User.register(
            username="test1user",
            password="password1",
            email="test1@test.com"
        )

        db.session.add(u1)
        db.session.commit()
    
        u2 = User.authenticate("test1user", "password1")
        self.assertEqual(u1,u2)