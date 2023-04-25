from unittest import TestCase

from app import app
from models import db, User, Post
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


class PostModelTestCase(TestCase):
    """ Tests the Post Model """

    def setUp(self):
        """ Seed the file  """
        seed()

    def tearDown(self):
        """ Clean up any fouled transaction """
        db.session.rollback()

    def test_get_all_posts(self):
        """ Tests that the get_all_posts is working """
        posts = Post.get_all()
        self.assertEqual(len(posts), 1)

    def test_get_posts_by_user(self):
        post = Post.get_all_by_user(1)
        self.assertTrue(type(post) == list)


with app.test_client() as client:
    class RoutesTestCase(TestCase):
        """ Tests for the routes """

        def setUp(self):
            """Clean up any existing users."""
            seed()

        def tearDown(self):
            """Clean up any fouled transaction."""
            db.session.rollback()

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

        def test_list_posts(self):
            """ Tests that the posts display correctly """
            res = client.get('/posts')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>All Posts</h1>", html)

        def test_show_post(self):
            """ tests that the post displays correctly """
            res = client.get('/posts/1')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Created by", html)

        def test_users_new_post_route(self):
            """ Tests that the /users/new POST request functions as expected """
            res = client.post('/users/new', data={
                "first-name": "John",
                "last-name": "Doe",
                "image-url": ""})
            self.assertEqual(res.status_code, 302)

        def test_new_post(self):
            """ user with id of 1 will have a new post, making him have 2 total. """
            user_id = 1
            res = client.post(f'users/{user_id}/posts/new', data={
                "title": "This is a test post",
                "content": "This is some test content"
            })
            users_posts = Post.get_all_by_user(user_id)
            self.assertEqual(res.status_code, 302)
            self.assertEqual(len(users_posts), 2)

        def test_edit_post(self):
            """ testing the GET/POST requests """
            post_id = 1
            get_res = client.get(f"/posts/{post_id}/edit")
            post_res = client.post(f"/posts/{post_id}/edit", data={
                "title": "This is a test post",
                "content": "This is some test content"
            })
            html = get_res.get_data(as_text=True)
            self.assertEqual(get_res.status_code, 200)
            self.assertEqual(post_res.status_code, 302)
            self.assertIn(
                '<label for="title" class="col-sm-2 control-label">Title</label>', html)
