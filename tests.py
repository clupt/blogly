import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import User, Post, DEFAULT_IMAGE_URL

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            fname="test1_first",
            lname="test1_last",
            img_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Test users page shows with test user name"""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_redirect_to_user(self):
        """Test redirect"""
        with self.client as c:
            resp = c.get("/")
            self.assertEqual(resp.status_code, 302)

    def test_new_user_form_html(self):
        """Test new form user form shows"""
        with self.client as c:
            resp = c.get("/users/new")
            html = resp.get_data(as_text=True)
            self.assertIn("TEST: isitworking?!",html)
            self.assertEqual(resp.status_code, 200)

    def test_add_new_user(self):
        """Test users page shows added user on new user form submit"""
        with self.client as c:
            resp = c.post("/users/new",
                          data={'fname': 'SOMEBODY',
                                'lname': 'LASTNAMED',
                                'img_url': ''
                                }, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('SOMEBODY', html)
            self.assertIn('LASTNAMED', html)
            self.assertEqual(resp.status_code, 200)

    def test_show_user_page(self):
        """Test user detail page shows user name and image"""
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)
            self.assertIn(DEFAULT_IMAGE_URL, html)
            self.assertEqual(resp.status_code, 200)

    def test_show_new_post_form(self):
        """Test the form shows to add new post"""
        with self.client as c:
            resp = c.get(f"users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- TEST: new_post form is working?!-->", html)
            self.assertEqual(resp.status_code, 200)

    def test_add_new_post(self):
        with self.client as c:
            resp = c.post(f"/users/{self.user_id}/posts/new",
                          data = {"title": 'SAMPLE TITLE',
                                  "content": "some content for the new post"
                                  }, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('SAMPLE TITLE', html)
            self.assertIn('<!--TEST: the detail page-->', html)
            self.assertEqual(resp.status_code, 200)

