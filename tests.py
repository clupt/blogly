import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import User

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

    #TODO: add docstrings!

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    # def test_list_users(self):
    #     with self.client as c:
    #         resp = c.get("/users")
    #         self.assertEqual(resp.status_code, 200)
    #         html = resp.get_data(as_text=True)
    #         self.assertIn("test1_first", html)
    #         self.assertIn("test1_last", html)

    # def test_redirect_to_user(self):
    #     with self.client as c:
    #         resp = c.get("/")
    #         self.assertEqual(resp.status_code, 302)

    # def test_new_user_form_html(self):
    #     with self.client as c:
    #         resp = c.get("/users/new")
    #         html = resp.get_data(as_text=True)
    #         self.assertIn("TEST: isitworking?!",html)
    #         self.assertEqual(resp.status_code, 200)

    def test_add_new_user(self):
        # breakpoint()
        with self.client as c:
            resp = c.post("/users/new",
                          data={'fname': 'SOMEBODY',
                                'lname': 'LASTNAMED',
                                'img_url': ''
                                }, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('SOMEBODY', html)
            self.assertIn('LASTNAMED', html)
            # self.assertIn(DEFAULT_IMAGE_URL, html)
            self.assertEqual(resp.status_code, 200)




