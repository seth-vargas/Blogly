from unittest import TestCase

from app import app
from models import db, User
from seed import seed

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """ Tests for the User model """

    def setUp(self):
        """Clean up any existing users."""
        seed()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_get_full_name(self):
        """ Tests that the User get_full_name method is working """
        user = User(first_name="David", last_name="Bateman")
        self.assertEqual(user.get_full_name(), "David Bateman")

    def test_get(self):
        """ Tests that the User get method is working """
        u1 = User.get(1)
        u2 = User.get(2)
        self.assertEqual(u1.get_full_name(), "John Doe")
        self.assertEqual(u2.get_full_name(), "Jane Doe")


with app.test_client() as client:
    class AppTestCase(TestCase):
        """ Tests for the routes """

        def test_home_route(self):
            """ Tests that the home route redirects to /users """
            res = client.get('/')
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/users')

        def test_users_route(self):
            """ Tests that the /users route is displaying properly """
            res = client.get('/users')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)


        def test_users_new_route(self):
            """ Tests that the /users/new route is displaying properly """
            res = client.get('/users/new')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Create a user</h1>", html)
            

        def test_users_new_post_route(self):
            """ Tests that the /users/new POST request functions as expected """
            res = client.post('/users/new', data={
                "first-name": "John",
                "last-name": "Doe",
                "image-url": "", 
            })
            self.assertEqual(res.status_code, 302)
